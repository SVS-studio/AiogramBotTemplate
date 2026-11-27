# SVS Aiogram Bot Template

A clean, reusable Telegram bot starter built with **aiogram 3.17**.

> This repository is the maintained SVS version of the original `Nigmatullayev001/AiogramBotTemplate` starter. It keeps the lightweight polling approach while improving configuration, lifecycle management, handler organization, and developer documentation.

## Requirements

- Python 3.10+
- Telegram bot token from [@BotFather](https://t.me/BotFather)

## Quick start

```bash
git clone https://github.com/SVS-studio/AiogramBotTemplate.git
cd AiogramBotTemplate
python -m venv .venv
```

Activate the virtual environment, then install dependencies:

```bash
# Windows PowerShell
.venv\\Scripts\\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

On Windows, create `.env` manually or run `Copy-Item .env.example .env`.

Set `BOT_TOKEN` and optionally `ADMINS` in `.env`, then run:

```bash
python main.py
```

## Project structure

```text
.
├── data/
│   └── config.py          # Environment configuration and validation
├── handlers/
│   ├── __init__.py        # Root router
│   ├── common.py          # /start and /help
│   └── echo.py            # Example text handler
├── .env.example
├── .gitignore
├── main.py                # Application entry point and lifecycle
└── requirements.txt
```

## Configuration

| Variable | Required | Default | Description |
|---|---:|---|---|
| `BOT_TOKEN` | Yes | — | Telegram bot token |
| `ADMINS` | No | empty | Comma-separated Telegram user IDs, e.g. `123456,789012` |
| `LOG_LEVEL` | No | `INFO` | Python logging level |
| `DROP_PENDING_UPDATES` | No | `true` | Discard queued updates when polling starts |

Never commit `.env` or expose your bot token.

## Add a handler

Create a module in `handlers/`, define an `aiogram.Router`, then include it in `handlers/__init__.py`:

```python
from aiogram import Router

router = Router(name=__name__)

@router.message(Command("ping"))
async def ping(message: Message) -> None:
    await message.answer("pong")
```

Import `Command` and `Message` from `aiogram.filters` and `aiogram.types` respectively. Keep Telegram update handling in routers; put business logic in separate service modules as the project grows.

## Development notes

- Configuration is loaded once at startup and validated before polling.
- The bot and dispatcher are created inside the async application lifecycle.
- Routers are registered centrally.
- FSM uses in-memory storage by default; use Redis or another persistent storage if state must survive restarts or multiple workers.
- This is a starter template, not a complete production deployment. Add persistence, rate limiting, error monitoring, and tests according to the bot's requirements.

## License

Add a license before redistributing this template if you intend to publish it for reuse.
