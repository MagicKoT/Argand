import discord
import asyncio
from discord.utils import get
from pymongo import MongoClient

intents = discord.Intents().all()
client = discord.Client(command_prefix = "-", intents = intents)
cluster = MongoClient("mongodb://127.0.0.1:27017")
collguild = cluster.argand.guild

@client.event
async def on_ready():
    for guild in client.guilds:
        post1 = {
            "_id": guild.id,
            "name": guild.name,
            "support": [],
            "verify": True
        }
        if collguild.count_documents({"_id": guild.id}) == 0:
            collguild.insert_one(post1)
    print(f"бот {client.name} успешно запущен и подключен")

@client.event
async def on_voice_state_update(member, before, after):
    guild = after.channel.guild
    datag = collguild.find_one({"_id": guild.id})
    bf = before.channel.id
    af = after.channel.id
    if datag["verify"] == True:
        if member.id in datag["support"]:
            return
        # Добавить проверку, что человек только зашел на канал, а не перешёл или выполнил условие
        if af == 1056206116469612646 or af == 1056206116469612647 or af == 1056206116469612648 or af == 1056206116469612649 or af == 1057637012028522596:
            print(f"Пользователь {member.name} зашел в {after.channel.name} и ждет верефикации")

@client.event
async def on_member_join(ctx, member):
    guild = ctx.guild
    datag = collguild.find_one({"_id": guild.id})
    if datag["verify"] == False:
        await member.send("Привет! Выберите ваш пол, нажав на соответствующую реакцию:")
        message = await member.send("👦 для выбора Мальчик\n👧 для выбора Девочка")
        await message.add_reaction('👦')
        await message.add_reaction('👧')

        def check(reaction, user):
            return user == member and str(reaction.emoji) in ['👦', '👧']

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            await member.send("Время на выбор пола истекло, вы будете исключены из сервера.")
            await member.kick(reason="Не выбран пол")
        else:
            if str(reaction.emoji) == '👦':
                role = get(member.guild.roles, name='Мальчик')
                await member.add_roles(role, reason='Выбор пола')
            elif str(reaction.emoji) == '👧':
                role = get(member.guild.roles, name='Девочка')
                await member.add_roles(role, reason='Выбор пола')
            await member.send("Вы успешно выбрали свой пол и можете продолжать пользоваться сервером.")

client.run('YOUR_BOT_TOKEN')