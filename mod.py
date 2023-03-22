import discord
import asyncio
from discord.utils import get
from discord.ext import commands
from discord.ui import View, Select, Button
from datetime import datetime, timedelta
from pymongo import MongoClient
import configparser
from typing import List



conf = configparser.ConfigParser()
conf.read('config.ini')

# Забираем данные из конфигурации (int-списки принудительно кастуем в List[int])
support_con:List[int] = [int(x) for x in conf.get('Settings', 'Support').split(',')]
prefix = conf.get('Settings', 'Prefix')
v_c:List[int] = [int(x) for x in conf.get('Settings', 'v_c').split(',')]


client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
cluster = MongoClient("mongodb://127.0.0.1:27017")
collguild = cluster.argand.guild
collmod = cluster.argand.mod_role
ButtonStyle = discord.ButtonStyle

@client.event
async def on_ready():
    print("Bot is ready.")

    # Запускаем циклическую функцию проверки через client.loop.create_task()
    client.loop.create_task(check_punishments())

async def check_punishments():
    while True:
        print("Запускаем циклическую функцию проверки")
        # Получаем текущую дату и время
        current_time = datetime.now()
        # Ищем все записи в коллекции collmod, где дата окончания наказания меньше текущей даты и времени
        expired_punishments = collmod.find({'expire_at': {'$lt': current_time}})
        # Проходимся по каждой записи и удаляем роль у пользователя
        for punishment in expired_punishments:
            # Получаем объект пользователя и роль
            guild = client.get_guild(1056206116201168947)
            member = await guild.fetch_member(punishment['user_id'])
            role = discord.utils.get(guild.roles, id=punishment['role_id'])
            # Удаляем роль у пользователя
            await member.remove_roles(role)
            # Удаляем запись из коллекции collmod
            collmod.delete_one({'_id': punishment['_id']})
        # Ждем 60 секунд
        await asyncio.sleep(60)

class mute(View):
    def __init__(self, member: discord.Member):
        super().__init__()
        self.member = member

    @discord.ui.button(label='10 мин', custom_id='mute10')
    async def mute_button10(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Мут')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=0.00694)
        })

        await interaction.response.send_message('Пользователь получил мут на 10 минут.', ephemeral=True)

    @discord.ui.button(label='30 мин', custom_id='mute30')
    async def mute_button30(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Мут')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=0.02083)
        })

        await interaction.response.send_message('Пользователь получил мут на 30 минут.', ephemeral=True)

    @discord.ui.button(label='60 мин', custom_id='mute60')
    async def mute_button60(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Мут')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=0.04166)
        })

        await interaction.response.send_message('Пользователь получил мут на 60 минут.', ephemeral=True)

    @discord.ui.button(label='3 часа', custom_id='mute3')
    async def mute_button3(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Мут')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=0.125)
        })

        await interaction.response.send_message('Пользователь получил мут на 3 часа.', ephemeral=True)

    @discord.ui.button(label='5 часов', custom_id='mute5')
    async def mute_button5(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Мут')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=0.20833)
        })

        await interaction.response.send_message('Пользователь получил мут на 5 часов.', ephemeral=True)

    @discord.ui.button(label='10 часов', custom_id='mute10h')
    async def mute_button10h(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Мут')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=0.41666)
        })

        await interaction.response.send_message('Пользователь получил мут на 10 часов.', ephemeral=True)

    @discord.ui.button(label='1 день', custom_id='mute1d')
    async def mute_button1d(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Мут')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=1)
        })

        await interaction.response.send_message('Пользователь получил мут на 1 день.', ephemeral=True)

    @discord.ui.button(label='3 дня', custom_id='mute3d')
    async def mute_button3d(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Мут')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=3)
        })

        await interaction.response.send_message('Пользователь получил мут на 3 деня.', ephemeral=True)

    @discord.ui.button(label='5 дней', custom_id='mute5d')
    async def mute_button5d(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Мут')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=5)
        })

        await interaction.response.send_message('Пользователь получил мут на 5 дней.', ephemeral=True)

class worm(View):
    def __init__(self, member: discord.Member):
        super().__init__()
        self.member = member

    @discord.ui.button(label='1 день', custom_id='warm1')
    async def mute_button1(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Предупреждение')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=1)
        })
        await interaction.response.send_message('Пользователь получил предупреждение на 1 день.', ephemeral=True)

    @discord.ui.button(label='3 дня', custom_id='warm3')
    async def mute_button3(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Предупреждение')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=3)
        })
        await interaction.response.send_message('Пользователь получил предупреждение на 3 дня.', ephemeral=True)

    @discord.ui.button(label='5 дней', custom_id='warm5')
    async def mute_button5(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Предупреждение')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=5)
        })
        await interaction.response.send_message('Пользователь получил предупреждение на 5 дней.', ephemeral=True)

    @discord.ui.button(label='7 дней', custom_id='warm7')
    async def mute_button7(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Предупреждение')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=7)
        })
        await interaction.response.send_message('Пользователь получил предупреждение на 7 дней.', ephemeral=True)

    @discord.ui.button(label='15 дней', custom_id='warm15')
    async def mute_button15(self, interaction: discord.Interaction, button: Button):
        collmod = cluster.argand.mod_role
        # Получение временной роли для предупреждения
        role = get(self.member.guild.roles, name='Предупреждение')
        # Выдача роли пользователю
        await self.member.add_roles(role)
        # Сохранение информации о временной роли в базе данных
        collmod.insert_one({
            'user_id': self.member.id,
            'role_id': role.id,
            'expire_at': datetime.now() + timedelta(days=15)
        })
        await interaction.response.send_message('Пользователь получил предупреждение на 15 дней.', ephemeral=True)


class ModActionView(View):
    def __init__(self, member: discord.Member):
        super().__init__()
        self.member = member

    @discord.ui.button(label='Замьютить', custom_id='mute')
    async def mute_button(self, interaction: discord.Interaction, button: Button):
        viewmute = mute(self.member)
        await interaction.response.send_message(f'Выберите время мьюта для пользователя {self.member.mention}', view=viewmute)

    @discord.ui.button(label='Предупреждение', custom_id='warn')
    async def warn_button(self, interaction: discord.Interaction, button: Button):
        viewwarm = worm(self.member)
        await interaction.response.send_message(f'Выберите время предупреждения для пользователя {self.member.mention}', view=viewwarm)


    @discord.ui.button(label='Кикнуть', custom_id='kick', style=discord.ButtonStyle.danger)
    async def kick_button(self, interaction: discord.Interaction, button: Button):
        # Забанить пользователя
        await self.member.kick(reason='Пользователь викинут администратором')
        await interaction.response.send_message(f'{self.member.display_name} был забанен.', ephemeral=True)
    
    @discord.ui.button(label='Забанить', custom_id='ban', style=discord.ButtonStyle.danger)
    async def ban_button(self, interaction: discord.Interaction, button: Button):
        # Забанить пользователя
        await self.member.ban(reason='Бан выдан администратором')

        await interaction.response.send_message(f'{self.member.display_name} был забанен.', ephemeral=True)

    @discord.ui.button(label='Разбанить', custom_id='unban', style=discord.ButtonStyle.danger)
    async def unban_button(self, interaction: discord.Interaction, button: Button):
        # Забанить пользователя
        await self.member.unban(reason='Бан снят администратором')
        await interaction.response.send_message(f'{self.member.display_name} был забанен.', ephemeral=True)


@client.command(
    name="modaction",
    aliases=["mod", "action", "act", 'мод'],
    brief="Выполнить адмнистративные действия для пользователя",
)
async def modaction(ctx: commands.Context, member: discord.Member):
    print(member.id)
    if ctx.author.id in support_con:
        view = ModActionView(member)
        await ctx.send(f'Выберите действие для пользователя {member.mention}', view=view)
    else:
        ctx.send("У вас недостаточно прав для использования этой команды")



client.run("MTA4ODA2ODM1Njk0ODYyNzQ3OA.GY4Nd4.cRhDBwvCYN0dkC9LgBfcW_VYi8O1I_nDhTP1Tg")