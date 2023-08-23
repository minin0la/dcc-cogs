from datetime import datetime
import asyncio

import discord
from discord.ext import commands
from redbot.core import utils
from redbot.core import commands

class DCC_RESIGN(commands.Cog):
    """Its all about Downtown Cab Co - Resign System"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, no_pm=True)
    @commands.has_any_role('Probationary Trainee', 'Trainee', 'suspended')
    async def resign(self, ctx, *, themessage):

        """Used to write a resign letter. Please write a message after the command."""


        server = ctx.message.guild
        visitorRole = ctx.guild.get_role(317392264571650058) # Get Visitor Role
        nitroRole = ctx.guild.get_role(588436644344889451) # Nitro role


        guild = ctx.guild
        author = ctx.author
        channel = guild.get_channel(367383714810036225) # Channel ID = evenlyn-office
        management = discord.utils.get(guild.text_channels, name='management') 
        await ctx.message.delete()
        date = datetime.now().strftime('%Y-%m-%d')
        embed = discord.Embed(title="To Downtown Cab Co. Management", colour=discord.Colour(
            0xFF0000), description="Dear Downtown Cab Co. Management,\n\nI would like to inform you that I am resigning from my position as {} for Downtown Cab Co., effective {}.\n\n{}\n\nSincerely,\n{}".format(author.top_role.mention, date, themessage, author.display_name))
        embed.set_thumbnail(
            url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
     
        await channel.send(embed=embed)
        await management.send(embed=embed)
        while author.top_role != server.default_role and author.top_role != nitroRole:
            print(author.top_role)
            try:
                await author.remove_roles(author.top_role)
            except discord.Forbidden:
                await ctx.send("I don't have permissions to suspend {}!".format(author.mention))
        await author.add_roles(visitorRole)