import discord.ext, functions, os
from discord.ext import commands
from io import BytesIO

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())


PUFFERPANEL_URL = functions.cleanurl(os.environ.get('PUFFERPANEL_URL', None))
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN', None)
PUFFERPANEL_USER = os.environ.get('PUFFERPANEL_USER', None)
PUFFERPANEL_PASS = os.environ.get('PUFFERPANEL_PASS', None)
SERVER_ID = os.environ.get('SERVER_ID', None)
SOUND_DIRECTORY = os.environ.get('SOUND_DIRECTORY', None)

@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!phadd"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    #if message.content == 'hello':
    #    await message.channel.send(f'Hi {message.author}')
    #if message.content == 'bye':
    #    await message.channel.send(f'Goodbye {message.author}')
    await bot.process_commands(message)

@bot.command()
async def phadd(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            if functions.extract_extension(str(attachment.filename).upper()) in ['MP3','WAV','OGG']:
                attachment_bytes = await attachment.read()
                upload(attachment_bytes,PUFFERPANEL_URL,attachment.filename,SERVER_ID,SOUND_DIRECTORY,PUFFERPANEL_USER,PUFFERPANEL_PASS)
                await ctx.send(f'File: `{functions.extracttitle(attachment.filename)}` added')
            elif functions.extract_extension(str(attachment.filename).upper()) in ['OGV', 'MP4', 'MPEG', 'AVI', 'MOV' ]:
                print(attachment.filename)
                attachment_bytes = await attachment.read()
                print(f"Received attachment of {len(attachment_bytes)} bytes")
                audio_bytes = functions.extract_audio_to_wav(attachment_bytes, attachment.filename)
                filename = f'{functions.extracttitle(attachment.filename)}.wav'
                audio_file = discord.File(BytesIO(audio_bytes), filename=filename)
                upload(audio_file,PUFFERPANEL_URL,filename,SERVER_ID,SOUND_DIRECTORY,PUFFERPANEL_USER,PUFFERPANEL_PASS)
                await ctx.send(file=audio_file)
            else:
                await ctx.send('Unsupported file format')
    else:
        await ctx.send('Please supply an attachment')

bot.run(DISCORD_TOKEN)