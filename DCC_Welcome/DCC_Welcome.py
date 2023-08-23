from discord.ext import tasks
from redbot.core import Config
import discord
import os
import asyncio
from discord.ext import commands
import json
from fuzzywuzzy import process
from redbot.core import commands


class DCC_WELCOME(commands.Cog):
    """Its all about Downtown Cab Co - Welcome System"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):

        guest_channel = self.bot.get_channel(301659110104104962)
        Join_Message = await guest_channel.send("""**Welcome to Downtown Cab co. {}.**\nPlease use command !name <FirstName> <LastName> into this channel to get access to Downtown social site.\nFor example: `!name James Cab`""".format(member.mention))
        try:
            await member.send(content="""**Welcome to Downtown Cab co. {}.**\nPlease use command !name <FirstName> <LastName> into <#301659110104104962> (#guests) channel to get access to Downtown social site.\nFor example: `!name James Cab`""".format(member.mention))
        except discord.errors.Forbidden:
            pass
        def check(m):
            return m.author == member
        await self.bot.wait_for('message', check=check)
        await Join_Message.delete()

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def name(self, ctx, *, name: str):

        """Use to change name on first join"""
        if len(ctx.author.roles) == 1:
            await ctx.author.edit(nick=name)
            await ctx.message.delete()
            message = await ctx.send("""Welcome to the Downtown social site, {}.\nIf you are here for an interview. Please type `!interview` to join in the waiting list.\nIf you are here as a visitor. Please type `!visitor` to join as visitor""".format(ctx.author.mention))
            def check(m):
                return m.author == ctx.author
            await self.bot.wait_for('message', check=check)
            await message.delete()
        else:
            await ctx.send("Hey {}, this is a single use command and you have used it in the past. Please contact a member of the management team to manually update your name.".format(ctx.author.mention))

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def interview(self, ctx):
        
        """Use to give interview role"""
        author = ctx.author
        interview_channel = self.bot.get_channel(353066751853854721)
        interviewee = ctx.guild.get_role(762663738179452940)
        if len(author.roles) == 1:
            await author.add_roles(interviewee)
            await ctx.message.delete()
            message = await interview_channel.send(content="""{}, thank you for joining the Downtown Cab Co discord! Please note this discord is strictly out of character, you will need to handle the interview process in character.""".format(author.mention))
            def check(m):
                return m.author == ctx.author
            await self.bot.wait_for('message', check=check)
            await message.delete()

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def visitor(self, ctx):

        """Use to join as visitor"""
        author = ctx.author
        shitposting_channel = self.bot.get_channel(409027176336195584)
        visitor = ctx.guild.get_role(317392264571650058)
        if len(author.roles) == 1:
            await author.add_roles(visitor)
            await ctx.message.delete()
            message = await shitposting_channel.send(content="""{}, You have been placed in Visitor Role""".format(author.mention))
            def check(m):
                return m.author == ctx.author
            await self.bot.wait_for('message', check=check)
            await message.delete()
