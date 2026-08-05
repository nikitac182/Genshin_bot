"""
Превращает ссылку из Happ (vless:// / vmess:// / trojan://) в config.json для xray.

Использование:
    python3 link_to_config.py "vless://..." > /opt/xray/config.json

Как достать ссылку из Happ:
  Настройки сервера -> "Поделиться" / "Экспортировать" -> "Копировать ссылку"
  (обычно она начинается с vless:// или vmess://).
"""
import sys
import json
import base64
from urllib.parse import urlparse, parse_qs, unquote

SOCKS_PORT = 10808


def build_vless(url: str) -> dict:
    p = urlparse(url)
    q = parse_qs(p.query)
    outbound = {
        "tag": "proxy",
        "protocol": "vless",
        "settings": {
            "vnext": [{
                "address": p.hostname,
                "port": p.port or 443,
                "users": [{
                    "id": p.username,
                    "encryption": "none",
                    "flow": q.get("flow", [""])[0],
                }],
            }]
        },
        "streamSettings": {
            "network": q.get("type", ["tcp"])[0],
            "security": q.get("security", ["none"])[0],
        },
    }
    sec = q.get("security", ["none"])[0]
    if sec == "reality":
        outbound["streamSettings"]["realitySettings"] = {
            "serverName": q.get("sni", [""])[0],
            "fingerprint": q.get("fp", ["chrome"])[0],
            "publicKey": q.get("pbk", [""])[0],
            "shortId": q.get("sid", [""])[0],
        }
    elif sec == "tls":
        outbound["streamSettings"]["tlsSettings"] = {
            "serverName": q.get("sni", [p.hostname])[0],
            "fingerprint": q.get("fp", ["chrome"])[0],
        }
    return outbound


def build_vmess(url: str) -> dict:
    raw = url[len("vmess://"):]
    data = json.loads(base64.b64decode(raw + "=" * (-len(raw) % 4)))
    outbound = {
        "tag": "proxy",
        "protocol": "vmess",
        "settings": {
            "vnext": [{
                "address": data["add"],
                "port": int(data["port"]),
                "users": [{"id": data["id"], "alterId": int(data.get("aid", 0))}],
            }]
        },
        "streamSettings": {"network": data.get("net", "tcp")},
    }
    if data.get("tls") == "tls":
        outbound["streamSettings"]["security"] = "tls"
        outbound["streamSettings"]["tlsSettings"] = {"serverName": data.get("sni", data["add"])}
    return outbound


def build_trojan(url: str) -> dict:
    p = urlparse(url)
    q = parse_qs(p.query)
    return {
        "tag": "proxy",
        "protocol": "trojan",
        "settings": {
            "servers": [{"address": p.hostname, "port": p.port or 443, "password": unquote(p.username)}]
        },
        "streamSettings": {
            "network": q.get("type", ["tcp"])[0],
            "security": "tls",
            "tlsSettings": {"serverName": q.get("sni", [p.hostname])[0]},
        },
    }


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    link = sys.argv[1].strip()
    if link.startswith("vless://"):
        outbound = build_vless(link)
    elif link.startswith("vmess://"):
        outbound = build_vmess(link)
    elif link.startswith("trojan://"):
        outbound = build_trojan(link)
    else:
        print("Не распознан протокол. Поддерживаются vless://, vmess://, trojan://", file=sys.stderr)
        sys.exit(1)

    config = {
        "log": {"loglevel": "warning"},
        "inbounds": [{
            "listen": "127.0.0.1",
            "port": SOCKS_PORT,
            "protocol": "socks",
            "settings": {"auth": "noauth", "udp": True},
        }],
        "outbounds": [outbound, {"tag": "direct", "protocol": "freedom"}],
    }
    print(json.dumps(config, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
