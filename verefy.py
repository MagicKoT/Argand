import discord
import asyncio
from discord.utils import get
from pymongo import MongoClient

intents = discord.Intents().all()
prefix = "-"
client = discord.Client(command_prefix = prefix, intents = intents)
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

@client.command(
        name = "voice_verify",
        aliases = ["vv", "voiceverify", "Voice_Verify"],
        brief = "Включить или выключить голосовую верефикацию",
	    usage = f"{prefix}vv 1"
    )
async def voice_verify(ctx, sum):
    author = ctx.author
    if author.id == 1046480698468479108:
        if sum == 1:
            datag = collguild.find_one({"_id": ctx.guild.id})
            collguild.update_one({"_id": ctx.guild.id},
                {"$set": {"verify": True}})
            await ctx.message.add_reaction("✅")
        if sum == 0:
            datag = collguild.find_one({"_id": ctx.guild.id})
            collguild.update_one({"_id": ctx.guild.id},
                {"$set": {"verify": False}})
            await ctx.message.add_reaction("✅")
        else:
            ctx.send("Вы указали не вероное значение\nЧто бы включить или выключить голосовую верефикацию нужно использовать одно из двух значений  \n 1 = Включить,   0 = Выключить")

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
        if before.channel is None and af == 1056206116469612646 or before.channel is None and af == 1056206116469612647 or before.channel is None and af == 1056206116469612648 or before.channel is None and af == 1056206116469612649 or before.channel is None and af == 1057637012028522596:
            print(f"Пользователь {member.name} зашел в {after.channel.name} и ждет верефикации")
            ch = client.get_channel(1086614040270360646)
            ch.send(f"<@&1056206116201168953> Пользователь {member.name} ждет верификации")

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
                role = get(member.guild.roles, name='♂️')
                await member.add_roles(role, reason='Выбор пола')
            elif str(reaction.emoji) == '👧':
                role = get(member.guild.roles, name='♀️')
                await member.add_roles(role, reason='Выбор пола')
            await member.send("Вы успешно выбрали свой пол и можете продолжать пользоваться сервером.")

client.run('MTA4Mjc1NzUxOTgwMzQzNzEzOA.GLq8um.sZkXhIGPdlsqPDGf4ibWyXBG3nax21E6Sovd50')