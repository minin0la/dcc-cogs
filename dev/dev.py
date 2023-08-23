from datetime import datetime
import asyncio
import textwrap
import discord
import inspect
from discord.ext import commands
from redbot.core import utils
from redbot.core import commands
from discord.ext import tasks
import aioschedule as schedule
import time
import requests
import json

class dev(commands.Cog):
    """Dev system!"""


    allenmessages = 0


    async def reset_limiter(self):
        self.allenmessages = 0


    async def morning_message(self):
        guild = discord.utils.get(self.bot.guilds, name="[ECRP] Downtown Cab Co.")
        channel = discord.utils.get(guild.text_channels, name='evelyn-daily') 
        
        try:
            r = requests.get("https://zenquotes.io/api/random")
            print(r)
      
            if r.status_code == 200:
                quotes = json.loads(r.content)
                print (quotes)
                quotes = quotes[0]
                author = quotes["a"]
                quote = quotes["q"]
                await channel.send("Good morning, team! \nRise and shine, and remember \"*{}*\"\n-{}".format(quote, author))
            else:
                print(r)
                await channel.send("Good morning, team!\nRise and shine, as you always do!\nUnfortuantely my quote service is down, perhaps <@!277399980052840448> would fix it?")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print( "Error has occured of type {}: {}\n{}".format(exc_type, exc_value, exc_traceback))
            await channel.send("Good morning, team!\nRise and shine, as you always do!\nUnfortuantely my quote service is down, perhaps <@!277399980052840448> can fix it?")



    def __init__(self, bot):
        self.bot = bot
        schedule.every().day.at("07:30").do(self.morning_message).tag("daily-tasks")
        schedule.every().day.at("00:00").do(self.reset_limiter).tag("daily-tasks")
        self._timer.start()

    #@commands.Cog.listener()
    async def on_message(self, message):
        if(message.author.id == 431556618489167882):
            if(self.allenmessages >= 5 or len(message.content) >= 225):
                await message.delete()
            else:
                self.allenmessages = self.allenmessages+1

    def cog_unload(self):
        self._timer.cancel()
        schedule.clear("daily-tasks")
        print("Unloaded bishes")

    @tasks.loop(seconds=0.1)
    async def _timer(self):
        await schedule.run_pending()

 #   @commands.has_any_role("COO", "Bot-Developer")
 #   @commands.command(pass_context=True, hidden=True, name="test")
 #   async def _test(self, ctx, *, user: discord.Member):
 #
 #      role = discord.utils.get(ctx.guild.roles, id=826749935365259276)

 #       for member in role.members:
 #           await member.remove_roles(role)

        
 #       await role.edit(name="%s of the week" % user.top_role.name, color=user.top_role.color, hoist=True)

 #      role_2 = user.top_role
 #       diff = 1

 #       while (role.position - role_2.position != 1):
 #           if(role.position - role_2.position > 0):
 #               diff = 1
 #           else:
 #               diff = -1

 #           await role.edit(position=role.position-diff)

 #       await user.add_roles(role)



    @commands.command(pass_context=True, hidden=True, name='eval')
    @commands.has_any_role("COO", "Bot-Developer")
    async def _eval(self, ctx, *, body: str):

       

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'self': self
        }

        env.update(globals())

        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await self.bot.say(self.get_syntax_error(e))

        func = env['func']
        await func()

  