import discord
import os
from discord.ext import commands
from redbot.core import commands
import asyncio
import datetime 

class DCC_GENERAL(commands.Cog):
    """Its all about Downtown Cab Co - General"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["bc"])
    async def businesscard(self, ctx):

        """Use to generate businesscard"""
        author = ctx.message.author
        got_data = False
        position = author.top_role.name
        if author.nick is not None:
            top_name = author.nick
            name = author.nick.replace(" ", "_")
        else:
            top_name = author.name
            name = author.name.replace(" ", "_")
        # await ctx.message.delete()
        def check(m):
            return m.author == ctx.author
        try:
            msg = await ctx.send("Can I have your photo please? (Send the URL: http://i.imgur.com/picture.png)")
            photo = await self.bot.wait_for('message', check=check, timeout=120)
            photo_content = photo.content
            await msg.delete()
            await photo.delete()
            got_data = True
        except asyncio.TimeoutError:
            got_data = False
            await ctx.send("Timeout! Please type !businesscard again")
        try:
            msg = await ctx.send("Can I have your number please?")
            number = await self.bot.wait_for('message', check=check, timeout=120)
            number_content = number.content
            await msg.delete()
            await number.delete()
            got_data = True
        except asyncio.TimeoutError:
            got_data = False
            await ctx.send("Timeout! Please type !businesscard again")
        if got_data is True:
            await ctx.send("Here is your businesscard, {}".format(author.mention))
            embed = discord.Embed(title="Downtown Cab Co",
                                url='http://downtowncab.co', color=10122825)
            embed.set_author(name="{}".format(
                top_name), icon_url='https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg')
            embed.set_thumbnail(url='{}'.format(photo_content))
            embed.add_field(name="Position:", value="{}".format(position), inline=False)
            embed.add_field(name="Phone Number: ", value="{}".format(
                number_content), inline=True)
            embed.add_field(name="Email: ", value="{}@downtowncab.co (({}))".format(
                name, author.mention), inline=True)
            await ctx.send(embed=embed)
    
    @commands.command(pass_context=True)
    @commands.has_any_role("Bot-Developer")
    async def oldestmember(self, ctx):
        guild = ctx.guild
        oldmembers = sorted(guild.members, key=lambda m: m.joined_at)
        for x in range(0, 19):
            await ctx.send("{}: Joined at {}".format(oldmembers[x].display_name, oldmembers[x].joined_at.strftime("%m/%d/%Y, %H:%M:%S")))

    @commands.command(pass_context=True)
    async def joindate(self, ctx, member: discord.Member):
        guild = ctx.guild
        await ctx.send("{}: Joined at {}".format(member.mention, member.joined_at.strftime("%m/%d/%Y, %H:%M:%S")))