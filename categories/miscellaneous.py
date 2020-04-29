import discord
import random
from discord.ext import commands

class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def hello(self, ctx):
        hello = [
            'Hello',
            'Hi',
            'Kon\'nichiwa',
            'Hola',
            'Bonjour',
            'Guten Tag',
            'Zdravstvuyte'
        ]
        await ctx.send(':wave: **' + random.choice(hello) + f', {ctx.author.mention}!**')

    @commands.command()
    async def dm(self, ctx):
        await ctx.author.send('Sup. I slid into your DMs.')

    @commands.command(aliases = ['spamdm'])
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def nuke(self, ctx, member : discord.Member=None, *,message='nuke\'d'):
      if member is None:
        await ctx.send('Who do you want to nuke??')
        await nuke.reset_cooldown(ctx)

      await ctx.send(f':boom: Okay, nuking {member} now... :boom:')
    
      tactical = await member.create_dm()
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)
      await tactical.send(message)

      await ctx.send(f':raised_hand: Now wait **2 Hours** before using this command again, {ctx.author.mention} :alarm_clock:')
    @nuke.error
    async def nuke_error(self, ctx, error):   
        if isinstance(error, commands.CommandOnCooldown):
            msg = ':octagonal_sign: Hey, you can use this command again in **{:.0f}s**'.format(error.retry_after)
            await ctx.send(msg)
        else:
            raise error

    @commands.command(aliases = ['testingserver', 'testserver'])
    async def testing(self, ctx):
        await ctx.author.send(
            f'{ctx.author.mention} **Here is the link for the EarthChan Testing server!** https://discord.gg/dAm265y')
    
    @commands.command()
    async def invite(self, ctx, *, guild : discord.Guild):
      instinv = await self.client.create_invite(self.client.get_channel())
      await ctx.send('Here is your invite: ' + instinv)

def setup(client):
    client.add_cog(Miscellaneous(client))