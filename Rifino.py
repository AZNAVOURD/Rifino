import discord

from discord.ext import commands, tasks

import youtube_dl

bot = commands.Bot(command_prefix='Rx')

# List of streaming statuses

statuses = [

    "R",

    "RI",

    "RIF",

    "RIFI",

    "RIFIN",

    "RIFINO"

]

@bot.event

async def on_ready():

    print('Bot is ready!')

    change_status.start()

@tasks.loop(seconds=1)

async def change_status():

    # Get the current status index

    current_status_index = statuses.index(bot.activity.name)

    # Increment the index or reset to 0 if reached the end

    new_status_index = (current_status_index + 1) % len(statuses)

    # Update the streaming status

    await bot.change_presence(activity=discord.Streaming(name=statuses[new_status_index], url="https://www.twitch.tv/example"))

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

async def help(ctx):

    help_message = """

    **Rx Music Bot Commands:**

    - `Rxplay [name] [link]` - Play music from a YouTube link.

    - `Rxhelp` - Show this help message.

    """

    await ctx.send(help_message)

# Replace 'YOUR_DISCORD_BOT_TOKEN' with your actual Discord bot token

bot.run('YOUR_DISCORD_BOT_TOKEN')


