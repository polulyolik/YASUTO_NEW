import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from commands import register_commands
from utils.background import background_match_checker

# Импорт автопоиска стратегий для использования в фоновых задачах или командах
from strategies import STRATEGIES

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not API_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN not set")

async def main():
    # Логирование с форматированием + запись в файл и консоль
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("bot.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    logging.info("=== ПРОВЕРКА ЛОГИРОВАНИЯ: бот стартует ===")  # <-- Проверка

    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Вызов без передачи strategies!
    register_commands(dp)

    # Исправлено: вызываем без лишних аргументов
    asyncio.create_task(background_match_checker(bot))

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
