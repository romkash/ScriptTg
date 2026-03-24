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

# Специальные пользователи
SPECIAL_USERS = {
    'aahaahahah1': 'привет писька , я отвечу чуть позже',
}

# Названия бесед для специальной обработки
SPECIAL_CHATS = ['общага 1', 'общага1', 'Общага 1', 'Общага1']

# Сообщение для пересылки
MESSAGE_TO_FORWARD = 'https://t.me/lamavaape/42'

# Имя файла сессии (постоянное)
SESSION_NAME = 'user_session_permanent'
# ======================================

# ============= КЛЮЧЕВЫЕ СЛОВА =============
<<<<<<< HEAD
# Действия (должны быть обязательно)
ACTION_WORDS = ['куплю', 'ищу', 'кто продаст', 'кто продаёт', 'кто продает', 'продам']
=======
ACTION_WORDS = ['куплю', 'ищу', 'кто продаст', 'кто продаёт', 'кто продает']
>>>>>>> 97840d2 (add permanent session for railway)

PRODUCT_WORDS = [
    'жижу', 'жижку', 'жидкость', 'жижки',
    'карик', 'картридж', 'картриджи', 'испаритель', 'испарители',
    'под', 'поды', 'подик', 'одноразку', 'одноразки',
    'вейп', 'вейпы', 'подоночки', 'хрос', 'расходник', 'расходники',
    'солевую жижу', 'жижу с никотином', 'жижу без никотина',
    'никотиновые жидкости', 'фруктовую жижу', 'сладкую жижу',
    'крепкую жижу', 'свежую жижу', 'жижу оптом', 'жижу недорого',
    'сменники', 'сменный картридж', 'картриджи на под',
    'оригинальные картриджи', 'оригинальные поды', '5 мини',
    'подонки', 'catswill', 'коты', 'котов', 'найс шот',
    'кэствил', 'хотспот', 'лабубу', 'злую', 'восток',
    'тех уник', 'технический', 'политех', 'рик', 'rick', 'аркад',
    'монашку', 'злую монашку', 'вкусные одноразки', 'табачку',
    'оригинал', 'солевые вкусы', 'топ вкусы', 'новые вкусы',
    'популярные вкусы', 'кислые', 'кислый', 'кислую', 'сладкую',
    'вкусную', 'на востоке', 'на дк', 'на замерзоне', 'замерзон',
    'у церкви', 'на белой', 'доставкой', 'жижу куплю', 'карик куплю',
    'жижку куплю', 'картридж куплю', 'куплю жижу банк',
]

<<<<<<< HEAD
# Фразы для автоматического ответа в общаге
=======
>>>>>>> 97840d2 (add permanent session for railway)
OBSHAGA_TRIGGERS = [
    'кто может продать жижу', 'кто продаёт жижу', 'кто продает жижу',
    'кто может продать карик', 'кто продает карик',
    'кто может продать', 'продаёт жижу', 'продает жижу',
<<<<<<< HEAD
    'нужна жижа', 'нужен карик', 'жижа нужна', 'карик нужен',
=======
    'куплю жижку', 'нужен карик на хрос', 'куплю карик', 'куплю жижу',
>>>>>>> 97840d2 (add permanent session for railway)
]

def contains_action_word(text):
    if not text:
        return False
    text_lower = text.lower()
    for action in ACTION_WORDS:
        if action in text_lower:
            return True
    return False

def contains_product_word(text):
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
<<<<<<< HEAD
    """Возвращает список найденных товаров в сообщении"""
=======
>>>>>>> 97840d2 (add permanent session for railway)
    if not text:
        return []
    text_lower = text.lower()
    found = []
<<<<<<< HEAD
    
=======
>>>>>>> 97840d2 (add permanent session for railway)
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
    if not text:
        return False
    text_lower = text.lower()
    for trigger in OBSHAGA_TRIGGERS:
        if trigger in text_lower:
            return True
    return False

def check_important_message(text):
    if not text:
        return False
    text_lower = text.lower()
    if 'куплю восток' in text_lower or 'ищу восток' in text_lower:
        return True
    if 'восток' in text_lower and ('куплю' in text_lower or 'ищу' in text_lower):
        return True
    return False

def should_auto_reply(message_text, chat_name):
    if not message_text:
        return False
    text_lower = message_text.lower()
    chat_lower = chat_name.lower() if chat_name else ""
    
<<<<<<< HEAD
    # Если это беседа "общага 1" и есть специальные триггеры
=======
>>>>>>> 97840d2 (add permanent session for railway)
    if any(chat.lower() in chat_lower for chat in ['общага 1', 'общага1']):
        if check_obshaga_trigger(message_text):
            return True
    
    if 'куплю восток' in text_lower or 'ищу восток' in text_lower:
        return True
    
    if 'восток' in text_lower:
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

# Создаем клиент
user_client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def get_user_link(username, user_id, first_name):
    if username:
        return f"https://t.me/{username}"
    else:
        return f"tg://user?id={user_id}"

def send_notification(message_text, chat_name, sender_id, sender_username, sender_first_name, is_important=False, matched_products=None, auto_reply_sent=False):
    if matched_products is None:
        matched_products = []
    
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
    try:
        user = await user_client.get_entity(sender.id)
        
        chat_lower = chat_name.lower() if chat_name else ""
        
        if any(chat.lower() in chat_lower for chat in ['общага 1', 'общага1']):
            reply_text = "Привет! Видел твое сообщение в общаге. Могу помочь с покупкой! Напиши, что именно интересует."
        elif 'восток' in original_message.lower():
            reply_text = "Привет! По поводу Востока - могу предложить хорошие варианты. Напиши, что конкретно ищешь."
        else:
            reply_text = "Привет, могу продать! Напиши мне, что именно интересует."
        
        await user_client.send_message(user, reply_text, link_preview=False)
        
        try:
            parts = MESSAGE_TO_FORWARD.split('/')
            channel_username = parts[-2]
            message_id = int(parts[-1])
            
            channel = await user_client.get_entity(channel_username)
            message_to_forward = await user_client.get_messages(channel, ids=message_id)
            
            if message_to_forward:
                await user_client.forward_messages(user, message_to_forward, channel)
<<<<<<< HEAD
                logger.info(f"✅ Автоответ с пересылкой отправлен @{sender.username if sender.username else sender.id}")
=======
                logger.info(f"✅ Автоответ с пересылкой отправлен")
>>>>>>> 97840d2 (add permanent session for railway)
        except Exception as e:
            logger.error(f"Ошибка пересылки: {e}")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        return False

async def send_special_reply(user_client, sender, username):
    try:
        user = await user_client.get_entity(sender.id)
        reply_text = SPECIAL_USERS.get(username, None)
        
        if reply_text:
            await user_client.send_message(user, reply_text, link_preview=False)
            logger.info(f"✅ Специальный ответ отправлен @{username}")
            return True
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
    return False

async def main():
    try:
        print("=" * 70)
        print("🤖 Telegram Монитор сообщений")
        print("=" * 70)
        print(f"📱 Номер: {PHONE_NUMBER}")
<<<<<<< HEAD
        print(f"📝 Условие: Действие (куплю/ищу/кто продаст) + Товар")
        print(f"🏠 Специальные беседы: {', '.join(SPECIAL_CHATS)}")
        print(f"👤 Специальные пользователи: {', '.join(SPECIAL_USERS.keys())}")
        print("🚫 Личные чаты игнорируются")
        print("=" * 70)
        
        def get_code():
            return input("🔑 Введите код из Telegram: ")
        
        await user_client.start(
            phone=PHONE_NUMBER,
            code_callback=get_code,
            password=lambda: PASSWORD
        )
=======
        print(f"📝 Условие: Действие + Товар")
        print("=" * 70)
        
        # Удаляем старые файлы сессии, если они есть
        session_files = [f for f in os.listdir('.') if f.startswith('user_session') and f.endswith(('.session', '.session-journal'))]
        for f in session_files:
            try:
                os.remove(f)
                logger.info(f"Удален старый файл сессии: {f}")
            except:
                pass
        
        # Подключаемся
        await user_client.connect()
        
        # Отправляем запрос на код
        await user_client.send_code_request(PHONE_NUMBER)
        
        print()
        print("📲 Код отправлен в Telegram!")
        print()
        
        # Запрашиваем код
        code = input("🔑 Введите код из Telegram: ")
        
        # Пытаемся войти с кодом
        try:
            await user_client.sign_in(PHONE_NUMBER, code)
        except Exception as e:
            if "password" in str(e).lower() or "Two-steps" in str(e):
                logger.info("Требуется пароль 2FA, вводим автоматически...")
                await user_client.sign_in(password=PASSWORD)
>>>>>>> 97840d2 (add permanent session for railway)
        
        logger.info("✅ Подключение успешно!")
        
        me = await user_client.get_me()
        logger.info(f"👤 Аккаунт: {me.first_name} (@{me.username})")
        logger.info(f"📁 Сессия сохранена в: {SESSION_NAME}.session")
        
        dialogs = await user_client.get_dialogs()
        groups_and_channels = [d for d in dialogs if d.is_group or d.is_channel]
        
        logger.info(f"📊 Найдено чатов: {len(dialogs)}")
        logger.info(f"📊 Из них бесед: {len(groups_and_channels)}")
        
<<<<<<< HEAD
        special_found = []
        for d in groups_and_channels:
            if d.name and any(chat.lower() in d.name.lower() for chat in SPECIAL_CHATS):
                special_found.append(d.name)
        
        if special_found:
            logger.info(f"🏠 Найдены специальные беседы: {', '.join(special_found)}")
        
=======
>>>>>>> 97840d2 (add permanent session for railway)
        @user_client.on(events.NewMessage)
        async def handler(event):
            try:
                sender = await event.get_sender()
                sender_username = sender.username if hasattr(sender, 'username') else None
                
<<<<<<< HEAD
                # Проверяем специальных пользователей
                if sender_username and sender_username in SPECIAL_USERS:
                    logger.info(f"👤 Специальный пользователь @{sender_username}")
                    await send_special_reply(user_client, sender, sender_username)
                    return
                
                # Пропускаем личные чаты
=======
                # Специальные пользователи
                if sender_username and sender_username in SPECIAL_USERS:
                    await send_special_reply(user_client, sender, sender_username)
                    return
                
                # Только группы
>>>>>>> 97840d2 (add permanent session for railway)
                if event.is_private:
                    return
                
                message_text = event.message.text or event.message.caption or ""
                if not message_text:
                    return
                
                chat = await event.get_chat()
                chat_name = chat.title if hasattr(chat, 'title') else "Unknown"
                
                has_action = contains_action_word(message_text)
                has_product = contains_product_word(message_text)
                
                if has_action and has_product:
<<<<<<< HEAD
                    sender_first_name = sender.first_name if hasattr(sender, 'first_name') else "Unknown"
                    is_important = check_important_message(message_text)
                    matched_products = get_matched_products(message_text)
                    
                    auto_reply_sent = False
                    if should_auto_reply(message_text, chat_name):
                        logger.info(f"🤖 Автоответ @{sender_username if sender_username else sender.id}")
=======
                    matched_products = get_matched_products(message_text)
                    is_important = check_important_message(message_text)
                    
                    auto_reply_sent = False
                    if should_auto_reply(message_text, chat_name):
>>>>>>> 97840d2 (add permanent session for railway)
                        auto_reply_sent = await send_auto_reply_to_user(user_client, sender, message_text, chat_name)
                    
                    send_notification(
                        message_text=message_text,
                        chat_name=chat_name,
                        sender_id=sender.id,
                        sender_username=sender_username,
                        sender_first_name=sender.first_name if hasattr(sender, 'first_name') else "Unknown",
                        is_important=is_important,
                        matched_products=matched_products,
                        auto_reply_sent=auto_reply_sent
                    )
                    
<<<<<<< HEAD
                    products_str = ', '.join(matched_products[:3])
                    logger.info(f"📨 [{products_str}] в {chat_name}")
=======
                    logger.info(f"📨 {chat_name}: {', '.join(matched_products[:3])}")
>>>>>>> 97840d2 (add permanent session for railway)
                    
            except Exception as e:
                logger.error(f"Ошибка: {e}")
        
<<<<<<< HEAD
        logger.info("👀 Мониторинг запущен 24/7")
=======
        logger.info("👀 Мониторинг запущен!")
        logger.info("💡 Для остановки нажмите Ctrl+C")
>>>>>>> 97840d2 (add permanent session for railway)
        await user_client.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
    finally:
        await user_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())