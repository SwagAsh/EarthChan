import discord
import urllib.parse, urllib.request, re
from discord.ext import commands

class WebSearch(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ['yt'])
  async def youtube(self, ctx, *,search):
      query_string = urllib.parse.urlencode({
        'search_query': search
      })
      htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string
      )
      search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
      await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

def setup(client):
  client.add_cog(WebSearch(client))