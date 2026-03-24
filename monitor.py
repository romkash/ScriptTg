import asyncio
from telethon import TelegramClient, events
import requests
import logging
import os

# ============= ВАШИ ДАННЫЕ =============
API_ID = 32156450
API_HASH = '969799d773d7e9095b76f50a693f9e31'
BOT_TOKEN = '7667185968:AAFlHcZP4tTVyGsmAddRbIMzKa5wVNOOPHs'
CHAT_ID = '7213969441'
KEYWORD = 'куплю'
PASSWORD = 'ngrief12'
IMPORTANT_KEYWORD = 'восток'

# Список пользователей для автоматического ответа
AUTO_REPLY_USERS = {
    'aahaahahah1': 'привет, могу продать',
    'Pashapure': 'привет, могу продать'
}

# Сообщение для пересылки
MESSAGE_TO_FORWARD = 'https://t.me/lamavaape/42'
# ======================================

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Создаем клиент
user_client = TelegramClient('user_session', API_ID, API_HASH)

def get_user_link(username, user_id, first_name):
    """Создает ссылку на пользователя"""
    if username:
        return f"https://t.me/{username}"
    else:
        return f"tg://user?id={user_id}"

def send_notification(message_text, chat_name, sender_id, sender_username, sender_first_name, is_important=False):
    """Отправка уведомления с ссылкой на пользователя"""
    
    if is_important:
        title_emoji = "🔴🔴🔴 ВАЖНО 🔴🔴🔴"
        border = "🔴" * 20
    else:
        title_emoji = "🔔 НАЙДЕНО"
        border = "━" * 20
    
    user_link = get_user_link(sender_username, sender_id, sender_first_name)
    
    notification = (
        f"<b>{title_emoji}</b>\n"
        f"{border}\n"
        f"📱 <b>Чат:</b> {chat_name}\n"
        f"👤 <b>Пользователь:</b> <a href='{user_link}'>{sender_first_name}</a>\n"
        f"💬 <b>Сообщение:</b>\n<code>{message_text[:500]}</code>\n"
        f"{border}\n"
    )
    
    if sender_username and sender_username in AUTO_REPLY_USERS:
        notification += f"🤖 <b>Автоответ:</b> Отправлен автоматический ответ\n"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': notification,
        'parse_mode': 'HTML',
        'disable_web_page_preview': False
    }
    
    try:
        requests.post(url, json=payload, timeout=10)
        logger.info(f"✅ Уведомление из чата: {chat_name}")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")

def check_important_message(text):
    if not text:
        return False
    return IMPORTANT_KEYWORD.lower() in text.lower()

async def forward_message_to_user(user_client, target_username, original_message):
    """Пересылает сообщение пользователю"""
    try:
        user = await user_client.get_entity(target_username)
        reply_text = AUTO_REPLY_USERS.get(target_username, "привет, могу продать")
        
        try:
            parts = MESSAGE_TO_FORWARD.split('/')
            channel_username = parts[-2]
            message_id = int(parts[-1])
            
            channel = await user_client.get_entity(channel_username)
            message_to_forward = await user_client.get_messages(channel, ids=message_id)
            
            if message_to_forward:
                await user_client.send_message(user, reply_text, link_preview=False)
                await user_client.forward_messages(user, message_to_forward, channel)
                logger.info(f"✅ Автоответ @{target_username} с пересылкой")
            else:
                await user_client.send_message(user, reply_text)
                logger.info(f"✅ Автоответ @{target_username} (без пересылки)")
        except Exception as e:
            logger.error(f"Ошибка пересылки: {e}")
            await user_client.send_message(user, reply_text)
            logger.info(f"✅ Автоответ @{target_username} (только текст)")
    except Exception as e:
        logger.error(f"Ошибка автоответа @{target_username}: {e}")

async def main():
    try:
        print("=" * 60)
        print("🤖 Telegram Монитор (Railway)")
        print("=" * 60)
        
        # Авторизация с сохранением сессии
        await user_client.start(
            phone=lambda: input("📱 Введите номер: "),
            code_callback=lambda: input("🔑 Введите код: "),
            password=lambda: PASSWORD
        )
        
        logger.info("✅ Авторизация успешна!")
        
        @user_client.on(events.NewMessage)
        async def handler(event):
            try:
                message_text = event.message.text or event.message.caption or ""
                if not message_text:
                    return
                
                if KEYWORD.lower() in message_text.lower():
                    chat = await event.get_chat()
                    sender = await event.get_sender()
                    
                    if hasattr(chat, 'title') and chat.title:
                        chat_name = chat.title
                    elif hasattr(chat, 'first_name'):
                        chat_name = chat.first_name
                        if hasattr(chat, 'last_name') and chat.last_name:
                            chat_name += f" {chat.last_name}"
                    else:
                        chat_name = "Unknown"
                    
                    sender_username = sender.username if hasattr(sender, 'username') else None
                    sender_first_name = sender.first_name if hasattr(sender, 'first_name') else "Unknown"
                    is_important = check_important_message(message_text)
                    
                    send_notification(
                        message_text=message_text,
                        chat_name=chat_name,
                        sender_id=sender.id,
                        sender_username=sender_username,
                        sender_first_name=sender_first_name,
                        is_important=is_important
                    )
                    
                    if sender_username and sender_username in AUTO_REPLY_USERS:
                        await forward_message_to_user(user_client, sender_username, event.message)
                    
                    if is_important:
                        logger.info(f"🔴 ВАЖНОЕ сообщение в {chat_name}")
                    else:
                        logger.info(f"📨 Найдено сообщение в {chat_name}")
                    
            except Exception as e:
                logger.error(f"Ошибка: {e}")
        
        logger.info("👀 Мониторинг запущен 24/7")
        await user_client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
    finally:
        await user_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())