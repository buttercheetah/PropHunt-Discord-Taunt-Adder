import discord.ext, functions, os
from discord.ext import commands
from io import BytesIO
TOKEN = "xxxx"

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())


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
                await ctx.send(f'File: `{functions.extracttitle(attachment.filename)}` added')
            elif functions.extract_extension(str(attachment.filename).upper()) in ['OGV', 'MP4', 'MPEG', 'AVI', 'MOV' ]:
                print(attachment.filename)
                attachment_bytes = await attachment.read()
                print(f"Received attachment of {len(attachment_bytes)} bytes")
                audio_bytes = functions.extract_audio_to_wav(attachment_bytes, attachment.filename)
                audio_file = discord.File(BytesIO(audio_bytes), filename=f'{functions.extracttitle(attachment.filename)}.wav')
                await ctx.send(file=audio_file)
            else:
                await ctx.send('Unsupported file format')
    else:
        await ctx.send('Please supply an attachment')

bot.run(TOKEN)