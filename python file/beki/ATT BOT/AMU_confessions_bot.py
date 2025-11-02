#!/usr/bin/env python3
"""
University Confession Bot – Complete Version
--------------------------------------------
Anonymous confession + moderation Telegram bot.
"""

import os
import sys
import json
import logging
import sqlite3
import html
from datetime import datetime, timedelta
from typing import Optional

# Try to use async SQLite if available
try:
    import aiosqlite
    ASYNC_DB = True
except ImportError:
    ASYNC_DB = False

from telegram import (
    Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto,
)
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters,
)

# --------------------------
# Environment configuration
# --------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")          # e.g. @myconfessions or -100xxxxxxxxxx
ADMIN_IDS_RAW = os.getenv("ADMIN_IDS")        # e.g. "123456,234567"
DATABASE_PATH = os.getenv("DATABASE_PATH", "confessions.db")
MAX_PER_DAY = int(os.getenv("MAX_PER_DAY", "3"))

if not BOT_TOKEN or not CHANNEL_ID or not ADMIN_IDS_RAW:
    print("❌ Please set BOT_TOKEN, CHANNEL_ID, and ADMIN_IDS environment variables.")
    sys.exit(1)

ADMIN_IDS = set()
for i in ADMIN_IDS_RAW.split(","):
    try:
        ADMIN_IDS.add(int(i.strip()))
    except ValueError:
        pass

# --------------------------
# Logging
# --------------------------
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --------------------------
# Helpers
# --------------------------
def utcnow(): return datetime.utcnow()
def anon_tag(n): return f"Anon#{n:04d}"
def escape_md(text): return html.escape(text)

# --------------------------
# Database
# --------------------------
CREATE_SQL = """
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    anon_local_id INTEGER,
    points INTEGER DEFAULT 0,
    is_banned INTEGER DEFAULT 0,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS confessions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    anon_local_id INTEGER,
    category TEXT,
    text TEXT,
    media_type TEXT,
    media_file_id TEXT,
    status TEXT,
    created_at TEXT,
    channel_message_id INTEGER
);
CREATE TABLE IF NOT EXISTS submissions_log(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    submitted_at TEXT
);
"""

if ASYNC_DB:
    import aiosqlite
    async def db_init():
        global conn
        conn = await aiosqlite.connect(DATABASE_PATH)
        await conn.executescript(CREATE_SQL)
        await conn.commit()
else:
    def db_init_sync():
        global conn
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        cur = conn.cursor()
        cur.executescript(CREATE_SQL)
        conn.commit()
    db_init = db_init_sync

async def db_exec(query, params=()):
    if ASYNC_DB:
        async with conn.execute(query, params) as cur:
            await conn.commit()
            return cur
    else:
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        return c

async def db_one(query, params=()):
    if ASYNC_DB:
        cur = await conn.execute(query, params)
        row = await cur.fetchone()
        await cur.close()
        return row
    else:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchone()

async def db_all(query, params=()):
    if ASYNC_DB:
        cur = await conn.execute(query, params)
        rows = await cur.fetchall()
        await cur.close()
        return rows
    else:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()

# --------------------------
# Core logic
# --------------------------
async def ensure_user(user_id: int):
    row = await db_one("SELECT anon_local_id FROM users WHERE user_id=?", (user_id,))
    if row: return row[0]
    anon = int(datetime.utcnow().timestamp() * 1000) % 10000
    await db_exec(
        "INSERT INTO users(user_id, anon_local_id, created_at) VALUES(?,?,?)",
        (user_id, anon, utcnow().isoformat())
    )
    return anon

async def user_submissions_24h(user_id: int):
    since = (utcnow() - timedelta(days=1)).isoformat()
    row = await db_one("SELECT COUNT(*) FROM submissions_log WHERE user_id=? AND submitted_at>=?",
                       (user_id, since))
    return row[0] if row else 0

# --------------------------
# Bot commands
# --------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await ensure_user(user.id)
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💌 Confess", callback_data="confess")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("🏆 Leaderboard", callback_data="leaderboard")]
    ])
    await update.message.reply_text(
        "👋 Welcome to *University Confession Bot!*\n\nSend anonymous confessions safely.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb
    )

async def confess_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✍️ Send your confession message (text or media).")
    context.user_data["confessing"] = True

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message
    if not context.user_data.get("confessing"):
        return
    count = await user_submissions_24h(user.id)
    if count >= MAX_PER_DAY:
        await msg.reply_text("⚠️ You reached your daily limit.")
        return
    text = msg.text or "(media)"
    media_type, file_id = None, None
    if msg.photo:
        media_type, file_id = "photo", msg.photo[-1].file_id
    anon = await ensure_user(user.id)
    await db_exec(
        "INSERT INTO confessions(user_id, anon_local_id, text, media_type, media_file_id, status, created_at)"
        " VALUES(?,?,?,?,?,?,?)",
        (user.id, anon, text, media_type, file_id, "pending", utcnow().isoformat())
    )
    await db_exec("INSERT INTO submissions_log(user_id, submitted_at) VALUES(?,?)", (user.id, utcnow().isoformat()))
    await msg.reply_text("✅ Sent for review! Admins will approve it soon.")
    context.user_data["confessing"] = False

async def profile_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    row = await db_one("SELECT anon_local_id, points FROM users WHERE user_id=?", (user.id,))
    anon, pts = row if row else (0, 0)
    await query.edit_message_text(f"👤 Profile\nAlias: {anon_tag(anon)}\nPoints: {pts}")

async def leaderboard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    rows = await db_all("SELECT anon_local_id, points FROM users ORDER BY points DESC LIMIT 10")
    txt = "🏆 *Top Confessors:*\n\n"
    for i, (aid, pts) in enumerate(rows, 1):
        txt += f"{i}. {anon_tag(aid)} — {pts} pts\n"
    await query.edit_message_text(txt, parse_mode=ParseMode.MARKDOWN)

# --------------------------
# Admin commands
# --------------------------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return await update.message.reply_text("Not authorized.")
    text = " ".join(context.args)
    await context.bot.send_message(CHANNEL_ID, text)
    await update.message.reply_text("📢 Broadcast sent.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    row = await db_one("SELECT COUNT(*) FROM confessions", ())
    total = row[0] if row else 0
    await update.message.reply_text(f"📊 Total confessions: {total}")

# --------------------------
# Dispatcher setup
# --------------------------
async def main():
    if ASYNC_DB:
        await db_init()
    else:
        db_init()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(confess_callback, pattern="^confess$"))
    app.add_handler(CallbackQueryHandler(profile_callback, pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(leaderboard_callback, pattern="^leaderboard$"))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, message_handler))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("stats", stats))

    logger.info("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
