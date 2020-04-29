import discord
import random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command()
    async def compliment(self, ctx, member: discord.Member):
        comps = [
            f'Hey, {member}, you are awesome!',
            f'You got nice lookin\' hair there, {member}.',
            f'{member}, you made my day!',
            f'Man, {member} has such a big brain!',
            f'You\'re probably the most wholesome person i met, {member}.',
            f'Thank you for existing, {member}.',
            f'The only thing that would make you any worse is if you weren\'t you, {member}',
            f'If there was a perfect person in this world, it just might be {member}'
        ]
        await ctx.send(random.choice(comps))

    @commands.command(aliases = ['askme', 'question'])
    async def ask(self, ctx, question):
        response = [
            'Yes :)',
            'No :|',
            'Of *course* :grin:',
            'Definitely :smile:',
            '__Highly Probable__ :grinning:',
            '*No chance* :unamused:',
            '**Don\'t keep your hopes high** :pensive:',
            'Never gonna happen!',
            'That\'s not possible! :laughing:',
            'I dunno ¯\\_(ツ)_/¯',
            'Ask later :sleeping:'
        ]
        await ctx.send(random.choice(response))

def setup(client):
    client.add_cog(Fun(client))