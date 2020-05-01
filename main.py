import discord
import os
from discord.ext import commands

earthchan = commands.Bot(command_prefix = ';')

t = open("token.txt", "r")

@earthchan.command()
async def load(ctx, extension):
    earthchan.load_extension(f'categories.{extension}')

@earthchan.command()
async def unload(ctx, extension):
    earthchan.unload_extension(f'categories.{extension}')

for filename in os.listdir('./categories'):
    if filename.endswith('.py'):
        earthchan.load_extension(f'categories.{filename[:-3]}')

earthchan.run(t.read())
