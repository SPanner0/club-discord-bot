# The bot's main file, run here

import discord
from discord.ext import commands
import os
import sys
import json


# A config.json file is required that stores the prefix and the token before running
config_file = "config.json"

if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
else:
    print("No such file '{}'".format(config_file), file=sys.stderr)


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)


@bot.event
async def on_ready():
    print("------")
    print("Logged in as")
    print(bot.user.name)
    print("------")

    await loadCogs()


# Load the cogs
async def loadCogs():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            await bot.load_extension(f"cogs.{f[:-3]}")


@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send("Loaded extensions!")

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send("Unloaded extensions!")

@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send("Reloaded extensions!")



bot.run(config["token"])