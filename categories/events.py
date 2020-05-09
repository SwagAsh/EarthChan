import discord
import sqlite3
from discord.ext import commands
from discord.utils import get

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Streaming(name='how to make discord bot', url='https://www.youtube.com/channel/UCYqx_6tN5HD6q7ciALF9T9g'))
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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome = sqlite3.connect('welcome.sqlite')
        cur = welcome.cursor()
        cur.execute(f"SELECT channel_id FROM welcome WHERE guild_id = {member.guild.id}")
        result = cur.fetchone()
        if result is None:
            return
        else:
            cur.execute(f"SELECT msg FROM welcome WHERE guild_id = {member.guild.id}")
            resone = cur.fetchone()
            if resone is not None:
                members = len(list(member.guild.members))
                mention = member.mention
                user = member.name
                server = member.guild
                smsg = str(resone[0]).format(members=members, mention=mention, user=user, guild=server)
            else:
                pass
            cur.execute(f"SELECT role_id FROM welcome WHERE guild_id = {member.guild.id}")
            result2 = cur.fetchone()
            role = get(member.guild.roles, id=int(result2[0]))
            if role is not None:
                await member.add_roles(role)
            else:
                pass
        chanl = self.client.get_channel(id=int(result[0]))
        try:
            await chanl.send(smsg)
        except:
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        db = sqlite3.connect('leave.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM leave WHERE guild_id = {member.guild.id}")
        res = cursor.fetchone()
        if res is None:
            return
        else:
            cursor.execute(f"SELECT message FROM leave WHERE guild_id = {member.guild.id}")
            res1 = cursor.fetchone()
            if res1 is not None:
                user = member.name
                members = len(list(member.guild.members))
                mention = member.mention
                server = member.guild
                leaveMessage = str(res1[0]).format(members=members, mention=mention, user=user, guild=server)
            else:
                return
        channel = self.client.get_channel(id=int(res[0]))
        await channel.send(leaveMessage)

    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx):
        await ctx.send('Welcome message setup commands: \n;welcome channel <#channel> (sets up the channel the message will be set)\n;welcome message <message> (sets a custom welcome message)\n;welcome role (Sets an automatic welcome role)')
    @welcome.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            wb = sqlite3.connect('welcome.sqlite')
            cursor = wb.cursor()
            cursor.execute(f"SELECT channel_id FROM welcome WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO welcome(guild_id, channel_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Welcome channel set to {channel.mention}")
            elif result is not None:
                sql = ("UPDATE welcome SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"Welcome channel set to {channel.mention}")
            cursor.execute(sql, val)
            wb.commit()
            cursor.close()
            wb.close()
    @welcome.command()
    async def message(self, ctx, *, message):
        if ctx.message.author.guild_permissions.manage_messages:
            wel = sqlite3.connect('welcome.sqlite')
            cursor = wel.cursor()
            cursor.execute(f"SELECT msg FROM welcome WHERE guild_id = {ctx.guild.id}")
            rslt = cursor.fetchone()
            if rslt is None:
                sequel = ("INSERT INTO welcome(guild_id, msg) VALUES(?,?)")
                value = (ctx.guild.id, message)
                await ctx.send(f'Welcome message set to \'{message}\'')
            elif rslt is not None:
                sequel = ("UPDATE welcome SET msg = ? WHERE guild_id = ?")
                value = (message, ctx.guild.id)
                await ctx.send(f'Welcome message set to \'{message}\'')
            cursor.execute(sequel, value)
            wel.commit()
            cursor.close()
            wel.close()
    @welcome.command()
    async def role(self, ctx, *, roleName:str):
        if ctx.message.author.guild_permissions.manage_roles:
            db = sqlite3.connect('welcome.sqlite')
            cur = db.cursor()
            cur.execute(f"SELECT role_id FROM welcome WHERE guild_id = {ctx.guild.id}")
            role = get(ctx.guild.roles, name=roleName)
            if role is None:
                newrole = await ctx.guild.create_role(name=roleName, reason=None)
                getnewrole = get(ctx.guild.roles, name=newrole.name)
                roleId = getnewrole.id
                sql = ("INSERT INTO welcome(guild_id, role_id) VALUES(?,?)")
                val = (ctx.guild.id, roleId)
                await ctx.send(f'Welcome role set to {roleName}')
            elif role is not None:
                roleId = role.id
                sql = ("UPDATE welcome SET role_id = ? WHERE guild_id = ?")
                val = (roleId, ctx.guild.id)
                await ctx.send(f'Welcome role set to {roleName}')
            cur.execute(sql, val)
            db.commit()
            cur.close()
            db.close()

    @commands.group(invoke_without_command=True, aliases = ['mleave'])
    async def memberleave(self, ctx):
        await ctx.send('Leave message commands :\n;memberleave channel <#channel> (sets the channel the message will be sent in)\n;memberleave message <message> (Sets the leave message)')
    @memberleave.command()
    async def channel(self, ctx, channel:discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            leave = sqlite3.connect('leave.sqlite')
            cleave = leave.cursor()
            cleave.execute(f"SELECT channel_id FROM leave WHERE guild_id = {ctx.guild.id}")
            clesult = cleave.fetchone()
            if clesult is None:
                clesql = ("INSERT INTO leave(guild_id, channel_id) VALUES(?,?)")
                cleaval = (ctx.guild.id, channel.id)
                await ctx.send(f'Leave message channel set to {channel}')
            else:
                clesql = ("UPDATE leave SET channel_id = ? WHERE guild_id = ?")
                cleaval = (channel.id, ctx.guild.id)
                await ctx.send(f'Leave message channel set to {channel}')
            cleave.execute(clesql, cleaval)
            leave.commit()
            cleave.close()
            leave.close()
    @memberleave.command()
    async def message(self, ctx, *, message):
        if ctx.message.author.guild_permissions.manage_messages:
            lb = sqlite3.connect('leave.sqlite')
            curser = lb.cursor()
            curser.execute(f"SELECT message FROM leave WHERE guild_id = {ctx.guild.id}")
            curesult = curser.fetchone()
            if curesult is None:
                cursql = ("INSERT INTO leave(guild_id, message) VALUES(?,?)")
                valuee = (ctx.guild.id, message)
                await ctx.send(f'Leave message set to \'{message}\'')
            else:
                cursql = ("UPDATE leave SET message = ? WHERE guild_id = ?")
                valuee = (message, ctx.guild.id)
                await ctx.send(f'Leave message set to \'{message}\'')
            curser.execute(cursql, valuee)
            lb.commit()
            curser.close()
            lb.close()

def setup(client):
    client.add_cog(Events(client))
