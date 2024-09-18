import subprocess
import asyncio
import requests

chat_id = ""


async def check_containers(chat_id: str):
    stopped_containers = []

    result = subprocess.run(['docker', 'ps', '-a', '--format', '{{.ID}} {{.Names}} {{.Status}}'],
                            stdout=subprocess.PIPE, text=True)

    containers = result.stdout.strip().split('\n')
    for container in containers:
        container_info = container.split()

        container_id = container_info[0]
        container_name = container_info[1]
        container_status = container_info[2]

        if 'Exited' in container_status and container_id not in stopped_containers:
            stopped_containers.append(container_id)

            message = f"⚠️ Container stopped!\n\nName: {container_name}\nID: {container_id}"
            await send_telegram_message(message, chat_id)

            await asyncio.sleep(120)

            subprocess.run(["./docker_restarter.sh", container_id])

            await asyncio.sleep(20)

            message = f"✅ Container successfully restarted!\n\nName: {container_name}\nID: {container_id}"
            await send_telegram_message(message, chat_id)


async def send_telegram_message(message: str, chat_id: str):
    url = "https://api.telegram.org/bot7342157923:AAFBt3dMPnXOUQfhP1pP1TTcduiPQTwi7yc/sendMessage"
    params = {
        'chat_id': f'{chat_id}',
        'text': message
    }

    await asyncio.to_thread(requests.get, url, params=params)


async def main():
    await check_containers(chat_id)


if __name__ == '__main__':
    asyncio.run(main())
