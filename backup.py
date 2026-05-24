import asyncio
import aiosqlite
import shutil
from datetime import datetime


async def backup_database():
    """Создаёт бэкап базы данных"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backups_{timestamp}.db"
    
    import os
    os.makedirs("backups", exist_ok=True)
    
    shutil.copy2("sqlite.db", backup_name)
    print(f"✅ Бэкап создан: {backup_name}")
    
    backups = sorted([f for f in os.listdir("backups") if f.startswith("sqlite_")])
    for old_backup in backups[:-7]:
        os.remove(f"backups/{old_backup}")
        print(f"🗑️ Удалён старый бэкап: {old_backup}")


if __name__ == "__main__":
    asyncio.run(backup_database())