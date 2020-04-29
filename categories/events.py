import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name='I have an illegal child??!?!'))
        print('Hello Senpai, i am wide awake!')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print(f'Someone deleted a message: {message}')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.client.get_channel(678308902038667318)
        embed = discord.Embed(title="Hello guys! EarthChan here.",
                              description="I am a multipurpose bot who is still a work in progress, but i can still do a lot of things! try using the ;help command to see what i can do! Some fun facts about me: I was programmed in python entirely by SwagAsh#3759. Pretty cool right?",
                              colour=discord.Colour.blurple())
        embed.set_author(name="EarthChan")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/695628979071352872/702575494679363604/2Q.png")
        await channel.send(embed=embed)

def setup(client):
    client.add_cog(Events(client))