# auth.py - запустите один раз для авторизации
import asyncio
from telethon import TelegramClient
import os

# Ваши данные
API_ID = 32156450
API_HASH = '969799d773d7e9095b76f50a693f9e31'
PHONE_NUMBER = '+375299206967'
PASSWORD = 'ngrief12'

session_name = f'user_session_{PHONE_NUMBER[-8:]}'

async def main():
    print("=" * 50)
    print("🔐 Авторизация Telegram")
    print("=" * 50)
    print(f"📱 Номер: {PHONE_NUMBER}")
    print()
    
    client = TelegramClient(session_name, API_ID, API_HASH)
    
    try:
        # Пытаемся авторизоваться
        await client.start(
            phone=PHONE_NUMBER,
            code_callback=lambda: input("📲 Введите код из Telegram: "),
            password=lambda: input("🔑 Введите пароль (если есть): ") if PASSWORD else None
        )
        
        print()
        print("✅ Авторизация успешна!")
        print(f"📁 Сессия сохранена в файл: {session_name}.session")
        print()
        print("Теперь можно запускать monitor.py")
        
        # Показываем информацию об аккаунте
        me = await client.get_me()
        print(f"👤 Аккаунт: {me.first_name} (@{me.username})")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())