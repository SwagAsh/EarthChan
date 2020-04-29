import discord
import os
import flask
from keep_alive import keep_alive
from discord.ext import commands

earthchan = commands.Bot(command_prefix = ';')

token = os.environ.get("DISCORD_BOT_SECRET")

@earthchan.command()
async def load(ctx, extension):
    earthchan.load_extension(f'categories.{extension}')

@earthchan.command()
async def unload(ctx, extension):
    earthchan.unload_extension(f'categories.{extension}')

for filename in os.listdir('./categories'):
    if filename.endswith('.py'):
        earthchan.load_extension(f'categories.{filename[:-3]}')

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
earthchan.run(token)