# Деплой Genshin-Bot на Raspberry Pi 3 через Happ-прокси

## Важно про venv
В архиве лежит venv, собранный под **Windows** (python.exe, Scripts/) — на Raspberry Pi (Linux/ARM)
он не запустится. На самой малине нужно создать venv заново.

## Шаг 0. Перенос проекта на Pi
Скопируйте папку `Genshin-Bot` (без `venv` и `__pycache__`) на Raspberry Pi, например в `/home/pi/Genshin-Bot`.

```bash
scp -r Genshin-Bot pi@<IP_МАЛИНЫ>:/home/pi/
```

## Шаг 1. Достаём ссылку из Happ
В приложении Happ: откройте нужный сервер подписки -> "Поделиться"/"Экспорт" -> "Скопировать ссылку".
Получите строку вида `vless://...`, `vmess://...` или `trojan://...`.

## Шаг 2. Ставим xray-core на Pi
```bash
cd /home/pi/Genshin-Bot/deploy
chmod +x install_xray.sh
./install_xray.sh
```
Если у вас 64-битная Raspberry Pi OS — до запуска поменяйте `ARCH` в `install_xray.sh` на `arm64-v8a`
(узнать битность: `uname -m` -> `aarch64` = 64-бит, `armv7l` = 32-бит).

## Шаг 3. Конвертируем ссылку в конфиг xray
```bash
python3 link_to_config.py "ВАША_ССЫЛКА_ИЗ_HAPP" | sudo tee /opt/xray/config.json
```

## Шаг 4. Запускаем xray как службу
```bash
sudo cp xray.service /etc/systemd/system/xray.service
sudo systemctl daemon-reload
sudo systemctl enable --now xray.service
sudo systemctl status xray.service
```
Проверка, что прокси реально работает (должен вернуть IP вашего VPN-сервера):
```bash
curl -x socks5h://127.0.0.1:10808 https://api.telegram.org
```

## Шаг 5. Ставим бота
```bash
cd /home/pi/Genshin-Bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```
Проверьте `.env` — там уже должна быть строка:
```
PROXY_URL=socks5://127.0.0.1:10808
```

## Шаг 6. Бот как служба
```bash
sudo cp deploy/genshin-bot.service /etc/systemd/system/genshin-bot.service
sudo systemctl daemon-reload
sudo systemctl enable --now genshin-bot.service
sudo journalctl -u genshin-bot.service -f
```

Если в логах пошёл polling без ошибок 502/Connection — значит бот успешно ходит в Telegram через ваш Happ-сервер.

## Если понадобится системный VPN на весь Pi (вариант B)
Вместо локального SOCKS5-инбаунда в `config.json` можно использовать `sing-box` с TUN-режимом —
это сложнее в настройке и не рекомендуется для Pi 3, но если понадобится, скажите — соберу отдельную инструкцию.
