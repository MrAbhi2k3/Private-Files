# (c) @TeleRoid14

import os

class Config(object):
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    BOT_USERNAME = os.environ.get("BOT_USERNAME")
    DESTINATION_BOT_TOKEN = os.environ.get("DESTINATION_BOT_TOKEN")
    DESTINATION_BOT_USERNAME = os.environ.get("DESTINATION_BOT_USERNAME")
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL"))
    BOT_OWNER = int(os.environ.get("BOT_OWNER"))
    DATABASE_URL = os.environ.get("DATABASE_URL")
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", None)
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))
    ABOUT_BOT_TEXT = """
This is Permanent FileStore Bot!
Send me any file I will save it in my DataBase. Also works for channels.
Add me to channel as Admin with Edit Permission, I will add Saved File in Channel & add Share Button Link.

🤖 My Name: [FileStores Bot](https://t.me/{BOT_USERNAME})

📝 Language: [Python 3 ](https://www.python.org) 

📚 Library: Pyrogram

📡 Hosted on: Heroku

🧑🏻‍💻 Developer: @MrAbhi2k3 

👥 Support Group: @TeleRoid14

📢 Updates Channel: @TeleRoidGroup
"""
    ABOUT_DEV_TEXT = """
Hi there, I'm Abhishek Kumar, a student and a Learner. I love to play with TG and I'm always trying to learn more. I created this bot to help people store their files securely and easily. If you have any questions or suggestions, feel free to contact me!

You can reach me on: @TeleRoid14

🧑🏻‍💻 GitHub: https://github.com/PredatorHackerzZ

My UPI & Link is On @DonateXRobot

	Want to Buy Bots : @OwnYourBotz 

"""

	HOME_TEXT = """
Hello, [{}](tg://user?id={})

This is Permanent **File Store Bot**.

How To Use This Bot & Benefits??

📍 Send Me Any File & It'll Be Uploaded Into My Database & You Get The File Link.

⚠️ Benefit: If You Have Telegram Movie Channel, Then It's Useful For Your Daily Usage, You can Send Me Your File & I'll Send You The Link Of Your File So Your Subscribers Can Get The File From Me & Your Channel Will Be Safe From COPYRIGHT INFRINGEMENT Issue.

❌ 𝗣𝗢𝗥𝗡𝗢𝗚𝗥𝗔𝗣𝗛𝗜𝗖 𝗖𝗢𝗡𝗧𝗘𝗡𝗧𝗦 Are Strictly Prohibited & Will Get You Banned Permanently...
"""
