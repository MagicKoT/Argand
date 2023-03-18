import discord
import asyncio
from discord.utils import get
from discord.ext import commands
from pymongo import MongoClient
from discord.ui import Button, View, Select
from discord import ui, Interaction


intents = discord.Intents().all()
prefix = "-"
client = commands.Bot(command_prefix = prefix, intents = intents)
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
    print(f"бот {client.user} успешно запущен и подключен")

class VerifyView(View):
    def __init__(self, member):
        super().__init__()
        self.member = member
    
    @discord.ui.button(label="Мужской", style=discord.ButtonStyle.primary, emoji='♂️')
    async def male(self, button: discord.ui.Button, interaction: discord.Interaction):
        role = discord.utils.get(self.member.guild.roles, name='♂️')
        unvr = discord.utils.get(self.member.guild.roles, name='unverify')
        await self.member.add_roles(role, reason='Выбор пола')
        await self.member.remove_roles(unvr, reason="Пройдена верификация")
        self.stop()
        # await interaction.response.send_message(f"Вы успешно провели верефикацию пользователю {self.member.name}. Ему была роль ♂️")
        # self.stop()

    @discord.ui.button(label="Женский", style=discord.ButtonStyle.primary, emoji='♀️')
    async def female(self, button: discord.ui.Button, interaction: discord.Interaction):
        role = discord.utils.get(self.member.guild.roles, name='♀️')
        unvr = discord.utils.get(self.member.guild.roles, name='unverify')
        await self.member.add_roles(role, reason='Выбор пола')
        await self.member.remove_roles(unvr, reason="Пройдена верификация")
        self.stop()
        # await interaction.response.send_message(f"Вы успешно провели верификацию пользователю {self.member.name}. Ей была роль ♀️")
        # self.stop()

@client.command(
    name="verify",
    aliases=["vf", "verefy", "veref", 'verif'],
    brief="Выберите как взаимодействовать с пользователем",
    usage=f"{prefix}vf @пользователь пол(М или Д)"
)
async def verify(ctx, member: discord.Member=None, gender:str=None):
    if member is None:
        await ctx.send("Вы не указали пользователя")
        return
    # if gender is None:
    #     await ctx.send("Вы не указали пол пользователя")
    #     return

    view = VerifyView(member)
    await ctx.send(f"Выберите пол для пользователя {member.mention}", view=view)


# @client.command(
#         name = "verify",
#         aliases = ["vf", "verefy", "veref", 'verif'],
#         brief = "Выберите как взаимодействовать с пользователем",
# 	    usage = f"{prefix}vf @пользователь пол(М или Д)"
#     )
# async def verify(ctx, member:discord.Member=None, gender:str=None):
#     if member is None:
#         await ctx.send("Вы не указали пользователя")
#         return
#     if gender is None:
#         await ctx.send("Вы не указали пол пользователя")
#         return
#     unvr = get(member.guild.roles, name='unverify')
#     # if gender != "м" or gender != "д" or gender != "М" or gender != "Д":
#     #     await ctx.send("Вы должны указать пол пользователя м или д")
#     #     return
#     if gender == "м" or gender == "М":
#         role = get(member.guild.roles, name='♂️')
#         await member.add_roles(role, reason='Выбор пола')
#         await member.remove_roles(unvr, reason="Пройдена верефикация")
#         await ctx.send(f"Вы увпешно провели верефикацию пользователю {member.name}. Ему была роль ♂️")
#         return
#     if gender == "д" or gender == "Д":
#         role = get(member.guild.roles, name='♀️')
#         await member.add_roles(role, reason='Выбор пола')
#         await member.remove_roles(unvr, reason="Пройдена верефикация")
#         await ctx.send(f"Вы увпешно провели верефикацию пользователю {member.name}. Ей была роль ♀️")
#         return
#     else:
#         await ctx.send("Вы должны указать пол пользователя м или д")
#         return
    

@client.command(
        name = "voice_verify",
        aliases = ["vv", "voiceverify", "Voice_Verify"],
        brief = "Включить или выключить голосовую верефикацию",
	    usage = f"{prefix}vv 1"
    )
async def voice_verify(ctx, sum):
    author = ctx.author
    if author.id == 1046480698468479108:
        if sum == "1":
            datag = collguild.find_one({"_id": ctx.guild.id})
            collguild.update_one({"_id": ctx.guild.id},
                {"$set": {"verify": True}})
            await ctx.message.add_reaction("✅")
            return
        if sum == "0":
            datag = collguild.find_one({"_id": ctx.guild.id})
            collguild.update_one({"_id": ctx.guild.id},
                {"$set": {"verify": False}})
            await ctx.message.add_reaction("✅")
            return
        else:
            await ctx.send("Вы указали не вероное значение\nЧто бы включить или выключить голосовую верефикацию нужно использовать одно из двух значений  \n 1 = Включить,   0 = Выключить")
            return
        
@client.event
async def on_voice_state_update(member, before, after):
    v_c = [1056206116469612646, 1086615962599575604, 1086616038289985547, 1086616040215150695, 1086616082284027904]
    guild = member.guild.id
    datag = collguild.find_one({"_id": guild})
    af = after.channel.id
    if datag["verify"] == True:
        if after.channel is None:
            return
        if member.id in datag["support"]:
            return
        # Добавить проверку, что человек только зашел на канал, а не перешёл или выполнил условие
        if before.channel is None and af in v_c:
            print(f"Пользователь {member.name} зашел в {after.channel.name} и ждет верефикации")
            ch = client.get_channel(1086614040270360646)
            await ch.send(f"<@&1056206116201168953> Пользователь {member.name} ждет верификации")

@client.event
async def on_member_join(member):
    guild = member.guild
    datag = collguild.find_one({"_id": guild.id})
    unvr = get(member.guild.roles, name='unverify')

    if datag["verify"] == False:
        await member.send("Привет! Выберите ваш пол, нажав на соответствующую реакцию:")
        message = await member.send("👦 для выбора Мальчик\n👧 для выбора Девочка")
        await message.add_reaction('👦')
        await message.add_reaction('👧')

        def check(reaction, user):
            return user == member and str(reaction.emoji) in ['👦', '👧']

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await member.send("Время на выбор пола истекло, вы будете исключены из сервера.")
            await member.kick(reason="Не выбран пол")
        else:
            if str(reaction.emoji) == '👦':
                role = get(member.guild.roles, name='♂️')
                await member.add_roles(role, reason='Выбор пола')
                await member.remove_roles(unvr, reason="Пройдена верефикация")
            elif str(reaction.emoji) == '👧':
                role = get(member.guild.roles, name='♀️')
                await member.add_roles(role, reason='Выбор пола')
                await member.remove_roles(unvr, reason="Пройдена верефикация")
            await member.send("Вы успешно выбрали свой пол и можете продолжать пользоваться сервером.")

client.run('MTA4Mjc1NzUxOTgwMzQzNzEzOA.GLq8um.sZkXhIGPdlsqPDGf4ibWyXBG3nax21E6Sovd50')