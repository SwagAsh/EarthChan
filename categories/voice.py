import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import shutil
import urllib.parse, urllib.request, re

class Music(commands.Cog):
    def __init__(self, client, queues = {}):
        self.client = client
        self.queues = queues

    @commands.command()
    async def join(self, ctx):
        try:
            global voice
            vchanl = ctx.message.author.voice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(vchanl)
            else:
                voice = await vchanl.connect()

            await voice.disconnect()

            if voice and voice.is_connected():
                await voice.move_to(vchanl)
            else:
                voice = await vchanl.connect()

            await ctx.send(f'Okay, i joined {vchanl}!')
        except AttributeError:
            print('bruh')
            await ctx.send('Your not even in a voice channel smh')

    @commands.command(aliases = ['leave'])
    async def disconnect(self, ctx):

        try:
            vchanl = ctx.guild.voice_client
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.disconnect()
                await ctx.send(f'Left {vchanl}')
            else:
                await ctx.send('I\'m not even in a voice channel smh')
        except AttributeError:
            await ctx.send('I\'m not in a channel and neither are you')

    @commands.command(aliases = ['p'])
    async def play(self, ctx, *,search):
        try:
            vchanl = ctx.message.author.voice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(vchanl)
            else:
                voice = await vchanl.connect()

        except AttributeError:
            await ctx.send('You need to be in a voice channel to play songs')
            return

        def check_queue():
            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    print('No more queued songs xD\n')
                    self.queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath('./EarthChan'))
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    print(f'Songs left in queue {still_q}')
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, "song.mp3")
                    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.1
                else:
                    self.queues.clear()
                    return
            else:
                self.queues.clear()
                print("No songs were queued before the last song\n")

        query_string = urllib.parse.urlencode({
            'search_query': search
        })
        htm_content = urllib.request.urlopen(
            'https://www.youtube.com/results?' + query_string
        )
        search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
        url = 'https://www.youtube.com/watch?v=' + search_results[0]
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            print('Song is being played, can\'t delete')
            await ctx.send('Song is being played, if you wan\'t to add to queue, use the ;addqueue command')
            return

        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            if Queue_infile is True:
                print('Old queue folder is gone')
                shutil.rmtree(Queue_folder)
        except:
            print('No old queue folder uwu')

        try:
            print('Readying the song...')
            await ctx.send('Song getting ready, please stand by.')

            voice = get(self.client.voice_clients, guild=ctx.guild)

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print('Download audio -_-\n')
                ydl.download([url])

            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    name = file
                    print(f'file renamed {file}\n')
                    os.rename(file, "song.mp3")

            voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.1

            await ctx.send(f'Playing `{name}` now...')
        except:
            await ctx.send('something went wrong')
        return

    @commands.command()
    async def pause(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("Paused the music")
        elif not voice:
            await ctx.send('I\'m not even in a music channel')
        else:
            await ctx.send('I\'m not playing any music right now')

    @commands.command()
    async def resume(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("Song is resumed")
        elif not voice:
            await ctx.send('I am not in a voice channel')
        else:
            await ctx.send('Music is already playing')

    @commands.command()
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        self.queues.clear()

        if (voice and voice.is_playing()) or (voice and voice.is_paused()):
            voice.stop()
            await ctx.send('Music stopped')
        elif not voice:
            await ctx.send('I\'m not even connected :facepalm:')
        else:
            await ctx.send('Song already stopped')

    @commands.command(aliases = ['addq'])
    async def addqueue(self, ctx, *, search):
        query_string = urllib.parse.urlencode({
            'search_query': search
        })
        htm_content = urllib.request.urlopen(
            'https://www.youtube.com/results?' + query_string
        )
        search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
        url = 'https://www.youtube.com/watch?v=' + search_results[0]
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is False:
            os.mkdir("Queue")
        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in self.queues:
                q_num += 1
            else:
                add_queue = False
                self.queues[q_num] = q_num

        queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
        await ctx.send("Song added to queue.")

def setup(client):
    client.add_cog(Music(client))