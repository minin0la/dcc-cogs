from discord.ext import tasks
from redbot.core import Config
import discord
import os
import asyncio
from discord.ext import commands
import json
from fuzzywuzzy import process
from redbot.core import commands
import requests


class DCC_Fun(commands.Cog):
    """Its all about Downtown Cab Co - Fun System"""

    def __init__(self, bot):
        self.bot = bot
 
    @commands.command(pass_context=True)
    @commands.guild_only()
    async def fact(self, ctx):
        r = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        result = json.loads(r.content)["text"]
        await ctx.send("Did you know that... \n**{}**".format(result))


    @commands.command(pass_context=True)
    @commands.guild_only()
    async def feed(self, ctx, member: discord.Member):
        r = requests.get('https://nekos.life/api/v2/img/feed')
        result = json.loads(r.content)
        embed=discord.Embed(description="{} **feeds** {}".format(ctx.author.mention, member.mention), color=0x000000)
        embed.set_image(url=result['url'])
        embed.set_footer(text="GIF provided by nekos.life")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def kiss(self, ctx, member: discord.Member):
        r = requests.get('https://nekos.life/api/v2/img/kiss')
        result = json.loads(r.content)
        embed=discord.Embed(description="{} **kissed** {}".format(ctx.author.mention, member.mention), color=0x000000)
        embed.set_image(url=result['url'])
        embed.set_footer(text="GIF provided by nekos.life")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def hug(self, ctx, member: discord.Member):
        r = requests.get('https://nekos.life/api/v2/img/hug')
        result = json.loads(r.content)
        embed=discord.Embed(description="{} **hugged** {}".format(ctx.author.mention, member.mention), color=0x000000)
        embed.set_image(url=result['url'])
        embed.set_footer(text="GIF provided by nekos.life")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def cuddle(self, ctx, member: discord.Member):
        r = requests.get('https://nekos.life/api/v2/img/cuddle')
        result = json.loads(r.content)
        embed=discord.Embed(description="{} **cuddled** {}".format(ctx.author.mention, member.mention), color=0x000000)
        embed.set_image(url=result['url'])
        embed.set_footer(text="GIF provided by nekos.life")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def slap(self, ctx, member: discord.Member):
        r = requests.get('https://nekos.life/api/v2/img/slap')
        result = json.loads(r.content)
        embed=discord.Embed(description="{} **slapped** {}".format(ctx.author.mention, member.mention), color=0x000000)
        embed.set_image(url=result['url'])
        embed.set_footer(text="GIF provided by nekos.life")
        await ctx.send(embed=embed)

