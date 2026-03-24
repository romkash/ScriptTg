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

# ============= ТОЧНОЕ СОВПАДЕНИЕ ДЛЯ ТРИГГЕРОВ =============
# Слова, которые должны быть в сообщении (не подстроки, а именно эти слова)
TRIGGER_WORDS_EXACT = [
    'куплю', 'ищу', 'жижу', 'жижку', 'жидкость', 'жижки',
    'карик', 'картридж', 'картриджи', 'испаритель', 'испарители',
    'под', 'поды', 'подик', 'одноразку', 'одноразки',
    'вейп', 'вейпы', 'подоночки', 'хрос', 'расходник', 'расходники',
]

# Фразы для точного совпадения (целые фразы)
TRIGGER_PHRASES_EXACT = [
    'солевую жижу', 'жижу с никотином', 'жижу без никотина',
    'никотиновые жидкости', 'фруктовую жижу', 'сладкую жижу',
    'крепкую жижу', 'свежую жижу', 'жижу оптом', 'жижу недорого',
    'сменники', 'сменный картридж', 'картриджи на под',
    'оригинальные картриджи', 'оригинальные поды', '5 мини',
    'подонки', 'catswill', 'коты', 'котов', 'найс шот',
    'кэствил', 'хотспот', 'лабубу', 'злую', 'восток', 'карик',
    'тех уник', 'технический', 'политех', 'рик', 'rick', 'аркад',
    'монашку', 'злую монашку', 'вкусные одноразки', 'табачку',
    'оригинал', 'солевые вкусы', 'топ вкусы', 'новые вкусы',
    'популярные вкусы', 'кислые', 'кислый', 'кислую', 'сладкую',
    'вкусную', 'на востоке', 'на дк', 'на замерзоне', 'замерзон',
    'у церкви', 'на белой', 'доставкой', 'жижу куплю', 'карик куплю',
    'жижку куплю', 'картридж куплю', 'куплю жижу банк',
]

# Объединяем все в один список для проверки
ALL_TRIGGERS = TRIGGER_WORDS_EXACT + TRIGGER_PHRASES_EXACT

# Важные ключевые слова (если есть - сообщение считается важным)
IMPORTANT_KEYWORDS = ['восток', 'куплю восток', 'на востоке', 'ищу восток', 'срочно']

def contains_exact_trigger(text):
    """Проверяет, содержит ли сообщение точное совпадение триггера"""
    if not text:
        return False
    
    text_lower = text.lower()
    
    # Проверяем каждое слово/фразу
    for trigger in ALL_TRIGGERS:
        # Для коротких слов (до 4 букв) используем границы слова
        if len(trigger) <= 4:
            # Используем границы слова для точного совпадения
            pattern = r'\b' + re.escape(trigger) + r'\b'
            if re.search(pattern, text_lower):
                return True
        else:
            # Для длинных слов/фраз просто проверяем вхождение
            if trigger in text_lower:
                return True
    return False

def get_matched_triggers(text):
    """Возвращает список найденных триггеров в сообщении"""
    if not text:
        return []
    
    text_lower = text.lower()
    found = []
    
    for trigger in ALL_TRIGGERS:
        if len(trigger) <= 4:
            pattern = r'\b' + re.escape(trigger) + r'\b'
            if re.search(pattern, text_lower):
                found.append(trigger)
        else:
            if trigger in text_lower:
                found.append(trigger)
    
    return list(set(found))

def check_important_message(text):
    """Проверяет, является ли сообщение важным (есть куплю восток)"""
    if not text:
        return False
    text_lower = text.lower()
    # Важное сообщение если есть "куплю восток" или просто "восток" в контексте покупки
    if 'куплю восток' in text_lower or 'ищу восток' in text_lower:
        return True
    if 'восток' in text_lower and ('куплю' in text_lower or 'ищу' in text_lower):
        return True
    return False

def should_auto_reply(message_text):
    """Проверяет, нужно ли отправлять автоответ в ЛС"""
    if not message_text:
        return False
    text_lower = message_text.lower()
    
    # Автоответ отправляем если:
    # 1. Есть "куплю восток" или "ищу восток"
    if 'куплю восток' in text_lower or 'ищу восток' in text_lower:
        return True
    
    # 2. Есть "куплю жижу" или подобное без других слов
    # Проверяем что сообщение короткое и содержит только одно ключевое слово
    words = text_lower.split()
    
    # Если сообщение короткое (до 5 слов) и содержит ключевые слова
    if len(words) <= 5:
        key_triggers = ['жижу', 'жижку', 'жидкость', 'карик', 'картридж', 'под', 'поды']
        for trigger in key_triggers:
            if trigger in text_lower:
                # Проверяем что нет других слов (кроме "куплю" и самого триггера)
                important_words = ['куплю', 'ищу', trigger]
                other_words = [w for w in words if w not in important_words]
                if len(other_words) <= 1:  # Допускается одно дополнительное слово
                    return True
    
    return False
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

def send_notification(message_text, chat_name, sender_id, sender_username, sender_first_name, is_important=False, matched_triggers=None, auto_reply_sent=False):
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
    
    if auto_reply_sent:
        notification += f"✅ <b>Автоответ:</b> Отправлен в ЛС пользователю\n"
    
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

async def send_auto_reply_to_user(user_client, sender, original_message):
    """Отправляет автоответ пользователю в ЛС"""
    try:
        # Получаем пользователя
        user = await user_client.get_entity(sender.id)
        
        # Текст ответа
        reply_text = "Привет, могу продать! Напиши мне, что именно интересует."
        
        # Отправляем сообщение
        await user_client.send_message(user, reply_text, link_preview=False)
        
        # Пересылаем сообщение из канала
        try:
            parts = MESSAGE_TO_FORWARD.split('/')
            channel_username = parts[-2]
            message_id = int(parts[-1])
            
            channel = await user_client.get_entity(channel_username)
            message_to_forward = await user_client.get_messages(channel, ids=message_id)
            
            if message_to_forward:
                await user_client.forward_messages(user, message_to_forward, channel)
                logger.info(f"✅ Автоответ с пересылкой отправлен @{sender.username if sender.username else sender.id}")
            else:
                logger.info(f"✅ Автоответ (текст) отправлен @{sender.username if sender.username else sender.id}")
        except Exception as e:
            logger.error(f"Ошибка пересылки: {e}")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка отправки автоответа: {e}")
        return False

async def main():
    try:
        print("=" * 70)
        print("🤖 Telegram Монитор сообщений (Только беседы)")
        print("=" * 70)
        print(f"📱 Номер: {PHONE_NUMBER}")
        print(f"📝 Отслеживается {len(ALL_TRIGGERS)} фраз (точное совпадение)")
        print("🚫 Личные чаты игнорируются")
        print("=" * 70)
        
        # Проверяем, существует ли файл сессии
        if os.path.exists(f'{session_name}.session'):
            logger.info("Найдена сохраненная сессия, подключаемся...")
            await user_client.start(
                phone=PHONE_NUMBER,
                password=lambda: PASSWORD
            )
        else:
            logger.info("Сессия не найдена, требуется авторизация...")
            code = input("🔑 Введите код из Telegram: ")
            await user_client.start(
                phone=PHONE_NUMBER,
                code=code,
                password=lambda: PASSWORD
            )
        
        logger.info("✅ Подключение успешно!")
        
        me = await user_client.get_me()
        logger.info(f"👤 Аккаунт: {me.first_name} (@{me.username})")
        
        # Получаем список чатов
        dialogs = await user_client.get_dialogs()
        
        # Фильтруем только группы и каналы (исключаем личные чаты)
        groups_and_channels = [d for d in dialogs if d.is_group or d.is_channel]
        
        logger.info(f"📊 Найдено чатов: {len(dialogs)}")
        logger.info(f"📊 Из них бесед (группы/каналы): {len(groups_and_channels)}")
        logger.info("🚫 Личные чаты исключены из мониторинга")
        
        groups = sum(1 for d in groups_and_channels if d.is_group)
        channels = sum(1 for d in groups_and_channels if d.is_channel)
        logger.info(f"📈 Статистика: {groups} групп, {channels} каналов")
        
        @user_client.on(events.NewMessage)
        async def handler(event):
            try:
                # Пропускаем личные чаты (только группы и каналы)
                if event.is_private:
                    return
                
                message_text = event.message.text or event.message.caption or ""
                if not message_text:
                    return
                
                # Проверяем точное совпадение триггеров
                if contains_exact_trigger(message_text):
                    chat = await event.get_chat()
                    sender = await event.get_sender()
                    
                    # Определяем название чата
                    chat_name = chat.title if hasattr(chat, 'title') else "Unknown"
                    
                    sender_username = sender.username if hasattr(sender, 'username') else None
                    sender_first_name = sender.first_name if hasattr(sender, 'first_name') else "Unknown"
                    
                    # Проверяем важность
                    is_important = check_important_message(message_text)
                    
                    # Получаем список найденных триггеров
                    matched_triggers = get_matched_triggers(message_text)
                    
                    # Проверяем, нужно ли отправить автоответ в ЛС
                    auto_reply_sent = False
                    if should_auto_reply(message_text):
                        logger.info(f"🤖 Отправка автоответа в ЛС пользователю @{sender_username if sender_username else sender.id}")
                        auto_reply_sent = await send_auto_reply_to_user(user_client, sender, event.message)
                    
                    # Отправляем уведомление
                    send_notification(
                        message_text=message_text,
                        chat_name=chat_name,
                        sender_id=sender.id,
                        sender_username=sender_username,
                        sender_first_name=sender_first_name,
                        is_important=is_important,
                        matched_triggers=matched_triggers,
                        auto_reply_sent=auto_reply_sent
                    )
                    
                    triggers_str = ', '.join(matched_triggers[:3])
                    if is_important:
                        logger.info(f"🔴 ВАЖНОЕ [{triggers_str}] в {chat_name}")
                    else:
                        logger.info(f"📨 [{triggers_str}] в {chat_name}")
                    
            except Exception as e:
                logger.error(f"Ошибка обработки: {e}")
        
        logger.info("👀 Мониторинг запущен 24/7")
        logger.info("📌 Отслеживаются только сообщения в группах и каналах")
        await user_client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
    finally:
        await user_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
