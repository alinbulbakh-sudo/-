# Telegram AI Userbot (Claude)

ШІ-асистент підключений до вашого Telegram акаунту. Автоматично відповідає на вхідні особисті повідомлення за допомогою Claude.

## Швидкий старт

### 1. Отримайте ключі

- **Telegram API** → [my.telegram.org](https://my.telegram.org) → App configuration
- **Anthropic API** → [console.anthropic.com](https://console.anthropic.com)

### 2. Встановіть залежності

```bash
pip install -r requirements.txt
```

### 3. Налаштуйте змінні середовища

```bash
cp .env.example .env
# відредагуйте .env своїми ключами
```

### 4. Запустіть

```bash
# З .env файлом:
export $(cat .env | xargs) && python bot.py

# Або напряму:
TELEGRAM_API_ID=... TELEGRAM_API_HASH=... ANTHROPIC_API_KEY=... python bot.py
```

Перший запуск запитає номер телефону та код підтвердження. Сесія зберігається у файл `assistant_session.session`.

## Налаштування

| Змінна | Опис |
|--------|------|
| `TELEGRAM_API_ID` | API ID з my.telegram.org |
| `TELEGRAM_API_HASH` | API Hash з my.telegram.org |
| `ANTHROPIC_API_KEY` | Ключ Claude API |
| `SESSION_NAME` | Назва файлу сесії (за замовч. `assistant_session`) |
| `SYSTEM_PROMPT` | Роль агента — змініть під свою задачу |

## Whitelist (відповідь лише обраним)

Щоб агент відповідав лише конкретним людям, відредагуйте `bot.py`:

```python
ALLOWED_SENDERS = {123456789}  # Telegram user ID
```

## Увага

Userbot працює від імені вашого акаунту. Telegram може заблокувати акаунт за масовий спам. Використовуйте відповідально.
