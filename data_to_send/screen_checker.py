import subprocess
import asyncio
import requests

chat_id = ""

async def check_screens(chat_id: str):
    result = subprocess.run(['screen', '-ls'], stdout=subprocess.PIPE, text=True)

    if "No Sockets found" in result.stdout:
        message = "⚠️ No active screen sessions found!"
        await send_telegram_message(message, chat_id)
    else:
        sessions = result.stdout.strip().split('\n')
        active_screens = [line for line in sessions if "(Detached)" in line or "(Attached)" in line]

        for screen in active_screens:
            screen_info = screen.strip().split()
            session_id = screen_info[0]
            session_name = screen_info[1]
            status = "detached" if "(Detached)" in screen else "attached"

            message = f"🖥️ Screen session detected:\n\nSession: {session_name}\nID: {session_id}\nStatus: {status}"
            await send_telegram_message(message, chat_id)

        if not active_screens:
            message = "⚠️ No active screen sessions detected."
            await send_telegram_message(message, chat_id)


async def send_telegram_message(message: str, chat_id: str):
    url = "https://api.telegram.org/bot<your-telegram-bot-token>/sendMessage"
    params = {
        'chat_id': f'{chat_id}',
        'text': message
    }

    await asyncio.to_thread(requests.get, url, params=params)


async def main():
    await check_screens(chat_id)


if __name__ == '__main__':
    asyncio.run(main())
