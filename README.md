# SVS Aiogram Bot Template

A reusable, multilingual Telegram bot starter built with **aiogram 3.17** and Python 3.11+.

## Features

- Reply Keyboard and Inline Keyboard navigation.
- Uzbek, English, and Russian interface translations.
- Per-user language preference persisted in SQLite.
- /start, /menu, /language, /help, and /ping commands.
- Modular handlers, keyboard builders, and service layer.
- Async application lifecycle with polling.

## Requirements

- Python 3.11+
- Telegram bot token from https://t.me/BotFather

Python 3.11 or 3.12 is recommended for this pinned dependency set. Python 3.14 may require native build tools for older dependency versions.

## Quick start

    git clone https://github.com/SVS-studio/AiogramBotTemplate.git
    cd AiogramBotTemplate

    py -3.11 -m venv .venv
    .venv/Scripts/Activate.ps1

    python -m pip install --upgrade pip
    pip install -r requirements.txt

    Copy-Item .env.example .env

Set BOT_TOKEN in .env, then start the bot:

    python main.py

## Commands

| Command | Description |
|---|---|
| /start | Start the bot and show both menus |
| /menu | Show the main menu |
| /language | Select Uzbek, English, or Russian |
| /help | Show localized help |
| /ping | Check whether the bot is responding |

## Keyboard navigation

**Reply Keyboard** provides persistent shortcuts to Features, Settings, Profile, and About.

**Inline Keyboard** provides callback-based navigation, language selection, and a return to the main menu. Callback handlers are separated from message handlers.

## Project structure

    .
    ├── data/
    │   ├── config.py
    │   └── bot.sqlite3          # Created automatically; ignored by Git
    ├── handlers/
    │   ├── __init__.py
    │   ├── common.py            # Commands and menu callbacks
    │   └── echo.py              # /ping and fallback echo example
    ├── keyboards/
    │   ├── __init__.py
    │   └── menus.py             # Reply and inline keyboard builders
    ├── services/
    │   ├── __init__.py
    │   ├── i18n.py              # Uzbek, English, Russian translations
    │   └── user_preferences.py  # SQLite language preferences
    ├── .env.example
    ├── .gitignore
    ├── README.md
    ├── main.py
    └── requirements.txt

## Configuration

| Variable | Required | Default | Description |
|---|---:|---|---|
| BOT_TOKEN | Yes | — | Telegram bot token |
| ADMINS | No | empty | Comma-separated Telegram user IDs |
| LOG_LEVEL | No | INFO | Python logging level |
| DROP_PENDING_UPDATES | No | true | Discard queued updates when polling starts |

## Add a handler

Create a module in handlers/, define an aiogram.Router, then include it in handlers/__init__.py. Keep Telegram update handling in routers and business logic in services/.

## Development notes

- User language preferences are stored in data/bot.sqlite3; the database is created automatically.
- SQLite operations run via asyncio.to_thread so synchronous database calls do not block the event loop.
- The language catalog and supported locales are centralized in services/i18n.py.
- FSM uses in-memory storage by default. Use Redis or another persistent storage if FSM state must survive restarts or multiple workers.
- This is a starter template, not a complete production deployment. Add tests, rate limiting, error monitoring, and deployment-specific infrastructure as needed.

Never commit .env, database files, or expose your bot token.
