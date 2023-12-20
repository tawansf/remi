import datetime
import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.reactions = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
topic_pattern = "Lembrete Diário - {date}"
channel_configs = {}


async def create_daily_topic(channel):
    now = datetime.datetime.now()
    date_str = now.strftime('%d/%m/%Y %H:%M:%S')
    topic = topic_pattern.format(date=date_str)
    await channel.edit(topic=topic, content='Lembrete Diário')


@tasks.loop(hours=24, minutes=0, seconds=0)
async def daily_topic():
    for guild_id, channel_id in channel_configs.items():
        guild = bot.get_guild(guild_id)
        channel = guild.get_channel(channel_id)
        if channel is not None:
            await create_daily_topic(channel)


@bot.command(name='reminder')
async def set_reminder(ctx, channel: discord.TextChannel):
    guild_id = ctx.guild.id
    channel_id = channel.id
    channel_configs[guild_id] = channel_id
    daily_topic.start()
    await ctx.send(f'Lembrete configurado para cada dia no canal {channel.mention}.')


@bot.event
async def on_ready():
    print(f'O {bot.user.name} está funcionando!')


bot.run(TOKEN)
