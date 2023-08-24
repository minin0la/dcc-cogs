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


class BlacklistButton(discord.ui.View):
    def __init__(self, cog, config: Config):
        super().__init__(timeout=None)
        self.cog = cog
        self.config = config
        self.database = config.get_conf(self.cog, identifier=1)
        self.blacklists = config.get_conf(None, identifier=1, cog_name="DCC_BLACKLIST")

    @discord.ui.button(
        style=discord.ButtonStyle.primary,
        label="Show reasons",
        # emoji="",
        custom_id="buttonevent",
    )
    async def button_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        Blacklists = await self.blacklists.guild(
            interaction.client.get_guild(676076481260290079)
        ).Blacklists()
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
                            + "- {} ({})\n{}\n".format(
                                y["NAME"], y["DATE"], y["REASON"]
                            )
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
        await interaction.response.send_message("", ephemeral=True, embed=embed)


class DCC_ANNOUNCER(commands.Cog):
    """Its all about Downtown Cab Co - Announcer System"""

    def __init__(self, bot):
        self.bot = bot
        self.database = Config.get_conf(self, identifier=1)
        data = {"Announcer": []}
        self.database.register_guild(**data)
        self.blacklists = Config.get_conf(None, identifier=1, cog_name="DCC_BLACKLIST")

    @commands.command(pass_context=True, invoke_without_command=True)
    @commands.guild_only()
    @commands.has_any_role(
        "CEO",
        "COO",
        "Bot-Developer",
        "General Manager",
        "Manager",
        "Assistant Manager",
        "CFO",
    )
    async def refresh(self, ctx):
        """Used to refreshed the Announcer message"""

        Blacklists = await self.blacklists.guild(ctx.guild).Blacklists()
        Announcers = await self.database.guild(ctx.guild).Announcer()
        message_board_channel = self.bot.get_channel(
            669167190334767105
        )  # Get Message Board Channel
        blacklist_message = ""

        Blacklists = sorted(Blacklists, key=lambda k: k["NAME"])

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
            await the_announcer.delete()
        except:
            pass
        msg = await message_board_channel.send(
            embed=embed, view=BlacklistButton(self, self.database)
        )
        Announcers["MSG_ID"] = msg.id
        await self.database.guild(ctx.guild).Announcer.set(Announcers)
        await ctx.send("Announcer message has been refreshed!")

    @commands.command(pass_context=True, invoke_without_command=True)
    @commands.guild_only()
    @commands.has_any_role(
        "CEO",
        "COO",
        "Bot-Developer",
        "General Manager",
        "Manager",
        "Assistant Manager",
        "CFO",
    )
    async def radiofreq(self, ctx, main: str, emergency: str):
        Blacklists = await self.blacklists.guild(ctx.guild).Blacklists()
        Announcers = await self.database.guild(ctx.guild).Announcer()
        message_board_channel = self.bot.get_channel(
            669167190334767105
        )  # Get Message Board Channel
        blacklist_message = ""

        Blacklists = sorted(Blacklists, key=lambda k: k["NAME"])

        try:
            for x in Blacklists:
                blacklist_message = blacklist_message + "- {} ({})\n{}\n".format(
                    x["NAME"], x["DATE"], x["REASON"]
                )
        except:
            pass
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
            await self.database.guild(ctx.guild).Announcer.set(
                {
                    "MSG_ID": Announcers["MSG_ID"],
                    "MAIN_FREQ": main,
                    "EMERGENCY_FREQ": emergency,
                }
            )
            await ctx.send("Radio Frequency has been updated")
        except:
            msg = await message_board_channel.send(embed=embed)
            await self.database.guild(ctx.guild).Announcer.set(
                {"MSG_ID": msg.id, "MAIN_FREQ": main, "EMERGENCY_FREQ": emergency}
            )
            await ctx.send("Radio Frequency has been updated")
