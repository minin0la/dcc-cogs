import discord
from discord.ext import commands
from discord.ext import tasks
from redbot.core import Config
from redbot.core import commands
from redbot.core import utils
import os
import asyncio
import time
import logging
import datetime
import difflib
import random
import string


class DCC_BLACKLIST(commands.Cog):
    """Its all about Downtown Cab Co - Blacklist System"""

    def __init__(self, bot):
        self.bot = bot
        self.database = Config.get_conf(self, identifier=1)
        data = {"Blacklists": []}
        self.database.register_guild(**data)
        self.units = {"day": 86400, "week": 604800, "month": 2592000}
        self.announcer = Config.get_conf(None, identifier=1, cog_name="DCC_ANNOUNCER")

    #     self.check_blacklists.start()

    # def cog_unload(self):
    #     self.check_blacklists.cancel()

    @commands.group(pass_context=True, invoke_without_command=True)
    @commands.guild_only()
    async def dccblacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("!dccblacklist add/remove/show")

    @dccblacklist.command(pass_context=True)
    @commands.has_any_role(
        "CEO",
        "COO",
        "Bot-Developer",
        "General Manager",
        "Manager",
        "Assistant Manager",
        "CFO",
    )
    async def add(self, ctx, date: str, *, name: str):
        """!dccblacklist add <PERMANENT/DATE> <NAME>
        Example: !dccblacklist add 31/JAN/2020 Jasper Cab
        Example: !dccblacklist add PERMANENT Jasper Cab
        """
        # time_unit = time_unit.lower()
        # s = ""
        # if time_unit.endswith("s"):
        #     time_unit = time_unit[:-1]
        #     s = "s"
        # if not time_unit in self.units:
        #     await ctx.send("Invalid time unit. Choose days/weeks/month")
        #     return
        # if quantity < 1:
        #     await ctx.send("Quantity must not be 0 or negative.")
        #     return
        # if len(name) > 1960:
        #     await ctx.send("The name is too long.")
        #     return
        # seconds = self.units[time_unit] * quantity
        # future = int(time.time() + seconds)
        msg = await ctx.send("""What is the reason for blacklist?""")

        def check(m):
            return m.author == ctx.author

        reason = await self.bot.wait_for("message", check=check, timeout=120)
        async with self.database.guild(ctx.guild).Blacklists() as blacklists:
            blacklists.append(
                {"ID": msg.id, "NAME": name, "DATE": date, "REASON": reason.content}
            )

        Announcers = await self.announcer.guild(ctx.guild).Announcer()
        message_board_channel = self.bot.get_channel(
            669167190334767105
        )  # Get Message Board Channel
        Blacklists = await self.database.guild(ctx.guild).Blacklists()
        blacklist_message = ""

        Blacklists = sorted(Blacklists, key=lambda k: k["NAME"])

        # try:
        #     for x in Blacklists:
        #         blacklist_message = blacklist_message + "- {} ({})\n{}\n".format(
        #             x["NAME"], x["DATE"], x["REASON"]
        #         )
        # except:
        #     pass
        # blacklist_message = utils.chat_formatting.pagify(
        #     blacklist_message, delims="-", page_length=1000
        # )
        embed = discord.Embed(
            colour=discord.Colour(0xFF9700),
            timestamp=datetime.datetime.utcfromtimestamp(int(time.time())),
        )
        embed.set_thumbnail(
            url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg"
        )
        embed.set_author(
            name="Downtown Cab Co. Dispatcher",
            icon_url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg",
        )
        embed.set_footer(text="Posted by Evelyn")

        embed.add_field(
            name="**Radio Frequency**",
            value="```{}```".format(Announcers["MAIN_FREQ"]),
            inline=True,
        )
        embed.add_field(
            name="**Emergency Frequency**",
            value="```{}```".format(Announcers["EMERGENCY_FREQ"]),
            inline=True,
        )
        embed.add_field(
            name="**Passenger Blacklist as of {}**".format(
                datetime.date.today().strftime("%d/%b/%Y")
            ),
            value="",
            inline=False,
        )
        try:
            messageList = []
            for x in list(string.ascii_uppercase):
                blacklist_message_alpha = ""
                NameExists = False
                for y in Blacklists:
                    if y["NAME"].upper().startswith(x):
                        blacklist_message_alpha = (
                            blacklist_message_alpha
                            + "- {} ({})\n".format(y["NAME"], y["DATE"])
                        )
                        NameExists = True
                if NameExists == True:
                    messageList.append({"LETTER": x, "TEXT": blacklist_message_alpha})
            finalmessage = "```diff\n"
            charsum = 0
            for x in messageList:
                charsum = (
                    len(finalmessage)
                    + len("+ {} +\n".format(x["LETTER"]))
                    + len(x["TEXT"])
                )
                if (charsum) < 900:
                    finalmessage = (
                        finalmessage + "+ {} +\n".format(x["LETTER"]) + x["TEXT"]
                    )
                else:
                    finalmessage = finalmessage + "```"
                    embed.add_field(name="", value=finalmessage, inline=False)
                    finalmessage = (
                        "```diff\n" "+ {} +\n".format(x["LETTER"]) + x["TEXT"]
                    )
            if finalmessage != "```diff\n":
                finalmessage = finalmessage + "```"
                embed.add_field(name="", value=finalmessage, inline=False)
        except:
            pass
        try:
            the_announcer = await message_board_channel.fetch_message(
                Announcers["MSG_ID"]
            )
            await the_announcer.edit(embed=embed)
            await ctx.send(
                """Blacklist has been updated. (DMB message has been edited)"""
            )
        except:
            msg = await message_board_channel.send(embed=embed)
            await self.announcer.guild(ctx.guild).Announcer.set(
                {
                    "MSG_ID": msg.id,
                    "MAIN_FREQ": Announcers["MAIN_FREQ"],
                    "EMERGENCY_FREQ": Announcers["EMERGENCY_FREQ"],
                }
            )
            await ctx.send(
                """Blacklist has been updated. (New DMB message has been posted)"""
            )

    @dccblacklist.command(pass_context=True)
    @commands.has_any_role(
        "CEO",
        "COO",
        "Bot-Developer",
        "General Manager",
        "Manager",
        "Assistant Manager",
        "CFO",
    )
    async def remove(self, ctx, ID: int):
        """Remove a specific blacklist"""
        to_remove = []
        async with self.database.guild(ctx.guild).Blacklists() as blacklists:
            for blacklist in blacklists:
                try:
                    if blacklist["ID"] == ID:
                        to_remove.append(blacklist)
                except KeyError:
                    pass

            if not to_remove == []:
                for blacklist in to_remove:
                    blacklists.remove(blacklist)
                await ctx.send(
                    "The blacklist #{} has been deleted".format(blacklist["ID"])
                )
            else:
                await ctx.send("Nothing to delete")

        Announcers = await self.announcer.guild(ctx.guild).Announcer()
        message_board_channel = self.bot.get_channel(
            669167190334767105
        )  # Get Message Board Channel
        Blacklists = await self.database.guild(ctx.guild).Blacklists()
        blacklist_message = ""

        Blacklists = sorted(Blacklists, key=lambda k: k["NAME"])

        # try:
        #     for x in Blacklists:
        #         blacklist_message = blacklist_message + "- {} ({})\n{}\n".format(
        #             x["NAME"], x["DATE"], x["REASON"]
        #         )
        # except:
        #     pass
        blacklist_message = utils.chat_formatting.pagify(
            blacklist_message, delims="-", page_length=1000
        )
        embed = discord.Embed(
            colour=discord.Colour(0xFF9700),
            timestamp=datetime.datetime.utcfromtimestamp(int(time.time())),
        )
        embed.set_thumbnail(
            url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg"
        )
        embed.set_author(
            name="Downtown Cab Co. Dispatcher",
            icon_url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg",
        )
        embed.set_footer(text="Posted by Evelyn")

        embed.add_field(
            name="**Radio Frequency**",
            value="```{}```".format(Announcers["MAIN_FREQ"]),
            inline=True,
        )
        embed.add_field(
            name="**Emergency Frequency**",
            value="```{}```".format(Announcers["EMERGENCY_FREQ"]),
            inline=True,
        )
        embed.add_field(
            name="**Passenger Blacklist as of {}**".format(
                datetime.date.today().strftime("%d/%b/%Y")
            ),
            value="",
            inline=False,
        )
        try:
            messageList = []
            for x in list(string.ascii_uppercase):
                blacklist_message_alpha = ""
                NameExists = False
                for y in Blacklists:
                    if y["NAME"].upper().startswith(x):
                        blacklist_message_alpha = (
                            blacklist_message_alpha
                            + "- {} ({})\n".format(y["NAME"], y["DATE"])
                        )
                        NameExists = True
                if NameExists == True:
                    messageList.append({"LETTER": x, "TEXT": blacklist_message_alpha})
            finalmessage = "```diff\n"
            charsum = 0
            for x in messageList:
                charsum = (
                    len(finalmessage)
                    + len("+ {} +\n".format(x["LETTER"]))
                    + len(x["TEXT"])
                )
                if (charsum) < 900:
                    finalmessage = (
                        finalmessage + "+ {} +\n".format(x["LETTER"]) + x["TEXT"]
                    )
                else:
                    finalmessage = finalmessage + "```"
                    embed.add_field(name="", value=finalmessage, inline=False)
                    finalmessage = (
                        "```diff\n" "+ {} +\n".format(x["LETTER"]) + x["TEXT"]
                    )
            if finalmessage != "```diff\n":
                finalmessage = finalmessage + "```"
                embed.add_field(name="", value=finalmessage, inline=False)
        except:
            pass
        try:
            the_announcer = await message_board_channel.fetch_message(
                Announcers["MSG_ID"]
            )
            await the_announcer.edit(embed=embed)
        except:
            msg = await message_board_channel.send(embed=embed)
            await self.announcer.guild(ctx.guild).Announcer.set(
                {
                    "MSG_ID": msg.id,
                    "MAIN_FREQ": Announcers["MAIN_FREQ"],
                    "EMERGENCY_FREQ": Announcers["EMERGENCY_FREQ"],
                }
            )

    @dccblacklist.command(pass_context=True)
    @commands.has_any_role(
        "CEO",
        "COO",
        "Bot-Developer",
        "General Manager",
        "Manager",
        "Assistant Manager",
        "CFO",
    )
    async def show(self, ctx):
        """list all blacklist"""
        # number = 1
        # namelist = ""
        pages = []
        number = 0
        listnumber = 1
        async with self.database.guild(ctx.guild).Blacklists() as blacklists:
            for blacklist in blacklists:
                if number < 1:
                    embed = discord.Embed(
                        colour=discord.Colour(0xFF9700),
                        timestamp=datetime.datetime.utcfromtimestamp(int(time.time())),
                    )
                    embed.set_thumbnail(
                        url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg"
                    )
                    embed.set_author(
                        name="Downtown Cab Co. Dispatcher",
                        icon_url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg",
                    )
                    embed.set_footer(text="Posted by Evelyn")
                embed.add_field(
                    name="{}. {} (ID: {})".format(
                        listnumber, blacklist["NAME"], blacklist["ID"]
                    ),
                    value="```diff\n! Expired on: {}\n- Reason: {}```".format(
                        blacklist["DATE"], blacklist["REASON"]
                    ),
                    inline=False,
                )
                number = number + 1
                listnumber = listnumber + 1
                if number > 4:
                    pages.append(embed)
                    number = 0
            if number > 0:
                pages.append(embed)
            await utils.menus.menu(
                ctx, pages, utils.menus.DEFAULT_CONTROLS, timeout=60.0
            )
            #     namelist = namelist + "{}. **{}**,\n".format(str(number), blacklist["NAME"])
            #     namelist = namelist + "**Expired on:** {}\n".format(blacklist['DATE'])
            #     namelist = namelist + "**Reason:** {}\n".format(blacklist["REASON"])
            #     namelist = namelist + "**Blacklist ID:** {}\n\n".format(blacklist["ID"])
            #     number = number + 1
            # newname = utils.chat_formatting.pagify(text=namelist, delims=['\n\n'], shorten_by=8)
            # for x in newname:
            #     await ctx.send("{}".format(x))
