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

# Специальные пользователи
SPECIAL_USERS = {
    'aahaahahah1': 'привет писька , я отвечу чуть позже',
}

# Названия бесед для специальной обработки
SPECIAL_CHATS = ['общага 1', 'общага1', 'Общага 1', 'Общага1']

# Сообщение для пересылки
MESSAGE_TO_FORWARD = 'https://t.me/lamavaape/42'

# Имя файла сессии
SESSION_NAME = 'user_session_permanent'
# ======================================

# ============= КЛЮЧЕВЫЕ СЛОВА =============
ACTION_WORDS = ['куплю', 'ищу', 'кто продаст', 'кто продаёт', 'кто продает']

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

OBSHAGA_TRIGGERS = [
    'кто может продать жижу', 'кто продаёт жижу', 'кто продает жижу',
    'кто может продать карик', 'кто продает карик',
    'кто может продать', 'продаёт жижу', 'продает жижу',
    'куплю жижку', 'нужен карик на хрос', 'куплю карик', 'куплю жижу',
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
    if not text:
        return []
    text_lower = text.lower()
    found = []
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
                logger.info(f"✅ Автоответ с пересылкой отправлен")
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
        print(f"📝 Условие: Действие + Товар")
        print("=" * 70)
        
<<<<<<< HEAD
        # Удаляем старую сессию если есть проблемы
        if os.path.exists(f'{SESSION_NAME}.session'):
            try:
                os.remove(f'{SESSION_NAME}.session')
                logger.info("Удалена старая сессия")
            except:
                pass
        if os.path.exists(f'{SESSION_NAME}.session-journal'):
            try:
                os.remove(f'{SESSION_NAME}.session-journal')
            except:
                pass
        
        # Подключаемся вручную
        await user_client.connect()
        
        # Отправляем запрос кода
        await user_client.send_code_request(PHONE_NUMBER)
        
        # Вводим код вручную
        code = input("🔑 Введите код из Telegram: ")
        
        # Пытаемся войти
        try:
            await user_client.sign_in(PHONE_NUMBER, code)
        except Exception as e:
            if "password" in str(e).lower() or "2FA" in str(e):
                # Автоматически вводим пароль
                await user_client.sign_in(password=PASSWORD)
                logger.info("✅ Пароль автоматически подставлен")
        
=======
        # Проверяем, есть ли файл сессии
        if os.path.exists(f'{SESSION_NAME}.session'):
            logger.info("Найдена сохраненная сессия, подключаемся...")
            await user_client.start(phone=PHONE_NUMBER)
        else:
            logger.info("Сессия не найдена, начинаем авторизацию...")
            await user_client.connect()
            await user_client.send_code_request(PHONE_NUMBER)
            code = input("🔑 Введите код из Telegram: ")
            await user_client.sign_in(PHONE_NUMBER, code)
            try:
                await user_client.sign_in(password=PASSWORD)
            except:
                pass
        
>>>>>>> d10077e6fa3b66cc32c2f625725693a9ef2067f3
        logger.info("✅ Подключение успешно!")
        
        me = await user_client.get_me()
        logger.info(f"👤 Аккаунт: {me.first_name} (@{me.username})")
<<<<<<< HEAD
=======
        logger.info(f"📁 Сессия: {SESSION_NAME}.session")
>>>>>>> d10077e6fa3b66cc32c2f625725693a9ef2067f3
        
        dialogs = await user_client.get_dialogs()
        groups_and_channels = [d for d in dialogs if d.is_group or d.is_channel]
        logger.info(f"📊 Найдено бесед: {len(groups_and_channels)}")
        
        @user_client.on(events.NewMessage)
        async def handler(event):
            try:
                sender = await event.get_sender()
                sender_username = sender.username if hasattr(sender, 'username') else None
                
                if sender_username and sender_username in SPECIAL_USERS:
                    await send_special_reply(user_client, sender, sender_username)
                    return
                
                if event.is_private:
                    return
                
                message_text = event.message.text or ""
                if hasattr(event.message, 'caption') and event.message.caption:
                    if not message_text:
                        message_text = event.message.caption
                
                if not message_text:
                    return
                
                chat = await event.get_chat()
                chat_name = chat.title if hasattr(chat, 'title') else "Unknown"
                
                if contains_action_word(message_text) and contains_product_word(message_text):
                    matched_products = get_matched_products(message_text)
                    is_important = check_important_message(message_text)
                    
                    auto_reply_sent = False
                    if should_auto_reply(message_text, chat_name):
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
                    
                    logger.info(f"📨 {chat_name}: {', '.join(matched_products[:3])}")
                    
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
