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


class ModActionView(View):
    def __init__(self, member: discord.Member):
        super().__init__()
        self.member = member

    @discord.ui.button(label='Замьютить', custom_id='mute')
    async def mute_button(self, interaction: discord.Interaction, button: Button):
        viewmute = mute(self.member)
        await interaction.response.send_message(f'Выберите действие для пользователя {self.member.mention}', view=viewmute)

    @discord.ui.button(label='Предупреждение', custom_id='warn')
    async def warn_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message('Пользователь получил предупреждение на 3 день.', ephemeral=True)


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

    


@client.command()
async def modaction(ctx: commands.Context, member: discord.Member):
    view = ModActionView(member)
    
    await ctx.send(f'Выберите действие для пользователя {member.mention}', view=view)




client.run("MTA4ODA2ODM1Njk0ODYyNzQ3OA.GY4Nd4.cRhDBwvCYN0dkC9LgBfcW_VYi8O1I_nDhTP1Tg")