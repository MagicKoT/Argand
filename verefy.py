import discord
import asyncio
from discord.utils import get
from discord.ext import commands
from discord import errors
from pymongo import MongoClient
from discord.ui import Button, View, Select
from discord import ui, Interaction
import configparser
from typing import List

conf = configparser.ConfigParser()
conf.read('config.ini')

# Забираем данные из конфигурации (int-списки принудительно кастуем в List[int])
support_con:List[int] = [int(x) for x in conf.get('Settings', 'Support').split(',')]
prefix = conf.get('Settings', 'Prefix')
v_c:List[int] = [int(x) for x in conf.get('Settings', 'v_c').split(',')]


intents = discord.Intents().all()
client = commands.Bot(command_prefix = prefix, intents = intents)
cluster = MongoClient("mongodb://127.0.0.1:27017")
collguild = cluster.argand.guild


# Отключаем стандартные команды Discord
client.remove_command('help')


@client.event
async def on_ready():
    for guild in client.guilds:
        post1 = {
            "_id": guild.id,
            "name": guild.name,
            "eco_rate": 1.00,
            "exp_rate": 1.00,
            "verify": True
        }
        if collguild.count_documents({"_id": guild.id}) == 0:
            collguild.insert_one(post1)
    print(f"бот {client.user} успешно запущен и подключен")


class NoVerifiableMembers(Exception):
    """
    Bсключение для обработки случая, когда у нас нет пользователей для верификации
    """
    pass


class MemberSelect(ui.Select):
    """
    Класс селекта для для выбора пользователя.
    Базовый конструктор элемента, ничего больше.
    """
    def __init__(self, options):
        super().__init__(
            placeholder = "Выберите пользователя, которого хотите верифицировать",
            min_values = 1,
            max_values = 1,
            options = options
        )
class SelectMemberView(View):
    """
    View-объект для отображения выпадающего меню с выбором пользователя для дальнейшей верификации.
    При отсутствии пользователей для верификации выдаем исключение NoVerifiableMembers и обрываем исполнение.

    Аргументы:
    ----------
    - guild - объект guild, который мы передаем из контекста вызова команды, требуется для получения объекта member выбранного пользователя
    """
    def __init__(self, author, guild):
        super().__init__()

        self.author = author
        self.guild = guild
        self.member = None
        self.v_c = [1056206116469612646, 1086615962599575604, 1086616038289985547, 1086616040215150695, 1086616082284027904]
        self.member_options = self.parse_voice_channel_members()

        # Если не нашли пользователей - триггерим исключение
        if len(self.member_options) == 0:
            raise NoVerifiableMembers
            self.stop()

        # Создаем Select-объект и добавляем его в финальную View
        # Принудительно присобачиваем в качестве callback'а функцию этого класса (self.callback)
        self.select = MemberSelect(options=self.member_options)
        self.select.callback = self.callback
        self.add_item(self.select)

    """
    Callback, который вызывается на выбор пользователя из выпадающего меню
    Сохраняет объект выбранного пользователя в себе, вызываем ивент on_verify_selected_member
    для дальнейшего продвижения по процессу верификации
    """
    async def callback(self, interaction: discord.Interaction):
        if self.author.id != interaction.user.id:
            sobaka = self.guild.get_member(interaction.user.id)
            await interaction.response.send_message(f"Убери руки от чужой формы, собака {sobaka.mention}")
            return

        member_id = self.select.values[0]
        self.member = await self.guild.fetch_member(member_id)
        client.dispatch("on_verify_selected_member")
        self.stop()

    """
    Вспомогательная функция для поиска верифицируемых пользователей, отдает список найденных пользователей
    Обязательное требование - наличие роли unverify
    """
    def parse_voice_channel_members(self):
        member_options = []
        unvr = discord.utils.get(self.guild.roles, name='unverify').id

        for voice in self.v_c:
            ch = client.get_channel(voice)
            for member in ch.members:
                member_roles = [x.id for x in member.roles]
                if unvr in member_roles:
                    member_options.append(discord.SelectOption(label=member.name, value=member.id))

        return member_options

    """
    Просто возвращает выбранного пользователя (требуется для следующей View с выбором пола)
    """
    def get_selected_member(self):
        return self.member


class VerifyView(View):
    def __init__(self, ctx, member, author, guild):
        super().__init__()
        self.ctx = ctx
        self.guild = guild
        self.author = author
        self.member = member

    @discord.ui.button(label="Мужской", style=discord.ButtonStyle.primary, emoji='♂️')
    async def male(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.author.id != interaction.user.id:
            sobaka = self.guild.get_member(interaction.user.id)
            await interaction.response.send_message(f"Убери руки от чужой формы, собака {sobaka.mention}")
            return
        
        gender_role = discord.utils.get(self.member.guild.roles, name='♂️')
        verified_role = discord.utils.get(self.member.guild.roles, name='verify')
        unvr = discord.utils.get(self.member.guild.roles, name='unverify')
        await self.member.add_roles(gender_role, reason='Выбор пола')
        await self.member.add_roles(verified_role, reason='Пройдена верификация')
        await self.member.remove_roles(unvr, reason="Пройдена верификация")
        await interaction.response.send_message(f"{self.ctx.author.name} успешно провели верефикацию пользователю {self.member.name}. Ему была роль ♂️")
        client.dispatch("on_verify_selected_member")
        self.stop()

    @discord.ui.button(label="Женский", style=discord.ButtonStyle.primary, emoji='♀️')
    async def female(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.author.id != interaction.user.id:
            sobaka = self.guild.get_member(interaction.user.id)
            await interaction.response.send_message(f"Убери руки от чужой формы, собака {sobaka.mention}")
            return
        
        gender_role = discord.utils.get(self.member.guild.roles, name='♀️')
        verified_role = discord.utils.get(self.member.guild.roles, name='verify')
        unvr = discord.utils.get(self.member.guild.roles, name='unverify')
        await self.member.add_roles(gender_role, reason='Выбор пола')
        await self.member.add_roles(verified_role, reason='Пройдена верификация')
        await self.member.remove_roles(unvr, reason="Пройдена верификация")
        await interaction.response.send_message(f"{self.ctx.author.name} успешно провели верификацию пользователю {self.member.name}. Ей была роль ♀️")
        client.dispatch("on_verify_selected_member")
        self.stop()

"""
Кастомный ивент для бота, который управляет поведением формы верификации пользователя
"""
@client.event
async def on_verify_selected_member(ctx):
    pass

@client.command(
    name="verify",
    aliases=["vf", "verefy", "veref", 'verif'],
    brief="Верефикация пользователей"
)
async def verify(ctx, member: discord.Member=None, gender:str=None):
    if ctx.author.id not in support_con:
        return
    
    try:
        # Отрисовываем селект с выбором пользователя
        select_member_view = SelectMemberView(ctx.author, ctx.guild)
        select_member_msg = await ctx.send("Выберите пользователя для верификации", view=select_member_view)

        # Ждем выполнения выбора пользователя и удаляем предыдущее сообщение
        await client.wait_for("on_verify_selected_member")
        await select_member_msg.delete()

        # Добавляем выбор гендера для выбранного пользователя
        member = select_member_view.get_selected_member()
        verify_view = VerifyView(ctx, member, ctx.author, ctx.guild)
        verify_view_msg = await ctx.send(f"Выберите пол для пользователя {member.mention}", view=verify_view)

        # Ожидаем выбора пола и верификации, после чего удаляем сообщение
        await client.wait_for("on_verify_selected_member")
        await verify_view_msg.delete()
    except NoVerifiableMembers:
        await ctx.send("Не найдено пользователей для верификации")
    

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
    guild = member.guild.id
    datag = collguild.find_one({"_id": guild})
    af = after.channel.id
    if datag["verify"] == True:
        if after.channel is None:
            print("AFTER CHANNEL IS NONE")
        if member.id in support_con:
            print("MEMBER ID IN SUPPORT CONT")
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