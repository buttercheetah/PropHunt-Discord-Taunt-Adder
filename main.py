import discord.ext
from discord.ext import commands
TOKEN = "xxxxx"

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        await message.channel.send(message)
    if message.content == 'hello':
        await message.channel.send(f'Hi {message.author}')
    if message.content == 'bye':
        await message.channel.send(f'Goodbye {message.author}')

    await bot.process_commands(message)

# Start each command with the @bot.command decorater
@bot.command()
async def square(ctx, arg): # The name of the function is the name of the command
    print(arg) # this is the text that follows the command
    await ctx.send(int(arg) ** 2) # ctx.send sends text in chat

@bot.command()
async def add(message):
    if message.attachments:
        for attachment in message.attachments:
            print(attachment.filename)
            attachment_bytes = await attachment.read()
            print(f"Received attachment of {len(attachment_bytes)} bytes")
    else:
        await message.send('Please supply an attachment')


bot.run(TOKEN)