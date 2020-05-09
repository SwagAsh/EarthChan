import discord
import sqlite3
import math
from discord.ext import commands

class Ranks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        db = sqlite3.connect('ranking.sqlite')
        cur = db.cursor()
        cur.execute(f"SELECT user_id FROM ranking WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
        result = cur.fetchone()
        if result is None:
            sql = ("INSERT INTO ranking(guild_id, user_id, exp, lvl) VALUES(?,?,?,?)")
            val = (message.guild.id, message.author.id, 2, 0)
            cur.execute(sql, val)
            db.commit()
        else:
            cur.execute(f"SELECT user_id, exp, lvl FROM ranking WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
            result1 = cur.fetchone()
            exp = int(result1[1])
            sql = ("UPDATE ranking SET exp = ? WHERE guild_id = ? and user_id = ?")
            val = (exp + 2, str(message.guild.id), str(message.author.id))
            cur.execute(sql, val)
            db.commit()

            cur.execute(f"SELECT user_id, exp, lvl FROM ranking WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
            result2 = cur.fetchone()

            xp_start = int(result2[1])
            lvl_start = int(result2[2])
            xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
            if xp_end < xp_start:
                await message.channel.send(f"GG, {message.author.mention}, you leveled up to level {lvl_start + 1}!")
                sql = ("UPDATE ranking SET lvl = ? WHERE guild_id = ? and user_id = ?")
                val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
                cur.execute(sql, val)
                db.commit()
                sql = ("UPDATE ranking SET exp = ? WHERE guild_id = ? and user_id = ?")
                val = (0, str(message.guild.id), str(message.author.id))
                cur.execute(sql, val)
                db.commit()
                cur.close()
                db.close()

    @commands.command(aliases = ['level'])
    async def rank(self, ctx, user:discord.User=None):
        if user is not None:
            rb = sqlite3.connect('ranking.sqlite')
            cur = rb.cursor()
            cur.execute(f"SELECT user_id, exp, lvl FROM ranking WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{user.id}'")
            res = cur.fetchone()
            if res is None:
                await ctx.send("User is not ranked")
            else:
                ranbed = discord.Embed(title=f"{user.name}'s Stats: ", colour=discord.Colour.teal())
                ranbed.set_thumbnail(url=f"{user.avatar_url}")
                ranbed.add_field(name='Level', value=f"{str(res[2])}")
                ranbed.add_field(name='EXP', value=f"{str(res[1])}")
                await ctx.send(embed=ranbed)
            cur.close()
            rb.close()
        elif user is None:
            rb = sqlite3.connect('ranking.sqlite')
            cur = rb.cursor()
            cur.execute(f"SELECT user_id, exp, lvl FROM ranking WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            res = cur.fetchone()
            if res is None:
                await ctx.send("You are not ranked yet")
            else:
                ranbed = discord.Embed(title=f"{ctx.message.author.name}'s Stats: ", colour=discord.Colour.teal())
                ranbed.set_thumbnail(url=f"{ctx.message.author.avatar_url}")
                ranbed.add_field(name='Level', value=f"{str(res[2])}")
                ranbed.add_field(name='EXP', value=f"{str(res[1])}")
                await ctx.send(embed=ranbed)
            cur.close()
            rb.close()




def setup(client):
    client.add_cog(Ranks(client))