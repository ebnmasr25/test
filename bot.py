##################### Codded By #####################
##################### ~ Zaid ~ Telegram : @ZDDDU
##################### ~ Source Channel : t.me/Y88F8
##################### © All rights reserved 
##################### 3 Sep 2022 


##################### Database #####################

# pip install pymongo[srv]
# pip install pyrogram
# pip install motor
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient # You can use pymongo module also
MONGO = "mongodb+srv://ebnmasr:Aaee1122##@clustering0.bew52zk.mongodb.net/?retryWrites=true&w=majority" # mongo db url here
mongo = MongoClient(MONGO)
mongodb = mongo.bot # You can change mongo.bot -> mongo.anything to use many bots/apps on same MONGO_URL
##################### USERS DB #####################
usersdb = mongodb.users

async def is_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def get_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list
    
async def add_user(user_id: int):
    is_served = await is_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})    
    
##################### GROUPS DB #####################
groupsdb = mongodb.groups

async def is_group(chat_id: int) -> bool:
    group = await groupsdb.find_one({"chat_id": chat_id})
    if not group:
        return False
    return True

async def get_groups() -> list:
    groups_list = []
    async for group in groupsdb.find({"chat_id": {"$gt": 0}}):
        groups_list.append(group)
    return groups_list
    
async def add_group(chat_id: int):
    is_served = await is_group(chat_id)
    if is_served:
        return
    return await groupsdb.insert_one({"chat_id": chat_id})   
    
# async def remove_group(chat_id: int):
#   is_served = await is_group(chat_id)
#   if not is_served:
#       return
#   return await groupsdb.remove_one({"chat_id": chat_id})   
    
##################### Pyrogram Client #####################
from pyrogram import Client, filters
app = Client(

    "Song Downloader Bot",

    bot_token = os.environ["BOT_TOKEN"],

    api_id = int(os.environ["API_ID"]),

    api_hash = os.environ["API_HASH"]

)
OWNER = 5601843091# Bot Owner ID
##################### START #####################
TEXT = """
**-> New User start your bot !

- Name : {}
- Id : {}

- Users stats : {}

➖**
"""
START_TEXT = "**Hello {} Its a very simple bot by @ZDDDU** !"
START = filters.command("start") & filters.private
@app.on_message(START)
@app.on_edited_message(START)
async def start(client, message):
      user_id = message.from_user.id
      if not await is_user(user_id):
         await add_user(user_id)
         a = message.from_user.mention
         b = message.from_user.id
         c = len(await get_users())
         await app.send_message(
            OWNER,
            TEXT.format(a,b,c)
         )
      a = message.from_user.id
# if your bot made on pyrogram 1.4 ,replace message.id to message.message_id
      await app.send_message(
          message.chat.id,
          START_TEXT.format(a),
          reply_to_message_id = message.id 
      )
NEW_GROUP = """
-> New Group !

-> Group Title : {}

-> Stats now : {}

➖
"""
@app.on_message(filters.new_chat_members)
async def new_chat(client, message):
    chat_id = message.chat.id
    await add_group(chat_id)
    bot_id = int(TOKEN.split(":")[0])
    for member in message.new_chat_members:
        if member.id == bot_id:
            await message.reply(
                " ** Thanks for add me to your group ! **"
            )
            a = message.chat.title
            b = len(await get_groups())
            await app.send_message(
                 OWNER,
                 NEW_GROUP.format(a,b)
            )
                 

##################### STATS & GET COPY #####################
STATS_TEXT = """**
Hello !

Bot stats :

Users : {}
Groups : {}

➖**
"""

STATS = filters.command("stats") & filters.user(OWNER)
STATS2 = filters.regex("^الاحصائيات$") & filters.user(OWNER)
@app.on_message(STATS)
@app.on_message(STATS2)
@app.on_edited_message(STATS)
@app.on_edited_message(STATS2)
async def stats(client, message):
      id = message.chat.id
      stats = len(await get_users())
      group_stats = len(await get_groups())
# if your bot made on pyrogram 1.4 ,replace message.id to message.message_id
      await app.send_message(
          id,
          STATS_TEXT.foramat(stats,group_stats),
          reply_to_message_id = message.id
      )

COPY = filters.command("getcopy") & filters.user(OWNER)
COPY2 = filters.regex("^نسخة احتياطية$") & filters.user(OWNER)
@app.on_message(COPY)
@app.on_message(COPY2)
@app.on_edited_message(COPY)
@app.on_edited_message(COPY2)
async def getcopy(client, message):
       id = message.chat.id
       d = message.id    
       m = await message.reply("**-» Processing ..**")
       filename = "@Y88F8 - Users .txt"
       with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(await get_users()))
       stats = len(await get_users())
       await message.reply_document(
            document=filename,
            caption=f"-» Users : {stats} ",
            quote=False
       )
       os.remove(filename)
       filename2 = "@Y88F8 - Groups .txt"
       with open(filename2, "w+", encoding="utf8") as out_file:
            out_file.write(str(await get_groups()))
       stats2 = len(await get_groups())
       await message.reply_document(
            document=filename2,
            caption=f"-» Groups : {stats2} ",
            quote=False
       )
       await m.delete()
       os.remove(filename2)
##################### BORAODCAST #####################
from pyrogram.types import Message
USERS_BROADCAST = filters.command("broadcast_users") & filters.user(OWNER)
USERS_BROADCAST2 = filters.regex("اذاعة بالخاص") & filters.user(OWNER)
@app.on_message(USERS_BROADCAST)
@app.on_message(USERS_BROADCAST2)
async def broadcast(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.id
        y = message.chat.id
        sent = 0
        users = []
        hah = await get_users()
        for user in hah:
            users.append(int(user["user_id"]))
        for i in users:
            try:
                m = await c.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"Successfully broadcasted to {sent} User ! ")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Type the command with your query or reply to an message**"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    users = []
    hah = await get_users()
    for user in hah:
        users.append(int(user["user_id"]))
    for i in users:
        try:
            m = await c.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"Successfully broadcasted to {sent} User !")
    

GROUPS_BROADCAST = filters.command("broadcast_groups") & filters.user(OWNER)
GROUPA_BROADCAST2 = filters.regex("اذاعة بالجروبات") & filters.user(OWNER)
@app.on_message(GROUPS_BROADCAST)
@app.on_message(GROUPS_BROADCAST2)
async def broadcasttt(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.id
        y = message.chat.id
        sent = 0
        groups = []
        hah = await get_groups()
        for group in hah:
            groups.append(int(user["chat_id"]))
        for i in groups:
            try:
                m = await c.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"Successfully broadcasted to {sent} Group ! ")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Type the command with your query or reply to an message**"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    groups = []
    hah = await get_users()
    for group in hah:
        groups.append(int(user["chat_id"]))
    for i in groups:
        try:
            m = await c.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"Successfully broadcasted to {sent} Group !")    
    

##################### Run Client #####################
print("«- Your Client has been started ✓ -»")
app.run()

##################### Codded By #####################
##################### ~ Zaid ~ Telegram : @ZDDDU
##################### ~ Source Channel : t.me/Y88F8
##################### © All rights reserved 
##################### 3 Sep 2022 
