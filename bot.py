import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix='_', intents=intents, discription="A bot that does stuff")
 
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
 
    if message.content.startswith('hi'):
        await message.channel.send('Hello!')
    
    if "good morning" in message.content:
        await message.channel.send("Good morning!")
    await client.process_commands(message)


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


client.run(os.getenv('TOKEN'))