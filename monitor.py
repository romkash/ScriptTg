import asyncio
from telethon import TelegramClient, events
import requests
import logging
import re
import os

# ============= ВАШИ ДАННЫЕ =============
API_ID = 32156450
API_HASH = '969799d773d7e9095b76f50a693f9e31'
BOT_TOKEN = '7667185968:AAFlHcZP4tTVyGsmAddRbIMzKa5wVNOOPHs'
CHAT_ID = '7213969441'
PHONE_NUMBER = '+375298206967'
PASSWORD = 'ngrief12'

# Список пользователей для автоматического ответа
AUTO_REPLY_USERS = {
    'aahaahahah1': 'привет, могу продать',
    'Pashapure': 'привет, могу продать'
}

# Сообщение для пересылки
MESSAGE_TO_FORWARD = 'https://t.me/lamavaape/42'
# ======================================

# ============= РАСШИРЕННЫЕ ТРИГГЕРЫ =============
TRIGGER_WORDS = [
    'куплю', 'ищу', 'жижу', 'жижку', 'жидкость', 'жижки',
    'солевую жижу', 'жижу с никотином', 'жижу без никотина',
    'никотиновые жидкости', 'фруктовую жижу', 'сладкую жижу',
    'крепкую жижу', 'свежую жижу', 'жижу оптом', 'жижу недорого',
    'карик', 'картридж', 'картриджи', 'испаритель', 'испарители',
    'сменники', 'сменный картридж', 'картриджи на под',
    'оригинальные картриджи', 'оригинальные поды',
    'под', 'поды', 'подик', 'одноразку', 'одноразки',
    'вейп', 'вейпы', 'подоночки', '5 мини',
    'подонки', 'catswill', 'коты', 'котов', 'найс шот',
    'кэствил', 'хотспот', 'лабубу', 'злую', 'восток', 'карик',
    'тех уник', 'технический', 'политех', 'рик', 'rick', 'аркад',
    'монашку', 'злую монашку', 'хрос', 'расходник', 'расходники',
    'вкусные одноразки', 'табачку', 'оригинал', 'солевые вкусы',
    'топ вкусы', 'новые вкусы', 'популярные вкусы', 'кислые',
    'кислый', 'кислую', 'сладкую', 'вкусную', 'на востоке', 'на дк',
    'на замерзоне', 'замерзон', 'у церкви', 'на белой', 'доставкой',
    'жижу куплю', 'карик куплю', 'жижку куплю', 'картридж куплю', 'куплю жижу банк',
]

IMPORTANT_KEYWORDS = ['восток', 'куплю жижу', 'куплю восток', 'на востоке', 'ищу восток']

def create_regex_pattern():
    escaped_words = [re.escape(word) for word in TRIGGER_WORDS]
    return re.compile('|'.join(escaped_words), re.IGNORECASE)

TRIGGER_PATTERN = create_regex_pattern()

def check_important_message(text):
    if not text:
        return False
    text_lower = text.lower()
    for keyword in IMPORTANT_KEYWORDS:
        if keyword in text_lower:
            return True
    return False

def get_matched_triggers(text):
    if not text:
        return []
    matches = TRIGGER_PATTERN.findall(text.lower())
    return list(set(matches))
# ======================================

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Имя файла сессии
session_name = f'user_session_{PHONE_NUMBER[-8:]}'

# Создаем клиент
user_client = TelegramClient(session_name, API_ID, API_HASH)

def get_user_link(username, user_id, first_name):
    if username:
        return f"https://t.me/{username}"
    else:
        return f"tg://user?id={user_id}"

def send_notification(message_text, chat_name, sender_id, sender_username, sender_first_name, is_important=False, matched_triggers=None):
    if matched_triggers is None:
        matched_triggers = []
    
    if is_important:
        title_emoji = "🔴🔴🔴 ВАЖНО 🔴🔴🔴"
        border = "🔴" * 25
    else:
        title_emoji = "🔔 НАЙДЕНО"
        border = "━" * 25
    
    user_link = get_user_link(sender_username, sender_id, sender_first_name)
    
    triggers_text = ""
    if matched_triggers:
        triggers_text = f"🎯 <b>Найдено:</b> {', '.join(matched_triggers[:5])}\n"
    
    notification = (
        f"<b>{title_emoji}</b>\n"
        f"{border}\n"
        f"📱 <b>Чат:</b> {chat_name}\n"
        f"👤 <b>Пользователь:</b> <a href='{user_link}'>{sender_first_name}</a>\n"
        f"🆔 <b>ID:</b> <code>{sender_id}</code>\n"
        f"{triggers_text}"
        f"💬 <b>Сообщение:</b>\n<code>{message_text[:500]}</code>\n"
        f"{border}\n"
    )
    
    if sender_username and sender_username in AUTO_REPLY_USERS:
        notification += f"🤖 <b>Автоответ:</b> Будет отправлен автоматический ответ\n"
    
    if is_important:
        notification += f"⚠️ <b>СРОЧНО!</b> Важное сообщение!\n"
        notification += f"💡 Нажмите на имя пользователя, чтобы написать ему"
    
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

async def forward_message_to_user(user_client, target_username, original_message):
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
                logger.info(f"✅ Автоответ @{target_username}")
            else:
                await user_client.send_message(user, reply_text)
                logger.info(f"✅ Автоответ @{target_username} (текст)")
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            await user_client.send_message(user, reply_text)
    except Exception as e:
        logger.error(f"Ошибка: {e}")

async def main():
    try:
        print("=" * 70)
        print("🤖 Telegram Монитор сообщений")
        print("=" * 70)
        print(f"📱 Номер: {PHONE_NUMBER}")
        print(f"📝 Отслеживается {len(TRIGGER_WORDS)} фраз")
        print("=" * 70)
        
        # Проверяем, существует ли файл сессии
        if os.path.exists(f'{session_name}.session'):
            logger.info("Найдена сохраненная сессия, подключаемся...")
            # Подключаемся с использованием сохраненной сессии
            await user_client.start(
                phone=PHONE_NUMBER,
                password=lambda: PASSWORD  # Автоматический ввод пароля
            )
        else:
            logger.info("Сессия не найдена, требуется авторизация...")
            # Запрашиваем код и автоматически вводим пароль
            code = input("🔑 Введите код из Telegram: ")
            await user_client.start(
                phone=PHONE_NUMBER,
                code=code,
                password=lambda: PASSWORD  # Автоматический ввод пароля
            )
        
        logger.info("✅ Подключение успешно!")
        
        me = await user_client.get_me()
        logger.info(f"👤 Аккаунт: {me.first_name} (@{me.username})")
        
        # Получаем список чатов
        dialogs = await user_client.get_dialogs()
        logger.info(f"📊 Найдено чатов: {len(dialogs)}")
        
        groups = sum(1 for d in dialogs if d.is_group)
        channels = sum(1 for d in dialogs if d.is_channel)
        users = sum(1 for d in dialogs if d.is_user)
        logger.info(f"📈 Статистика: {groups} групп, {channels} каналов, {users} личных чатов")
        
        @user_client.on(events.NewMessage)
        async def handler(event):
            try:
                message_text = event.message.text or event.message.caption or ""
                if not message_text:
                    return
                
                matched_triggers = get_matched_triggers(message_text)
                
                if matched_triggers:
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
                        is_important=is_important,
                        matched_triggers=matched_triggers
                    )
                    
                    if sender_username and sender_username in AUTO_REPLY_USERS:
                        await forward_message_to_user(user_client, sender_username, event.message)
                    
                    triggers_str = ', '.join(matched_triggers[:3])
                    if is_important:
                        logger.info(f"🔴 ВАЖНОЕ [{triggers_str}] в {chat_name}")
                    else:
                        logger.info(f"📨 [{triggers_str}] в {chat_name}")
                    
            except Exception as e:
                logger.error(f"Ошибка: {e}")
        
        logger.info("👀 Мониторинг запущен 24/7")
        await user_client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
    finally:
        await user_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())