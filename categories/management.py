import discord
from discord.ext import commands

class ServerManagement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['cchannel'])
    async def createchannel(self, ctx, channeltype=None, *, name=None):
        if channeltype == 'Text' or channeltype == 'text':
            ncht = await ctx.guild.create_text_channel(name=name)
            await ctx.send('Created text channel :+1:')
        elif channeltype == 'voice' or channeltype == 'Voice':
            nchv = await ctx.guild.create_voice_channel(name=name)
            await ctx.send('Created voice channel :+1:')
        elif channeltype is None:
            await ctx.send('Please specify a channel type. (text or voice)')
        else:
            await ctx.send('Please specify a **valid** channel type. (text or voice)')
      #breaking point xd lol
        if name is None:
            await ctx.send('Please specify a channel name.')
        else:
            return 'Nothing is wrong'

    @commands.command(aliases = ['ccategory'])
    async def createcategory(self, ctx, *,category):
        ncog = await ctx.guild.create_category(name=category)
        await ctx.send('Created category :+1:')

def setup(client):
    client.add_cog(ServerManagement(client))