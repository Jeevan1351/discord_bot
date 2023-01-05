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
        await message.channel.send(f'Hello! <@!{message.author.id}>')
    
    if "good morning" in message.content:
        await message.channel.send("Good morning!")
    await client.process_commands(message)


@client.command(description="Pings the bot")
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(description="Clears messages")
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command(description="Toss a coin")
async def toss(ctx):
    import random
    toss = random.randint(1, 2)
    if toss == 1:
        await ctx.send(file=discord.File('heads-coin-toss.gif'))
    else:
        await ctx.send(file=discord.File('tails-coin-toss.gif'))

class JoinDistance:
    def __init__(self, joined, created):
        self.joined = joined
        self.created = created

    @property
    def delta(self):
        return self.joined - self.created

class JoinDistanceConverter(commands.MemberConverter):
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        return JoinDistance(member.joined_at, member.created_at)

@client.command(description="Check how new a member is")
async def delta(ctx, *, member: JoinDistanceConverter):
    is_new = member.delta.days < 100
    if is_new:
        await ctx.send(f"Hey you're pretty new! {member.delta.days} days!")
    else:
        await ctx.send(f"Hm you're not so new. {member.delta.days} days!")

client.run(os.getenv('TOKEN'))