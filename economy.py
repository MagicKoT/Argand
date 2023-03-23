import discord
import asyncio
from discord.utils import get
from discord.ext import commands
from pymongo import MongoClient
import time
import configparser

conf = configparser.ConfigParser()
conf.read('config.ini')

# Забираем данные ...
support = conf.get('Settings', 'Support')
prefix = conf.get('Settings', 'Prefix')

intents = discord.Intents().all()
client = commands.Bot(command_prefix = prefix, intents = intents)
cluster = MongoClient("mongodb://127.0.0.1:27017")
collguild = cluster.argand.guild
collmember = cluster.argand.member

@client.event
async def on_ready():
    for guild in client.guilds:
        for member in guild.members:
            post1 = {
                "_id": member.id,
                "name": member.name,
                "balance": 0,
                "voice_active": 0,
                "messages": 0,
                "voice_trip": 0,
                "message_cd": 0,
                "deaf_time": 0,
                "deaf_trip": 0
            }
            if collmember.count_documents({"_id": member.id}) == 0:
                collmember.insert_one(post1)
            print(f"Пользователь {member.name}Добавлен в базу данных")
    print(f"Бот {client.user}успешно запушен и проверил пользователей на наличие в базе данных")

@client.event
async def on_voice_state_update(member, before, after):
    data = collmember.find_one({"_id": member.id})
    datag = collguild.find_one({"_id": member.guild.id})
    t2 = time.time()
    dte = data["deaf_time"]

    if before.channel is None and after.channel is not None:
        t1 = time.time()
        collmember.update_one({"_id": member.id},
            {"$set": {"voice_trip": t1}})
        print(f"Пользователь {member.name} зашел на канал {after.channel.name}")
        return
    if before.channel is not None and after.channel is None:
        if data["voice_trip"] == 0:
            return
        t1 = data["voice_trip"]
        voice_activ = data["voice_active"]
        balance = data["balance"]
        tim = t2-t1
        vox = datag["eco_rate"]
        if data["deaf_time"] != 0:
            # if data["deaf_time"] < tim:
            de = data["deaf_time"]
            tim1 = tim - de
            collmember.update_one({"_id": member.id},
                {"$set": {"voice_active": voice_activ + tim1}})
            collmember.update_one({"_id": member.id},
                {"$set": {"balance": balance + (tim1 / 12) * vox}})
            collmember.update_one({"_id": member.id},
                {"$set": {"deaf_time": 0}})
        else:
            collmember.update_one({"_id": member.id},
                {"$set": {"voice_active": voice_activ + tim}})
            collmember.update_one({"_id": member.id},
                {"$set": {"balance": balance + (tim / 12) * vox}})
        print(f"Пользователь {member.name} вышел с канала {before.channel.name}")
        return
    if before.channel is not None and after.channel is not None and before.channel != after.channel:
        print(f"Пользователь {member.name} перешел с канала {before.channel.name} на канал {after.channel.name}")
        return
    else:
        if before.self_deaf is False and after.self_deaf is True:
            collmember.update_one({"_id": member.id},
                {"$set": {"deaf_trip": t2}})
            print(f"пользователь {member.name} выключил у себя звук и микрофон")
            return
        if before.self_deaf is True and after.self_deaf is False:
            if data["deaf_trip"] == 0:
                return
            else:
                dt = data["deaf_trip"]
                dea = t2 - dt
                deaf = dea / 12
                collmember.update_one({"_id": member.id},
                    {"$set": {"deaf_time": dte + deaf}})
            print(f"пользователь {member.name} включил у себя звук и микрофон")
            return
        if before.self_mute is False and after.self_mute is True:
            collmember.update_one({"_id": member.id},
                {"$set": {"deaf_trip": t2}})
            print(f"пользователь {member.name} выключил микрофон")
            return
        if before.self_mute is True and after.self_mute is False:
            if data["deaf_trip"] == 0:
                return
            else:
                dt = data["deaf_trip"]
                dea = t2 - dt
                deaf = dea / 12
                collmember.update_one({"_id": member.id},
                    {"$set": {"deaf_time": dte + deaf}})
            print(f"пользователь {member.name} включил микрофон")
            return
        
client.run('MTA4NjcwNTg4Mzk1NTg2Nzc4MQ.GZCoKb.BLjQ-2eqx9mH2oktmmaUEb_4NuFdTpwVd09wZU')
