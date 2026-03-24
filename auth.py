# auth_local.py - запустите на своем ПК один раз
import asyncio
from telethon import TelegramClient
from datetime import datetime

# Ваши данные
API_ID = 32156450
API_HASH = '969799d773d7e9095b76f50a693f9e31'
PHONE_NUMBER = '+375298206967'
PASSWORD = 'ngrief12'

# Имя файла сессии (без временной метки для постоянного использования)
session_name = 'user_session_permanent'

async def main():
    print("=" * 50)
    print("🔐 Авторизация Telegram для Railway")
    print("=" * 50)
    print(f"📱 Номер: {PHONE_NUMBER}")
    print()
    
    client = TelegramClient(session_name, API_ID, API_HASH)
    
    try:
        # Запрашиваем код
        code = input("📲 Введите код из Telegram: ")
        
        await client.start(
            phone=PHONE_NUMBER,
            code=code,
            password=lambda: PASSWORD
        )
        
        print()
        print("✅ Авторизация успешна!")
        print(f"📁 Файл сессии сохранен: {session_name}.session")
        
        me = await client.get_me()
        print(f"👤 Аккаунт: {me.first_name} (@{me.username})")
        print()
        print("Теперь загрузите эти файлы на GitHub:")
        print(f"  - {session_name}.session")
        print(f"  - {session_name}.session-journal (если есть)")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())