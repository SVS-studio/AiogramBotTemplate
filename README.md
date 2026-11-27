# IELTS Prep AI Telegram Companion

A Telegram companion for the IELTS Prep AI platform, built with **aiogram 3.17** and Python 3.11+. The bot uses the platform's Django API and existing VERIX/Gemini service; it does not duplicate IELTS business logic.

## Features

- Reply Keyboard and Inline Keyboard navigation.
- Uzbek, English, and Russian interface translations.
- Per-user language and notification preferences persisted in SQLite.
- Referral deep links with unique registration tracking and referral counts.
- Referral sharing through Telegram's share URL.
- Secure one-time account linking to an IELTS Prep AI account.
- VERIX AI chat routed through the existing Django/Gemini service.
- IELTS profile, plan, band scores, streak, and completed-test summary.
- Commands: /start, /menu, /settings, /language, /referral, /help, /ping, /link, /profile, and /verix.
- Modular handlers, keyboard builders, and service layer.
- Async application lifecycle with polling.

## Requirements

- Python 3.11+
- Telegram bot token from https://t.me/BotFather

Python 3.11 or 3.12 is recommended for this pinned dependency set. Python 3.14 may require native build tools for older dependency versions.

## Quick start (PowerShell)

    git clone https://github.com/SVS-studio/AiogramBotTemplate.git
    cd AiogramBotTemplate

    py -3.11 -m venv .venv
    .venv/Scripts/Activate.ps1

    python -m pip install --upgrade pip
    pip install -r requirements.txt

    Copy-Item .env.example .env

Set BOT_TOKEN, IELTS_API_BASE_URL, and IELTS_BOT_INTERNAL_SECRET in .env. The internal secret must match TELEGRAM_BOT_INTERNAL_SECRET in the Django backend .env. Then start the bot:

    python main.py

## Commands

| Command | Description |
|---|---|
| /start | Start the bot; accepts referral payloads |
| /menu | Show the main menu |
| /settings | Open user settings |
| /language | Select Uzbek, English, or Russian |
| /referral | Show your referral link and invite count |
| /help | Show localized help |
| /ping | Check whether the bot is responding |
| /link | Show account-linking instructions |
| /profile | Show platform profile and IELTS progress |
| /verix | Ask VERIX an IELTS question |

## IELTS Prep AI integration

1. Start the Django backend and apply migrations.
2. Configure `TELEGRAM_BOT_INTERNAL_SECRET` in the backend `.env`.
3. Configure the exact same value as `IELTS_BOT_INTERNAL_SECRET` in the bot `.env`.
4. Set `TELEGRAM_BOT_USERNAME` in the backend `.env` to this bot's username.
5. In the platform, open Profile → Connect Telegram and open the generated deep link.
6. Use `/profile` to view platform data. Send a normal text message or use `/verix` to talk to the existing VERIX service.

The bot uses long polling. Do not configure Telegram webhook delivery for this same bot token while polling is active.

## Referral tracking

Each user gets a deep link in this format:

    https://t.me/<bot_username>?start=ref_<telegram_user_id>

When a new user starts the bot with this payload:
- The bot checks that the referrer is already registered.
- Self-referrals are rejected.
- The new Telegram user is recorded only once.
- The referrer's count increases only for a newly registered user.
- Repeated /start calls do not create duplicate referrals.

Referral counts are tracked from the time this feature is deployed. Existing users who were never stored in the previous database may need to run /start once after the update before they can be recognized as referrers.

This template tracks referral registrations only. It does not implement reward payouts, points, or fraud-proof identity checks.

## Settings

- Language preference: Uzbek, English, or Russian.
- Notifications preference: enabled or disabled.
- Both preferences are stored per Telegram user in SQLite.

The notification switch stores the user's preference. A scheduler or notification-producing feature must check this setting before sending notifications; no background notification campaign is included in this starter.

## Keyboard navigation

**Reply Keyboard** provides persistent shortcuts to Features, Settings, Profile, Referrals, and About.

**Inline Keyboard** provides callback-based navigation, language selection, notification preferences, referral sharing, and a return to the main menu.

## Project structure

    .
    ├── .github/
    │   └── workflows/tests.yml
    ├── tests/
    │   └── test_user_preferences.py
    ├── data/
    │   ├── config.py
    │   └── bot.sqlite3
    ├── handlers/
    │   ├── __init__.py
    │   ├── common.py
    │   ├── companion.py
    │   └── echo.py
    ├── keyboards/
    │   ├── __init__.py
    │   └── menus.py
    ├── services/
    │   ├── __init__.py
    │   ├── i18n.py
    │   ├── platform_api.py
    │   └── user_preferences.py
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
| IELTS_API_BASE_URL | No | http://127.0.0.1:8000 | Django backend base URL |
| IELTS_BOT_INTERNAL_SECRET | Yes | — | Shared secret for bot-to-backend requests |

## Run tests

    python -m unittest discover -s tests -v

GitHub Actions runs the unit tests and Python bytecode compilation on pushes and pull requests to main.

## Development notes

- The SQLite database and new columns are created/migrated automatically at startup.
- SQLite operations run via asyncio.to_thread so synchronous database calls do not block the event loop.
- Translation strings are centralized in services/i18n.py.
- FSM uses in-memory storage by default. Use Redis or another persistent storage if FSM state must survive restarts or multiple workers.
- This is a starter template, not a complete production deployment. Add automated tests, rate limiting, error monitoring, and deployment-specific infrastructure before public production use.

Never commit .env, database files, or expose your bot token.
