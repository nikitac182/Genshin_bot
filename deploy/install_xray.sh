#!/usr/bin/env bash
# Установка xray-core на Raspberry Pi (armv7 - обычная Raspberry Pi OS 32-bit,
# для Pi 3 это стандарт; если у вас 64-bit ОС - смените ARCH на arm64-v8a)
set -e

ARCH="arm32-v7a"   # 64-bit Raspberry Pi OS -> "arm64-v8a"
VERSION="v1.8.24"  # можно проверить актуальную на github.com/XTLS/Xray-core/releases

sudo mkdir -p /opt/xray
cd /tmp
curl -L -o xray.zip "https://github.com/XTLS/Xray-core/releases/download/${VERSION}/Xray-linux-${ARCH}.zip"
sudo unzip -o xray.zip -d /opt/xray
sudo chmod +x /opt/xray/xray
rm xray.zip

echo "xray установлен в /opt/xray. Теперь положите ваш config.json в /opt/xray/config.json"
