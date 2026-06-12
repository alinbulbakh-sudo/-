import os
import asyncio
from telethon import TelegramClient, events
from anthropic import Anthropic

# --- Config ---
API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
SESSION_NAME = os.environ.get("SESSION_NAME", "assistant_session")

# Whitelist of user IDs who can trigger the assistant (empty = everyone)
ALLOWED_SENDERS = set()  # e.g. {123456789, 987654321}

SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT", (
    "Ти — особистий ШІ-асистент. Відповідай стисло, по суті, дружньо. "
    "Мова відповіді — така ж, як мова вхідного повідомлення."
))

# --- State ---
# Keeps last N messages per chat for context
MAX_HISTORY = 10
chat_history: dict[int, list[dict]] = {}

anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


def get_reply(chat_id: int, user_text: str) -> str:
    history = chat_history.setdefault(chat_id, [])
    history.append({"role": "user", "content": user_text})
    if len(history) > MAX_HISTORY * 2:
        history[:] = history[-MAX_HISTORY * 2:]

    response = anthropic.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=history,
    )
    reply = response.content[0].text
    history.append({"role": "assistant", "content": reply})
    return reply


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # Skip group/channel messages unless mentioned
    if not event.is_private:
        return

    sender = await event.get_sender()
    if ALLOWED_SENDERS and sender.id not in ALLOWED_SENDERS:
        return

    text = event.raw_text.strip()
    if not text:
        return

    async with client.action(event.chat_id, "typing"):
        reply = await asyncio.to_thread(get_reply, event.chat_id, text)

    await event.respond(reply)


async def main():
    await client.start()
    me = await client.get_me()
    print(f"Userbot запущено як @{me.username} ({me.first_name})")
    print("Очікую повідомлення... (Ctrl+C для зупинки)")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
