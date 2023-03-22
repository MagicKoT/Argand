import discord
from discord.utils import get
from discord.ext import commands
import configparser
from datetime import datetime, timezone
from pymongo import MongoClient

conf = configparser.ConfigParser()
conf.read('config.ini')

# Забираем данные ...
support = conf.get('Settings', 'Support')
prefix = conf.get('Settings', 'Prefix')
cluster = MongoClient("mongodb://127.0.0.1:27017")
collguild = cluster.argand.guild

intents = discord.Intents().all()
client = commands.Bot(command_prefix = prefix, intents = intents)


@client.event
async def on_ready():
    print(f"Бот {client.user}успешно запушен и проверил пользователей на наличие в базе данных")

@client.command(
        name = "mute_log",
        brefing = "Включает/выключает логи выключение или включения микрофона"
)
async def mutelog(ctx, number:int = 2):
    guild = ctx.guild
    datag = collguild.find_one({"_id": guild.id})
    if number == 2:
        ctx.send("Укажите пожалуйста верное значение\n 1 - Выключить\n 0 - Включить")
    if number == 1:
        collguild.update_one({"_id": ctx.guild.id},
                {"$set": {"deaf_logs": True}})
        await ctx.send("Функция логов микрофона включена")
    if number == 0:
        collguild.update_one({"_id": ctx.guild.id},
                {"$set": {"deaf_logs": False}})
        await ctx.send("Функция логов микрофона выключена")

@client.event
async def on_voice_state_update(member, before, after):
    ch = client.get_channel(1086720746807636030)
    if before.channel is None and after.channel is not None:
        print(f"Пользователь {member.name} зашел на канал {after.channel.name}")
        action = "зашел в войс"
        color = 0x00FF00
        embed = discord.Embed(title="Голосовая активность", description=f"Пользователь {member.mention} {action}", color=color)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Канал", value=f"<#{after.channel.id}>")
        await ch.send(embed=embed)
        return
    if before.channel is not None and after.channel is None:
        print(f"Пользователь {member.name} вышел с канала {before.channel.name}")
        chid = before.channel.id
        action = "вышел с войса"
        color = 0xFF0000
        embed = discord.Embed(title="Голосовая активность", description=f"Пользователь {member.mention} {action}", color=color)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Канал", value=f"<#{chid}>")
        await ch.send(embed=embed)
        return
    if before.channel is not None and after.channel is not None and before.channel != after.channel:
        print(f"Пользователь {member.name} перешел с канала {before.channel.name} на канал {after.channel.name}")
        chid = before.channel.id
        action = "перешел на другой канал"
        color = 0x0000FF
        embed = discord.Embed(title="Голосовая активность", description=f"Пользователь {member.mention} {action}", color=color)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Прошлый канал", value=f"<#{before.channel.id}>")
        embed.add_field(name="Новый канал", value=f"<#{after.channel.id}>")
        await ch.send(embed=embed)
        return
    else:
        guild = member.guild
        datag = collguild.find_one({"_id": guild.id})
        if datag["deaf_logs"] == True:
            action = ""
            color = 0
            channel = after.channel or before.channel
            if before.self_deaf is False and after.self_deaf is True:
                action = "выключил у себя звук и микрофон"
                color = 0xFF0000
                embed = discord.Embed(title="Голосовая активность", description=f"**{member.mention}** {action}", color=color)
                embed.set_thumbnail(url=member.avatar)
                embed.add_field(name="Канал", value=f"<#{channel.id}>")
                await ch.send(embed=embed)
                return
            elif before.self_deaf is True and after.self_deaf is False:
                action = "включил у себя звук и микрофон"
                color = 0x00FF00
                embed = discord.Embed(title="Голосовая активность", description=f"**{member.mention}** {action}", color=color)
                embed.set_thumbnail(url=member.avatar)
                embed.add_field(name="Канал", value=f"<#{channel.id}>")
                await ch.send(embed=embed)
                return
            elif before.self_mute is False and after.self_mute is True:
                action = "выключил микрофон"
                color = 0xFF0000
                embed = discord.Embed(title="Голосовая активность", description=f"**{member.mention}** {action}", color=color)
                embed.set_thumbnail(url=member.avatar)
                embed.add_field(name="Канал", value=f"<#{channel.id}>")
                await ch.send(embed=embed)
                return
            elif before.self_mute is True and after.self_mute is False:
                action = "включил микрофон"
                color = 0x00FF00
                embed = discord.Embed(title="Голосовая активность", description=f"**{member.mention}** {action}", color=color)
                embed.set_thumbnail(url=member.avatar)
                embed.add_field(name="Канал", value=f"<#{channel.id}>")
                await ch.send(embed=embed)
                return

async def log_deleted_messages(message):
    # Проверяем, что это текстовый канал
    if not isinstance(message.channel, discord.TextChannel):
        return
    channel = message.channel
    # Создаем вложенный embed с информацией
    color = 0xFF0000
    embed = discord.Embed(title="Удаленные сообщения", description=f"Канал: **#{channel.name}**", color=color)
    print(f"Удалено сообщение: {message.content}")
    # Если удалено, то добавляем информацию в embed и отправляем его
    embed.add_field(name="Автор", value=message.author.mention, inline=False)
    embed.add_field(name="Удалено", value=message.content, inline=False)
    ch = channel.guild.get_channel(1086720790248034462)
    await ch.send(embed=embed)


async def log_edited_messages(before, after):
    channel = None
    if after and after.channel:
        channel = after.channel
    elif before and before.channel:
        channel = before.channel

    # Проверяем, что это текстовый канал
    if not isinstance(channel, discord.TextChannel):
        return


    # Создаем вложенный embed с информацией о канале
    color = 0x0000FF
    embed = discord.Embed(title="Измененные или удаленные сообщения", description=f"Канал: **#{channel.name}**", color=color)

    # Проверяем удалено ли сообщение
    
    # Проверяем изменено ли 
    message_url = after.jump_url
    # before.content and after.content and before.content != after.content:
    print(f"Изменено сообщение: {before.content} на {after.content}")
    # Если изменено, то добавляем информацию в embed и отправляем его
    
    embed.add_field(name="Автор", value=before.author.mention, inline=False)
    embed.add_field(name="Было", value=before.content, inline=False)
    embed.add_field(name="Стало", value=after.content, inline=False)
    embed.add_field(name="Сообщение", value=f"[Перейти]({message_url})", inline=False)
    ch = channel.guild.get_channel(1086720790248034462)
    await ch.send(embed=embed)

@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return
    await log_deleted_messages(message)

@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    await log_edited_messages(before, after)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1086720714498916443)
    inviter_id = await get_inviter_id(member)
    if inviter_id is None:
        inviter = "Не удалось узнать кто приглосил"
    elif inviter_id is not None:
        inviter = f"<@{inviter_id}>"
    join_date1 = member.joined_at.replace(tzinfo=timezone.utc)
    leave_date1 = datetime.now(timezone.utc)
    time_spent = leave_date1 - join_date1
    time_spent_str = str(time_spent).split('.')[0]
    join_date = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
    leave_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    # time_spent = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
    roles = [role.mention for role in member.roles[1:]] # exclude @everyone role
    
    embed = discord.Embed(
        title=f"**{member.name}** #{member.discriminator} Покинул сервер",
        description=f"**Приглосил:** {inviter}",
        color=discord.Color.red()
    )
    
    embed.set_thumbnail(url=member.avatar)
    
    embed.add_field(name="Зашел", value=join_date, inline=True)
    embed.add_field(name="Роли", value=", ".join(roles), inline=True)
    embed.add_field(name="Пробыл", value=time_spent_str, inline=True)
    embed.add_field(name="Вышел", value=leave_date, inline=True)
    embed.set_footer(text=f"ID: {member.id}")
    
    await channel.send(embed=embed)

@client.event
async def on_member_join(member):
    channel = client.get_channel(1056296400230559754)
    inviter_id = await get_inviter_id(member)
    if inviter_id is None:
        inviter = "Не удалось узнать кто приглосил"
    elif inviter_id is not None:
        inviter = f"<@{inviter_id}>"
    join_date = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
    registred_at = member.created_at.strftime("%Y-%m-%d %H:%M:%S")
    # time_spent = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
    roles = [role.mention for role in member.roles[1:]] # exclude @everyone role
    
    embed = discord.Embed(
        title=f"**{member.name}** #{member.discriminator} Зашел на сервер",
        description=f"**Приглосил:** {inviter}",
        color=discord.Color.red()
    )
    
    embed.set_thumbnail(url=member.avatar)
    
    embed.add_field(name="Зашел", value=join_date, inline=True)
    embed.add_field(name="Регестрация", value=registred_at, inline=True)
    embed.set_footer(text=f"ID: {member.id}")
    await channel.send(embed=embed)

async def get_inviter_id(member):
    invites = await member.guild.invites()
    for invite in invites:
        if invite.code == member.guild.me.id:
            continue
        if invite.uses < invite.max_uses:
            if invite.created_at > member.joined_at:
                return invite.inviter.id
    return None

            
                
client.run('MTA4ODA3MDg3OTg0NzY2NTcyNA.G_Sf5z.IvIV1UF1AHjTmgLUQv4Tdtt-Hxi26-WvmjrJOA')
