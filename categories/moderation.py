import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Okay. {member} has been kicked from the server.')

    @commands.command(aliases = ['foreverkick'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member} has been banned from the server. Bye Bye!')

    @commands.command(aliases = ['unforeverkick'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Ok! {user} can now rejoin the server!')
                return

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f':wastebasket: **Removed {amount} messages!** :thumbsup:')

    @commands.command(aliases = ['nickname'])
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *,nick=None):
        await member.edit(nick=nick)
        await ctx.send(f':white_check_mark: **Ok, {member} now has the nickname {nick}!** :pencil2:')

def setup(client):
    client.add_cog(Moderation(client))