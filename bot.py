# (c) @TeleRoidGroup

import os
import time
import math
import json
import string
import random
import traceback
import asyncio
import datetime
import aiofiles
from random import choice
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid
from configs import Config
from database import Database

## --- Sub Configs --- ##
BOT_USERNAME = Config.BOT_USERNAME
BOT_TOKEN = Config.BOT_TOKEN
DESTINATION_BOT_USERNAME = Config.DESTINATION_BOT_USERNAME
DESTINATION_BOT_TOKEN = Config.DESTINATION_BOT_TOKEN
API_ID = Config.API_ID
API_HASH = Config.API_HASH
DB_CHANNEL = Config.DB_CHANNEL
ABOUT_BOT_TEXT = Config.ABOUT_BOT_TEXT
ABOUT_DEV_TEXT = Config.ABOUT_DEV_TEXT
HOME_TEXT = Config.HOME_TEXT
BOT_OWNER = Config.BOT_OWNER
db = Database(Config.DATABASE_URL, BOT_USERNAME)
broadcast_ids = {}
Bot = Client(BOT_USERNAME, DESTINATION_BOT_USERNAME, dest_bot_token=DESTINATION_BOT_TOKEN  bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

async def send_msg(user_id, message):
    try:
        if message.document:
            # Check if file size is less than or equal to 4GB
            if message.document.file_size <= (4 * 1024 * 1024 * 1024):
                await message.forward(chat_id=user_id)
            else:
                # File size greater than 4GB, send as document
                await Bot.send_document(chat_id=user_id, document=message.document.file_id)
        else:
            await message.forward(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

@Bot.on_message(filters.command("start") & filters.private)
async def start(bot, cmd):
	if not await db.is_user_exist(cmd.from_user.id):
		await db.add_user(cmd.from_user.id)
		await bot.send_message(
		    Config.LOG_CHANNEL,
		    f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{BOT_USERNAME} !!"
		)
	usr_cmd = cmd.text.split("_")[-1]
	if usr_cmd == "/start":
		if Config.UPDATES_CHANNEL:
			invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
			try:
				user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), cmd.from_user.id)
				if user.status == "banned":
					await bot.send_message(
						chat_id=cmd.from_user.id,
						text="You are Banned😛. Contact my [Support Group](https://t.me/TeleRoid14).",
						parse_mode="markdown",
						disable_web_page_preview=True
					)
					return
			except UserNotParticipant:
				await bot.send_message(
					chat_id=cmd.from_user.id,
					text="**Please Join Channel, Only Channel Subscribers can use the Bot!",
					reply_markup=InlineKeyboardMarkup(
						[
							[
								InlineKeyboardButton("⭕ Join Updates Channel ⭕", url=invite_link.invite_link)
							],
							[
								InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
							]
						]
					),
					parse_mode="markdown"
				)
				return
			except Exception:
				await bot.send_message(
					chat_id=cmd.from_user.id,
					text="Something went Wrong. Contact my [🛑 Support 🛑](https://t.me/TeleRoid14).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		await cmd.reply_text(
			HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id),
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("🛑 Support 🛑", url="https://t.me/TeleRoid14"),
						InlineKeyboardButton("⭕Channel⭕", url="https://t.me/TeleRoidGroup")
					],
					[
						InlineKeyboardButton("👥 About ", callback_data="aboutbot"),
						InlineKeyboardButton("👨‍🔧 Dev ", callback_data="aboutdevs")
					], 
                                        [
						InlineKeyboardButton(" Github ", url="https://GitHub.com/PredatorHackerzZ"),
						InlineKeyboardButton("📢 Powered By", url="https://t.me/MoviesFlixers_DL")
					]
				]
			)
		)
	else:
		if Config.UPDATES_CHANNEL:
			invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
			try:
				user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), cmd.from_user.id)
				if user.status == "kicked":
					await bot.send_message(
						chat_id=cmd.from_user.id,
						text=" You are Banned! Contact [🛑 Support Group 🛑](https://t.me/TeleRoid14).",
						parse_mode="markdown",
						disable_web_page_preview=True
					)
					return
			except UserNotParticipant:
				file_id = int(usr_cmd)
				await bot.send_message(
					chat_id=cmd.from_user.id,
					text="**Please Join Channel, Only Subscribers can use the Bot!",
					reply_markup=InlineKeyboardMarkup(
						[
							[
								InlineKeyboardButton("Updates Channel", url=invite_link.invite_link)
							],
							[
								InlineKeyboardButton("🔄 Try Again", url=f"https://telegram.me/{DESTINATION_BOT_USERNAME}?start=TeleRoid14_{file_id}")
							]
						]
					),
					parse_mode="markdown"
				)
				return
			except Exception:
				await bot.send_message(
					chat_id=cmd.from_user.id,
					text="Something went Wrong. Contact my [🛑 Support 🛑 ](https://t.me/TeleRoid14).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		try:
			file_id = int(usr_cmd)
			send_stored_file = await bot.copy_message(chat_id=cmd.from_user.id, from_chat_id=DB_CHANNEL, message_id=file_id)
			await send_stored_file.reply_text(f"**Here is Sharable Link of this file:** https://telegram.dog/{DESTINATION_BOT_USERNAME}?start=TeleRoid14_{file_id}\n\n  To Retrive the Stored File, just open the link!__", disable_web_page_preview=True, quote=True)
		except Exception as err:
			await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")

@Bot.on_message(filters.document | filters.video | filters.audio & ~filters.edited)
async def main(bot, message):
	if message.chat.type == "private":
		editable = await message.reply_text("Please wait ...")
		try:
			forwarded_msg = await message.forward(DB_CHANNEL)
			file_er_id = forwarded_msg.message_id
			await forwarded_msg.reply_text(f"#PRIVATE_FILE:\n\n[{message.from_user.first_name}](tg://user?id={message.from_user.id}) Got File Link!", parse_mode="Markdown", disable_web_page_preview=True)
			share_link = f"https://telegram.dog/{DESTINATION_BOT_USERNAME}?start=TeleRoid14_{file_er_id}"
			await editable.edit(
				f"**Your File Stored in the Database & Permanent Link of your file: {share_link} \n\nJust Click the link to get your file!",
				parse_mode="Markdown",
				reply_markup=InlineKeyboardMarkup(
					[[InlineKeyboardButton("Open Link", url=share_link)], [InlineKeyboardButton("⭕ Channel ⭕", url="https://t.me/TeleRoidGroup"), InlineKeyboardButton("🛑 Support 🛑", url="https://t.me/TeleRoid14")]]
				),
				disable_web_page_preview=True
			)
		except Exception as err:
			await editable.edit(f"Something Went Wrong!\n\n**Error:** `{err}`")
	elif message.chat.type == "channel":
		if message.chat.id == Config.LOG_CHANNEL:
			return
		elif message.chat.id == int(Config.UPDATES_CHANNEL):
			return
		else:
			pass
		forwarded_msg = None
		file_er_id = None
		if message.forward_from_chat:
			return
		elif message.forward_from:
			return
		else:
			pass
		if message.photo:
			return
		try:
			forwarded_msg = await message.forward(DB_CHANNEL)
			file_er_id = forwarded_msg.message_id
			share_link = f"https://telegram.dog/{DESTINATION_BOT_USERNAME}?start=TeleRoid14_{file_er_id}"
			CH_edit = await bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Get Sharable Stored Link", url=share_link)]]))
			if message.chat.username:
				await forwarded_msg.reply_text(f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/{message.chat.username}/{CH_edit.message_id}) Channel's Broadcasted File's Button Added!")
			else:
				private_ch = str(message.chat.id)[4:]
				await forwarded_msg.reply_text(f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/c/{private_ch}/{CH_edit.message_id}) Channel's Broadcasted File's Button Added!")
		except Exception as err:
			print(f"Error: {err}")

@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply)
async def broadcast_(c, m):
	all_users = await db.get_all_users()
	broadcast_msg = m.reply_to_message
	while True:
	    broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
	    if not broadcast_ids.get(broadcast_id):
	        break
	out = await m.reply_text(
	    text = f"Broadcast Started! You will be notified with log file when all the users are notified."
	)
	start_time = time.time()
	total_users = await db.total_users_count()
	done = 0
	failed = 0
	success = 0
	broadcast_ids[broadcast_id] = dict(
	    total = total_users,
	    current = done,
	    failed = failed,
	    success = success
	)
	async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
	    async for user in all_users:
	        sts, msg = await send_msg(
	            user_id = int(user['id']),
	            message = broadcast_msg
	        )
	        if msg is not None:
	            await broadcast_log_file.write(msg)
	        if sts == 200:
	            success += 1
	        else:
	            failed += 1
	        if sts == 400:
	            await db.delete_user(user['id'])
	        done += 1
	        if broadcast_ids.get(broadcast_id) is None:
	            break
	        else:
	            broadcast_ids[broadcast_id].update(
	                dict(
	                    current = done,
	                    failed = failed,
	                    success = success
	                )
	            )
	if broadcast_ids.get(broadcast_id):
	    broadcast_ids.pop(broadcast_id)
		completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
	await asyncio.sleep(3)
	await out.delete()
	if failed == 0:
	    await m.reply_text(
	        text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
	        quote=True
	    )
	else:
	    await m.reply_document(
	        document='broadcast.txt',
	        caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
	        quote=True
	    )
	    await os.remove('broadcast.txt')

@Bot.on_message(filters.private & filters.command("status") & filters.user(BOT_OWNER))
async def sts(c, m):
	total_users = await db.total_users_count()
	await m.reply_text(text=f"**Total Users in DB:** `{total_users}`", parse_mode="Markdown", quote=True)

@Bot.on_callback_query()
async def button(bot, cmd: CallbackQuery):
	cb_data = cmd.data
	if "aboutbot" in cb_data:
		await cmd.message.edit(
			ABOUT_BOT_TEXT,
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("Source Code ", url="https://github.com/PredatorHackerzZ")
					],
					[
						InlineKeyboardButton("🏠 Home ", callback_data="gotohome"),
						InlineKeyboardButton("👥 About Dev ", callback_data="aboutdevs")
					]
				]
			)
		)
	elif "aboutdevs" in cb_data:
		await cmd.message.edit(
			ABOUT_DEV_TEXT,
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("Source Code", url="https://github.com/PredatorHackerzZ")
					],
					[
						InlineKeyboardButton("👥 About", callback_data="aboutbot"),
						InlineKeyboardButton("🏠 Home", callback_data="gotohome")
					]
				]
			)
		)
	elif "gotohome" in cb_data:
		await cmd.message.edit(
			HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("🛑 Support 🛑", url="https://t.me/TeleRoid14"),
						InlineKeyboardButton("⭕ Channel ⭕", url="https://t.me/TeleRoidGroup")
					],
					[
						InlineKeyboardButton("🤖 About Bot", callback_data="aboutbot"),
						InlineKeyboardButton("👮 About Dev", callback_data="aboutdevs")
					]
				]
			)
		)
	elif "refreshmeh" in cb_data:
		if Config.UPDATES_CHANNEL:
			invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
			try:
				user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), cmd.message.chat.id)
				if user.status == "kicked":
					await cmd.message.edit(
						text="You Are banned. Contact my [Support Group](https://t.me/TeleRoid14).",
						parse_mode="markdown",
						disable_web_page_preview=True
					)
					return
			except UserNotParticipant:
				await cmd.message.edit(
					text="**Don't be OverSmart!**\n Only Subscribers can use the Bot!",
					reply_markup=InlineKeyboardMarkup(
						[
							[
								InlineKeyboardButton("🤖 Updates Channel", url=invite_link.invite_link)
							],
							[
								InlineKeyboardButton("🔄 Try Again 🔄", callback_data="refreshmeh")
							]
						]
					),
					parse_mode="markdown"
				)
				return
			except Exception:
				await cmd.message.edit(
					text="Something went Wrong. Contact my [Support Group](https://t.me/TeleRoid14).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		await cmd.message.edit(
			text=HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("🛑 Support 🛑", url="https://t.me/TeleRoid14"),
						InlineKeyboardButton("⭕ Channel ⭕", url="https://t.me/TeleRoidGroup")
					],
					[
						InlineKeyboardButton("🤖 About Bot", callback_data="aboutbot"),
						InlineKeyboardButton("👮 About Dev", callback_data="aboutdevs")
					]
				]
			)
		)

Bot.run()
