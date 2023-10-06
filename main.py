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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!ph"))

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
async def ph(ctx,*args):
    function = args[0]
    if function == 'add':
        if len(args) <= 1:
            playertype = '2'
        else:
            playertype = "1" if args[1].lower() == 'hunter' or args[1].lower() == 'seeker' else "2"
        if len(args) <= 2:
            category = 'custom'
        else:
            category = args[2].lower()
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                try:
                    if functions.extract_extension(str(attachment.filename).upper()) in ['MP3','WAV','OGG','AAC','FLV']:
                        attachment_bytes = await attachment.read()
                        filename = f'{functions.extracttitle(attachment.filename)}.wav'
                        functions.upload(functions.Convert_Audio_to_Wav(attachment_bytes, attachment.filename),PUFFERPANEL_URL,filename,SERVER_ID,f'{SOUND_DIRECTORY}/{playertype}/{category}',PUFFERPANEL_USER,PUFFERPANEL_PASS)
                        await ctx.send(f'File: `{functions.extracttitle(attachment.filename)}` added')
                    elif functions.extract_extension(str(attachment.filename).upper()) in ['OGV', 'MP4', 'MPEG', 'AVI', 'MOV' ]:
                        print(attachment.filename)
                        attachment_bytes = await attachment.read()
                        print(f"Received attachment of {len(attachment_bytes)} bytes")
                        audio_bytes = functions.extract_audio_to_wav(attachment_bytes, attachment.filename)
                        audio_bytes = functions.Convert_Audio_to_Wav(attachment_bytes, attachment.filename)
                        filename = f'{functions.extracttitle(attachment.filename)}.wav'
                        audio_file = discord.File(BytesIO(audio_bytes), filename=filename)
                        functions.upload(audio_bytes,PUFFERPANEL_URL,filename,SERVER_ID,f'{SOUND_DIRECTORY}/{playertype}/{category}',PUFFERPANEL_USER,PUFFERPANEL_PASS)
                        await ctx.send(file=audio_file)
                        await ctx.send(f'File: `{functions.extracttitle(attachment.filename)}` added')
                    else:
                        await ctx.send(f'Unsupported file format: {functions.extracttitle(attachment.filename)}')
                except:
                    await ctx.send(f'Unrecoverable error proccesing file: {functions.extracttitle(attachment.filename)}')
        else:
            await ctx.send('Please supply an attachment. Command syntax is `!ph add Hunter/Hider Category`')
    elif function == 'stop':
        headers = functions.login_to_pufferpanel(PUFFERPANEL_URL,PUFFERPANEL_USER,PUFFERPANEL_PASS)
        functions.send_commands(headers,functions.get_plain_url(PUFFERPANEL_URL),SERVER_ID,[{"type":"stop"}])
    elif function == 'start':
        headers = functions.login_to_pufferpanel(PUFFERPANEL_URL,PUFFERPANEL_USER,PUFFERPANEL_PASS)
        functions.send_commands(headers,functions.get_plain_url(PUFFERPANEL_URL),SERVER_ID,[{"type":"start"}])
    else:
        await ctx.send('Available commands are `add`, `stop`, and `start`')

bot.run(DISCORD_TOKEN)