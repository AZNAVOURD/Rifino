import asyncio

from discord import Activity, ActivityType

statuses = ["R", "RI", "RIF", "RIFI", "RIFIN", "RIFINO"]

@bot.event

async def on_ready():

    while True:

        for status in statuses:

            stream_name = status

            stream_url = "https://www.twitch.tv/gtav"

            activity = Activity(type=ActivityType.streaming, name=stream_name, url=stream_url)

            await bot.change_presence(activity=activity)

            await asyncio.sleep(0.5)

@bot.command()

async def play(ctx, name, link):

    # Validate if the link is a valid YouTube link

    if not youtube_dl.validateURL(link):

        await ctx.send('Invalid YouTube link!')

        return

    try:

        # Join the voice channel of the user who sent the message

        voice_channel = ctx.author.voice.channel

        if not voice_channel:

            await ctx.send('You need to join a voice channel first!')

            return

        # Join the voice channel and play the music

        voice_client = await voice_channel.connect()

        ydl_opts = {'format': 'bestaudio'}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(link, download=False)

            url2 = info['formats'][0]['url']

            voice_client.play(discord.FFmpegPCMAudio(url2))

        # Notify the user that the music is now playing

        await ctx.send(f'Now playing "{name}"')

        # Handle when the music finishes playing

        def check_queue():

            queue = ctx.voice_client

            if len(queue.channel.voice_states) == 1:

                asyncio.ensure_future(queue.disconnect())

        while ctx.voice_client.is_playing():

            check_queue()

        check_queue()

    except Exception as e:

        print('Error playing music:', e)

        await ctx.send('An error occurred while playing music!')

@bot.command()

async def skip(ctx):

    # Check if the bot is connected to a voice channel and is currently playing music

    if ctx.voice_client and ctx.voice_client.is_playing():

        # Skip the current music

        ctx.voice_client.stop()

        await ctx.send('Skipped the current music.')

    else:

        await ctx.send('No music is currently playing.')

@bot.command()

async def pause(ctx):

    # Check if the bot is connected to a voice channel and is currently playing music

    if ctx.voice_client and ctx.voice_client.is_playing():

        # Pause the current music

        ctx.voice_client.pause()

        await ctx.send('Paused the music.')

    else:

        await ctx.send('No music is currently playing.')

@bot.command()

async def resume(ctx):

    # Check if the bot is connected to a voice channel and the music is paused

    if ctx.voice_client and ctx.voice_client.is_paused():

        # Resume the paused music

        ctx.voice_client.resume()

        await ctx.send('Resumed the music.')

    else:

        await ctx.send('No music is currently paused.')

@bot.command()

async def stop(ctx):

    # Check if the bot is connected to a voice channel and is currently playing music

    if ctx.voice_client and ctx.voice_client.is_playing():

        # Stop the current music and disconnect from the voice channel

        ctx.voice_client.stop()

        await ctx.voice_client.disconnect()

        await ctx.send('Stopped the music and disconnected from the voice channel.')

    else:

        await ctx.send('No music is currently playing.')

@bot.command()

async def bot_help(ctx):

    help_message = """

    **Rx Music Bot Commands:**

    - `Rxplay [name] [link]` - Play music from a YouTube link.

    - `Rxskip` - Skip the current music.

    - `Rxpause` - Pause the current music.

    - `Rxresume` - Resume the paused music.

    - `Rxstop` - Stop the music and disconnect from the voice channel.

    - `Rxbot_help` - Show this help message.

    """

    await ctx.send(help_message)

