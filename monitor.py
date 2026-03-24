import asyncio
from telethon import TelegramClient, events
import requests
import logging
import re
import os
from datetime import datetime

# ============= ВАШИ ДАННЫЕ =============
API_ID = 32156450
API_HASH = '969799d773d7e9095b76f50a693f9e31'
BOT_TOKEN = '7667185968:AAFlHcZP4tTVyGsmAddRbIMzKa5wVNOOPHs'
CHAT_ID = '7213969441'
PHONE_NUMBER = '+375298206967'
PASSWORD = 'ngrief12'

# Специальные пользователи с индивидуальными ответами
SPECIAL_USERS = {
    'aahaahahah1': 'привет писька , я отвечу чуть позже',
    # Добавляйте других пользователей сюда
}

# Названия бесед для специальной обработки
<<<<<<< Updated upstream
SPECIAL_CHATS = ['общага 1', 'общага1', 'Общага 1']
=======
SPECIAL_CHATS = ['общага 1', 'общага1', 'Общага 1', 'Общага1']
>>>>>>> Stashed changes

# Сообщение для пересылки
MESSAGE_TO_FORWARD = 'https://t.me/lamavaape/42'
# ======================================

<<<<<<< Updated upstream
# ============= ТОЧНОЕ СОВПАДЕНИЕ ДЛЯ ТРИГГЕРОВ =============
TRIGGER_WORDS_EXACT = [
    'куплю жижу', 'ищу жижку', 'жижу', 'жижку', 'жидкость', 'жижки',
    'карик', 'картридж', 'картриджи', 'испаритель', 'испарители',
    'под', 'поды', 'подик', 'одноразку', 'одноразки',
    'вейп', 'вейпы', 'подоночки', 'хрос', 'расходник', 'расходники',
]

TRIGGER_PHRASES_EXACT = [
=======
# ============= КЛЮЧЕВЫЕ СЛОВА =============
# Действия (должны быть обязательно)
ACTION_WORDS = ['куплю', 'ищу', 'кто продаст', 'кто продаёт', 'кто продает']

# Товары (должно быть хотя бы одно)
PRODUCT_WORDS = [
    'жижу', 'жижку', 'жидкость', 'жижки',
    'карик', 'картридж', 'картриджи', 'испаритель', 'испарители',
    'под', 'поды', 'подик', 'одноразку', 'одноразки',
    'вейп', 'вейпы', 'подоночки', 'хрос', 'расходник', 'расходники',
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
# Фразы для автоматического ответа в общаге
OBSHAGA_TRIGGERS = [
    'кто может продать жижу', 'кто продаёт жижу?', 'кто продает жижу',
    'кто может продать карик', 'куплю жижу', 'кто продает карик',
    'кто может продать жижу', 'ищу кто продаёт жижу', 'кто продает жижу?',
    'нужна жижа', 'нужен карик', 'жижа нужна', 'карик нужен',
]

# Объединяем все в один список
ALL_TRIGGERS = TRIGGER_WORDS_EXACT + TRIGGER_PHRASES_EXACT

IMPORTANT_KEYWORDS = ['восток', 'куплю восток', 'куплю жижу', 'куплю карик']

def contains_exact_trigger(text):
    """Проверяет, содержит ли сообщение точное совпадение триггера"""
    if not text:
        return False
    
    text_lower = text.lower()
    
    for trigger in ALL_TRIGGERS:
        if len(trigger) <= 4:
            pattern = r'\b' + re.escape(trigger) + r'\b'
            if re.search(pattern, text_lower):
                return True
        else:
            if trigger in text_lower:
                return True
    return False

def check_obshaga_trigger(text):
    """Проверяет, есть ли триггер для общаги"""
    if not text:
        return False
    text_lower = text.lower()
    for trigger in OBSHAGA_TRIGGERS:
        if trigger in text_lower:
            return True
    return False

def get_matched_triggers(text):
    """Возвращает список найденных триггеров в сообщении"""
=======
# Фразы для автоматического ответа в общаге (без проверки на действие, так как действие уже есть)
OBSHAGA_TRIGGERS = [
    'кто может продать жижу', 'кто продаёт жижу', 'кто продает жижу',
    'кто может продать карик', 'кто продает карик',
    'кто может продать', 'продаёт жижу', 'продает жижу',
    'нужна жижа', 'нужен карик', 'куплю жижу', 'карик нужен', 'куплю карик',
]

# Важные ключевые слова
IMPORTANT_KEYWORDS = ['восток', 'куплю восток', 'на востоке', 'ищу восток', 'срочно']

def contains_action_word(text):
    """Проверяет наличие слова действия (куплю/ищу/кто продаст)"""
    if not text:
        return False
    text_lower = text.lower()
    for action in ACTION_WORDS:
        if action in text_lower:
            return True
    return False

def contains_product_word(text):
    """Проверяет наличие слова товара"""
    if not text:
        return False
    text_lower = text.lower()
    for product in PRODUCT_WORDS:
        if len(product) <= 4:
            pattern = r'\b' + re.escape(product) + r'\b'
            if re.search(pattern, text_lower):
                return True
        else:
            if product in text_lower:
                return True
    return False

def get_matched_products(text):
    """Возвращает список найденных товаров в сообщении"""
>>>>>>> Stashed changes
    if not text:
        return []
    
    text_lower = text.lower()
    found = []
    
<<<<<<< Updated upstream
    for trigger in ALL_TRIGGERS:
        if len(trigger) <= 4:
            pattern = r'\b' + re.escape(trigger) + r'\b'
            if re.search(pattern, text_lower):
                found.append(trigger)
        else:
            if trigger in text_lower:
                found.append(trigger)
    
    return list(set(found))

=======
    for product in PRODUCT_WORDS:
        if len(product) <= 4:
            pattern = r'\b' + re.escape(product) + r'\b'
            if re.search(pattern, text_lower):
                found.append(product)
        else:
            if product in text_lower:
                found.append(product)
    
    return list(set(found))

def check_obshaga_trigger(text):
    """Проверяет, есть ли триггер для общаги"""
    if not text:
        return False
    text_lower = text.lower()
    for trigger in OBSHAGA_TRIGGERS:
        if trigger in text_lower:
            return True
    return False

>>>>>>> Stashed changes
def check_important_message(text):
    """Проверяет, является ли сообщение важным"""
    if not text:
        return False
    text_lower = text.lower()
    if 'куплю восток' in text_lower or 'ищу восток' in text_lower:
        return True
    if 'восток' in text_lower and ('куплю' in text_lower or 'ищу' in text_lower):
        return True
    return False

def should_auto_reply(message_text, chat_name):
    """Проверяет, нужно ли отправлять автоответ в ЛС"""
    if not message_text:
        return False
    text_lower = message_text.lower()
    chat_lower = chat_name.lower() if chat_name else ""
    
    # Если это беседа "общага 1" и есть специальные триггеры
<<<<<<< Updated upstream
    if any(chat in chat_lower for chat in ['общага 1', 'общага1']):
=======
    if any(chat.lower() in chat_lower for chat in ['общага 1', 'общага1']):
>>>>>>> Stashed changes
        if check_obshaga_trigger(message_text):
            return True
    
    # Если есть "куплю восток" или "ищу восток"
    if 'куплю восток' in text_lower or 'ищу восток' in text_lower:
        return True
    
    # Если есть слово "восток" в сообщении
    if 'восток' in text_lower:
        return True
    
    # Короткие сообщения с покупкой
    words = text_lower.split()
    if len(words) <= 5:
        key_triggers = ['жижу', 'жижку', 'жидкость', 'карик', 'картридж', 'под', 'поды']
        for trigger in key_triggers:
            if trigger in text_lower:
                important_words = ['куплю', 'ищу', trigger]
                other_words = [w for w in words if w not in important_words]
                if len(other_words) <= 1:
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

# Создаем имя сессии с временной меткой
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
session_name = f'user_session_{PHONE_NUMBER[-8:]}_{timestamp}'

# Создаем клиент
user_client = TelegramClient(session_name, API_ID, API_HASH)

def get_user_link(username, user_id, first_name):
    if username:
        return f"https://t.me/{username}"
    else:
        return f"tg://user?id={user_id}"

<<<<<<< Updated upstream
def send_notification(message_text, chat_name, sender_id, sender_username, sender_first_name, is_important=False, matched_triggers=None, auto_reply_sent=False):
    if matched_triggers is None:
        matched_triggers = []
=======
def send_notification(message_text, chat_name, sender_id, sender_username, sender_first_name, is_important=False, matched_products=None, auto_reply_sent=False):
    if matched_products is None:
        matched_products = []
>>>>>>> Stashed changes
    
    if is_important:
        title_emoji = "🔴🔴🔴 ВАЖНО 🔴🔴🔴"
        border = "🔴" * 25
    else:
        title_emoji = "🔔 НАЙДЕНО"
        border = "━" * 25
    
    user_link = get_user_link(sender_username, sender_id, sender_first_name)
    
    products_text = ""
    if matched_products:
        products_text = f"🎯 <b>Товар:</b> {', '.join(matched_products[:5])}\n"
    
    notification = (
        f"<b>{title_emoji}</b>\n"
        f"{border}\n"
        f"📱 <b>Чат:</b> {chat_name}\n"
        f"👤 <b>Пользователь:</b> <a href='{user_link}'>{sender_first_name}</a>\n"
        f"🆔 <b>ID:</b> <code>{sender_id}</code>\n"
        f"{products_text}"
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

async def send_auto_reply_to_user(user_client, sender, original_message, chat_name):
    """Отправляет автоответ пользователю в ЛС"""
    try:
        user = await user_client.get_entity(sender.id)
        
        # Разный текст для разных ситуаций
        chat_lower = chat_name.lower() if chat_name else ""
        
<<<<<<< Updated upstream
        if any(chat in chat_lower for chat in ['общага 1', 'общага1']):
=======
        if any(chat.lower() in chat_lower for chat in ['общага 1', 'общага1']):
>>>>>>> Stashed changes
            reply_text = "Привет! Видел твое сообщение в общаге. Могу помочь с покупкой! Напиши, что именно интересует."
        elif 'восток' in original_message.lower():
            reply_text = "Привет! По поводу Востока - могу предложить хорошие варианты. Напиши, что конкретно ищешь."
        else:
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
<<<<<<< Updated upstream
=======

async def send_special_reply(user_client, sender, username):
    """Отправляет специальный ответ для определенных пользователей"""
    try:
        user = await user_client.get_entity(sender.id)
        reply_text = SPECIAL_USERS.get(username, None)
        
        if reply_text:
            await user_client.send_message(user, reply_text, link_preview=False)
            logger.info(f"✅ Специальный ответ отправлен @{username}")
            return True
    except Exception as e:
        logger.error(f"❌ Ошибка отправки специального ответа @{username}: {e}")
    return False
>>>>>>> Stashed changes

async def main():
    try:
        print("=" * 70)
        print("🤖 Telegram Монитор сообщений (Только беседы)")
        print("=" * 70)
        print(f"📱 Номер: {PHONE_NUMBER}")
<<<<<<< Updated upstream
        print(f"📝 Отслеживается {len(ALL_TRIGGERS)} фраз (точное совпадение)")
        print(f"🏠 Специальные беседы: {', '.join(SPECIAL_CHATS)}")
        print("🚫 Личные чаты игнорируются")
        print("=" * 70)
        
        # Удаляем старую сессию если она есть и вызывает ошибку
        if os.path.exists(f'{session_name}.session'):
            logger.info("Удаляем старую сессию для создания новой...")
            os.remove(f'{session_name}.session')
            if os.path.exists(f'{session_name}.session-journal'):
                os.remove(f'{session_name}.session-journal')
        
        # Создаем новую сессию
        logger.info("Создаем новую сессию...")
        code = input("🔑 Введите код из Telegram: ")
        await user_client.start(
            phone=PHONE_NUMBER,
            code=code,
=======
        print(f"📝 Условие: Действие (куплю/ищу/кто продаст) + Товар")
        print(f"🏠 Специальные беседы: {', '.join(SPECIAL_CHATS)}")
        print(f"👤 Специальные пользователи: {', '.join(SPECIAL_USERS.keys())}")
        print(f"📁 Файл сессии: {session_name}.session")
        print("🚫 Личные чаты игнорируются")
        print("=" * 70)
        
        # Функция для получения кода
        def get_code():
            return input("🔑 Введите код из Telegram: ")
        
        # Подключаемся
        await user_client.start(
            phone=PHONE_NUMBER,
            code_callback=get_code,
>>>>>>> Stashed changes
            password=lambda: PASSWORD
        )
        
        logger.info("✅ Подключение успешно!")
        
        me = await user_client.get_me()
        logger.info(f"👤 Аккаунт: {me.first_name} (@{me.username})")
        
        # Получаем список чатов
        dialogs = await user_client.get_dialogs()
        
        # Фильтруем только группы и каналы
        groups_and_channels = [d for d in dialogs if d.is_group or d.is_channel]
        
        logger.info(f"📊 Найдено чатов: {len(dialogs)}")
        logger.info(f"📊 Из них бесед (группы/каналы): {len(groups_and_channels)}")
        
        # Показываем специальные беседы
        special_found = []
        for d in groups_and_channels:
            if d.name and any(chat.lower() in d.name.lower() for chat in SPECIAL_CHATS):
                special_found.append(d.name)
        
        if special_found:
            logger.info(f"🏠 Найдены специальные беседы: {', '.join(special_found)}")
        
        groups = sum(1 for d in groups_and_channels if d.is_group)
        channels = sum(1 for d in groups_and_channels if d.is_channel)
        logger.info(f"📈 Статистика: {groups} групп, {channels} каналов")
        
        @user_client.on(events.NewMessage)
        async def handler(event):
            try:
<<<<<<< Updated upstream
                # Пропускаем личные чаты
=======
                # Получаем информацию об отправителе
                sender = await event.get_sender()
                sender_username = sender.username if hasattr(sender, 'username') else None
                
                # Проверяем специальных пользователей (даже в личных чатах)
                if sender_username and sender_username in SPECIAL_USERS:
                    logger.info(f"👤 Специальный пользователь @{sender_username} написал сообщение")
                    await send_special_reply(user_client, sender, sender_username)
                    return  # Не обрабатываем дальше, чтобы не дублировать
                
                # Пропускаем личные чаты для остальных
>>>>>>> Stashed changes
                if event.is_private:
                    return
                
                message_text = event.message.text or event.message.caption or ""
                if not message_text:
                    return
                
                # Получаем информацию о чате
                chat = await event.get_chat()
                chat_name = chat.title if hasattr(chat, 'title') else "Unknown"
                
<<<<<<< Updated upstream
                # Проверяем точное совпадение триггеров
                if contains_exact_trigger(message_text):
                    sender = await event.get_sender()
                    
                    sender_username = sender.username if hasattr(sender, 'username') else None
=======
                # ОСНОВНОЕ УСЛОВИЕ: должно быть действие И товар
                has_action = contains_action_word(message_text)
                has_product = contains_product_word(message_text)
                
                if has_action and has_product:
>>>>>>> Stashed changes
                    sender_first_name = sender.first_name if hasattr(sender, 'first_name') else "Unknown"
                    
                    # Проверяем важность
                    is_important = check_important_message(message_text)
                    
<<<<<<< Updated upstream
                    # Получаем список найденных триггеров
                    matched_triggers = get_matched_triggers(message_text)
=======
                    # Получаем список найденных товаров
                    matched_products = get_matched_products(message_text)
>>>>>>> Stashed changes
                    
                    # Проверяем, нужно ли отправить автоответ в ЛС
                    auto_reply_sent = False
                    if should_auto_reply(message_text, chat_name):
                        logger.info(f"🤖 Отправка автоответа в ЛС пользователю @{sender_username if sender_username else sender.id} (чат: {chat_name})")
                        auto_reply_sent = await send_auto_reply_to_user(user_client, sender, message_text, chat_name)
                    
                    # Отправляем уведомление
                    send_notification(
                        message_text=message_text,
                        chat_name=chat_name,
                        sender_id=sender.id,
                        sender_username=sender_username,
                        sender_first_name=sender_first_name,
                        is_important=is_important,
<<<<<<< Updated upstream
                        matched_triggers=matched_triggers,
                        auto_reply_sent=auto_reply_sent
                    )
                    
                    triggers_str = ', '.join(matched_triggers[:3])
=======
                        matched_products=matched_products,
                        auto_reply_sent=auto_reply_sent
                    )
                    
                    products_str = ', '.join(matched_products[:3])
>>>>>>> Stashed changes
                    if is_important:
                        logger.info(f"🔴 ВАЖНОЕ [{products_str}] в {chat_name}")
                    else:
                        logger.info(f"📨 [{products_str}] в {chat_name}")
                    
            except Exception as e:
                logger.error(f"Ошибка обработки: {e}")
        
        logger.info("👀 Мониторинг запущен 24/7")
<<<<<<< Updated upstream
        logger.info("📌 Отслеживаются только сообщения в группах и каналах")
=======
        logger.info("📌 Условие: сообщение должно содержать действие (куплю/ищу/кто продаст) И товар")
        logger.info("👤 Специальные пользователи получают индивидуальные ответы")
>>>>>>> Stashed changes
        await user_client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
    finally:
        await user_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
