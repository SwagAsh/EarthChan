import  discord
from discord.ext import commands
class StatsAndData(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(aliases = ['latency'])
    async def ping(self, ctx):
        steat = discord.Embed(
            title=':ping_pong: **Pong!**',
            description=f'{round(self.client.latency * 1000)}ms',
            colour=discord.Colour.purple()
        )
        await ctx.send(embed=steat)

    @commands.command(aliases = ['mcount'])
    async def membercount(self, ctx):
        mList = [x for x in ctx.guild.members]
        await ctx.send('This server has **' + str(len(mList)) + '** members')


def setup(client):
    client.add_cog(StatsAndData(client))
