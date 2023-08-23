from datetime import datetime
import asyncio
import textwrap
import discord
import inspect
from redbot.core import Config
from discord.ext import commands
from redbot.core import utils
from redbot.core import commands
from discord.ext import tasks
import aioschedule as schedule
import time
import requests
import json
import sys

from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions


from timezonefinder import TimezoneFinder
import copy


from geopy import geocoders
from datetime import datetime, timedelta
from tzwhere import tzwhere
from pytz import timezone
import pytz
from dateutil import parser



class DCC_SCHEDULE(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.gn = geocoders.GeoNames(username='dccbot')
        self.database = Config.get_conf(self, identifier=1)

        self.message_db = Config.get_conf(self, identifier=2)
        self.message_db.register_guild(**{"Messages":[]})

     
        data = {"Scheduler": []}
        self.database.register_guild(**data)
        

        self.messages = []
        self._timer.start()
        self.reminder_values = [["1 hour", 3600], ["30 minutes", 1800], ["10 minutes", 600]]
        self.emojis = ["1️⃣", "2️⃣", "3️⃣"]
        asyncio.create_task(self.on_ready())
    
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print("RAN")
        for guild in self.bot.guilds: 
            await self.load_messages(guild)
            print("Loading messages for {}".format(guild.id))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if(payload.member is None):
            if self.bot.get_user(payload.user_id).bot is False:
                print(self.bot.get_user(payload.user_id))
                DM_channel = self.bot.get_channel(payload.channel_id)
                message = await DM_channel.fetch_message(payload.message_id)

                guild_id = message.embeds[0].url.split("/")[4]
                channel_id = message.embeds[0].url.split("/")[5]
                message_id = message.embeds[0].url.split("/")[6]
                print(message_id)
                


                msg_obj = await self.find_message_by_id(int(message_id))
               
                
                await DM_channel.send("{} reminder has been set!".format(self.reminder_values[self.emojis.index(payload.emoji.name)][0]))

                ((list(filter(lambda x: x[0].id == payload.user_id, msg_obj[2])))[0])[1].append(self.reminder_values[self.emojis.index(payload.emoji.name)][1])
                

                #print((list(filter(lambda x: self.reminder_values[self.emojis.index(payload.emoji.name)][1] in x[1], msg_obj[2]))))

         
            return

        if payload.member.bot:
            return
    

        msg_object = await self.find_message_by_id(payload.message_id)

        if(msg_object is not None):

            print(payload.guild_id)
            Scheduler = await self.database.guild(payload.member.guild).Scheduler()

 

            channel = discord.utils.get(payload.member.guild.channels, id=payload.channel_id)
            
            actual_message = await channel.fetch_message(payload.message_id)

            print(actual_message.embeds[0].fields)

            try:
                loc_tz = timezone(Scheduler[str(payload.member.id)])
            except:
                await payload.member.send("You haven't set your timezone! Please set your timezone with !tz and your city, example: ```!tz Amsterdam```")
                await actual_message.remove_reaction(payload.emoji.name, payload.member)
                return

        
            if(payload.emoji.name == "✅"):
                self.add_member(msg_object, payload.member)
                await self.update_message(actual_message, msg_object)

                embed = discord.Embed(colour=discord.Colour(0xff9700), title=msg_object[3][0], description=msg_object[3][1], url="https://discord.com/channels/{}/{}/{}".format(msg_object[0].guild.id, msg_object[0].channel.id, msg_object[0].id))
                embed.set_thumbnail(url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
                embed.set_author(name="Downtown Cab Co. Dispatcher", icon_url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
                embed.set_footer(text="Press 1️⃣ to set 1 hour reminder, press 2️⃣ to set a 30 minute remider, press 3️⃣ to set a 10 minute reminder.")
                embed.add_field(name="Where?", value="```{}```".format(msg_object[3][2]), inline=True)
                embed.add_field(name="When? (Your time)", value="```{}```".format(msg_object[1].astimezone(loc_tz).strftime("%H:%M:%S - %d/%b/%Y")), inline=True)
                

                msg_to_user = await payload.member.send(embed=embed)
                start_adding_reactions(msg_to_user, self.emojis)

                # embed =  actual_message.embeds[0]
                # embed.set_field_at(2, name="Attendees", value="Korec", inline=False)
                # await actual_message.edit(embed=embed)


            if(payload.emoji.name == "🌐"):

                now = datetime.now()
                timestamp = datetime.timestamp(now)
                diff = msg_object[1].timestamp() - timestamp


                time = msg_object[1].astimezone(loc_tz)
                await payload.member.send("Converted time should be: {}".format(time.strftime("%H:%M:%S - %d/%b/%Y")))
                await actual_message.remove_reaction("🌐", payload.member)
        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        guild = discord.utils.get(self.bot.guilds, id=payload.guild_id)


        if(guild is None):

            if self.bot.get_user(payload.user_id).bot is False:
                print(self.bot.get_user(payload.user_id))
                DM_channel = self.bot.get_channel(payload.channel_id)
                message = await DM_channel.fetch_message(payload.message_id)

                guild_id = message.embeds[0].url.split("/")[4]
                channel_id = message.embeds[0].url.split("/")[5]
                message_id = message.embeds[0].url.split("/")[6]
                print(message_id)
                


                msg_obj = await self.find_message_by_id(int(message_id))

                await DM_channel.send("{} reminder has been removed!".format(self.reminder_values[self.emojis.index(payload.emoji.name)][0]))

                ((list(filter(lambda x: x[0].id == payload.user_id, msg_obj[2])))[0])[1].remove(self.reminder_values[self.emojis.index(payload.emoji.name)][1])

            return

        payload.member = discord.utils.get(guild.members, id=payload.user_id)

        if payload.member.bot:
            return
    

        msg_object = await self.find_message_by_id(payload.message_id)

        if(msg_object is not None):

        
            Scheduler = await self.database.guild(guild).Scheduler()

            channel = discord.utils.get(guild.channels, id=payload.channel_id)
            actual_message = await channel.fetch_message(payload.message_id)

            print(actual_message.embeds[0].fields)

            loc_tz = timezone(Scheduler[str(payload.member.id)])
        

        
            if(payload.emoji.name == "✅"):
                self.remove_member(msg_object, payload.member)
                await self.update_message(actual_message, msg_object)
                print(msg_object)
                # embed =  actual_message.embeds[0]
                # embed.set_field_at(2, name="Attendees", value="Korec", inline=False)
                # await actual_message.edit(embed=embed)

    def cog_unload(self):
        self._timer.cancel()


    def add_member(self, msg_obj, member):

        hasFound = False

        for user in msg_obj[2]:
            if(user[0] == member):
                hasFound = True

        if(hasFound == False):
            msg_obj[2].append([member, []])

    def remove_member(self, msg_obj, member):
        try:

            

            msg_obj[2].remove(((list(filter(lambda x: x[0] == member, msg_obj[2]))))[0])
        except:
            return
     

    @tasks.loop(seconds=0.1)
    async def _timer(self):
        
        for message in self.messages:

            
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            diff = message[1].timestamp() - timestamp


           

            for reminder in self.reminder_values:
                if(diff <= reminder[1] and reminder[1] not in message[4]):  
                    message[4].append(reminder[1])
                    for user in ((list(filter(lambda x: reminder[1] in x[1], message[2])))):
                        try:
                            await user[0].send("{} will begin in {}".format(message[3][0], reminder[0]))
                        except:
                            print("Something broke, rip!")

   

            # if(diff - 600 < 0.1 and diff >= 600):
            #     for user in message[2]:
            #         await user[0].send("10 minutes to event!")
            

            # if(diff - 600 < 0.1 and diff >= 600):
            #     for user in message[2]:
            #         await user[0].send("10 minutes to event!")
            

            # if(diff - 600 < 0.1 and diff >= 600):
            #     for user in message[2]:
            #         await user[0].send("10 minutes to event!")

            if(diff < 0):
                for user in message[2]:
                    try:
                        await user[0].send("{} is starting now!".format(message[3][0]))
                    except:
                        print("Something broke x2")
                        
                await self.remove_message(message)

           # print(diff)
            
    
    async def remove_message(self, msg_obj):
        self.messages.remove(msg_obj)
        guild = msg_obj[0].guild
        try:
            await msg_obj[0].delete()
        except:
            print("Already deleted")
        await self.save_messages(guild)

    async def update_message(self, actual_message, msg_obj):
        embed =  actual_message.embeds[0]
        guild = msg_obj[0].guild
        print(embed)
        Attendees = ""
        if(len(msg_obj[2])<1):
            Attendees = "None"

        for person in msg_obj[2]:
            Attendees += person[0].mention + "\n"

        embed.set_field_at(2, name="Attendees", value="{}".format(Attendees), inline=False)
        await actual_message.edit(embed=embed)
        await self.save_messages(guild)

    @commands.command(pass_context=True, aliases=["scd"])
    @commands.guild_only()
    @commands.has_any_role("CEO", "COO", "Human Resources Director", "Human Resources Representative", "Team Leader", "Bot-Developer", "General Manager", "Manager", "Assistant Manager", "Dispatcher")
    async def schedule(self, ctx, *, args:str):

        """ The arguments should be split by a "|", 4 are required in the following order Name of the Event, Description, Location and Time. Example ```!scd DCC's Pizza Party | Some proper pizza party | DCC Office | 10/MAR/2021 - 21:00```  """

        await ctx.message.delete()

        args = args.split("|")
        
        name = args[0]
        desc = args[1]
        loc = args[2]
        time = args[3]
        
        
        await self.add_message(ctx, time, [name, desc, loc], ctx.author)
    

        # msg = await ctx.send("React to me!")
        # emojis = ReactionPredicate.ALPHABET_EMOJIS[:3]
        # start_adding_reactions(msg, emojis)


    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):

        msg_obj = await self.find_message_by_id(payload.cached_message.id)

        if msg_obj != None:
            for user in msg_obj[2]:
                await user[0].send("{} has been cancelled!".format(msg_obj[3][0]))
            await self.remove_message(msg_obj)
            return

        
    

    def Cloning(self, li1): 
        li_copy = [] 
        for entry in li1:
            li_copy.append(entry)
        return li_copy

    @commands.command(pass_context=True)
    @commands.has_any_role("CEO", "COO", "Human Resources Director", "Human Resources Representative", "Team Leader", "Bot-Developer", "General Manager", "Manager", "Assistant Manager", "Dispatcher")
    async def clearmsg(self, ctx):
         await self.message_db.guild(ctx.message.guild).Messages.set({})

    @commands.command(pass_context=True)  
    @commands.has_any_role("CEO", "COO", "Human Resources Director", "Human Resources Representative", "Team Leader", "Bot-Developer", "General Manager", "Manager", "Assistant Manager", "Dispatcher")
    async def savemsg(self, ctx):

        #convert to serilizable object
        cloned_list = []

        for entry in self.messages:

            users = []
            
            for user in entry[2]:
                users.append([user[0].id, user[1]])

            cloned_list.append([[entry[0].id, entry[0].channel.id, entry[0].guild.id], entry[1].timestamp(), users, entry[3]])

        

        print(cloned_list)
    

        await self.message_db.guild(ctx.message.guild).Messages.set(cloned_list)

    @commands.command(pass_context=True)
    @commands.has_any_role("CEO", "COO", "Human Resources Director", "Human Resources Representative", "Team Leader", "Bot-Developer", "General Manager", "Manager", "Assistant Manager", "Dispatcher")
    async def loadmsg(self, ctx):
        
        temp_list = await self.message_db.guild(ctx.message.guild).Messages()


        for entry in temp_list:


            users = []
            for user in entry[2]:
                users.append([self.bot.get_user(user[0]), user[1]])

            guild = discord.utils.get(self.bot.guilds, id=entry[0][2])
            channel = discord.utils.get(guild.channels, id=entry[0][1])
            entry[0] = await channel.fetch_message(entry[0][0])
            entry[1] = pytz.utc.localize(datetime.fromtimestamp(entry[1]))
            entry[2] = users

        self.messages = temp_list

        #self.messages = json.loads(await self.message_db.guild(ctx.message.guild).Messages())
        #print(json.loads(await self.message_db.guild(ctx.message.guild).Messages()))
    
    async def save_messages(self, guild):
        #convert to serilizable object
        cloned_list = []

        for entry in self.messages:

            users = []
            
            for user in entry[2]:
                users.append([user[0].id, user[1]])

            cloned_list.append([[entry[0].id, entry[0].channel.id, entry[0].guild.id], entry[1].timestamp(), users, entry[3], entry[4]])

        

        print(cloned_list)
    

        await self.message_db.guild(guild).Messages.set(cloned_list)

    async def load_messages(self, guild):


        temp_list = await self.message_db.guild(guild).Messages()

        if(len(temp_list) < 1):
            self.messages = []
            return

        for entry in temp_list:


            users = []
            for user in entry[2]:
                users.append([self.bot.get_user(user[0]), user[1]])

            guild = discord.utils.get(self.bot.guilds, id=entry[0][2])
            channel = discord.utils.get(guild.channels, id=entry[0][1])
            entry[0] = await channel.fetch_message(entry[0][0])
            entry[1] = pytz.utc.localize(datetime.fromtimestamp(entry[1]))
            entry[2] = users

        self.messages = temp_list

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_any_role("Bot-Developer")
    async def convert(self, ctx, *, time: str):
        Scheduler = await self.database.guild(ctx.guild).Scheduler()
        time_before = parser.parse(time)
        utc_dt = pytz.utc.localize(time_before)
        loc_tz = timezone(Scheduler[str(ctx.author.id)])
        
        time = await self.convert_time(ctx, utc_dt, loc_tz)

        await ctx.send("Converted time should be: {}".format(time.strftime("%H:%M:%S - %d/%b/%Y")))


    async def find_message_by_id(self, message_id):
        
        try:
            return (list(filter(lambda x: x[0].id == message_id, self.messages)))[0]
        except:
            return None
    

    async def add_message(self, ctx, time_arg, event, author):

        event_time = pytz.utc.localize(parser.parse(time_arg))


        embed = discord.Embed(colour=discord.Colour(0xff9700), timestamp=datetime.utcfromtimestamp(int(time.time())),title=event[0], description=event[1])
        embed.set_thumbnail(url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
        embed.set_author(name="Downtown Cab Co. Dispatcher", icon_url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
        embed.set_footer(text="Press ✅ to attend.  Press 🌐 to convert to your time zone. \nPosted by {}\n".format(author.nick))
        embed.add_field(name="Where?", value="```{}```".format(event[2]), inline=True)
        embed.add_field(name="When? (UTC)", value="```{}```".format(event_time.strftime("%H:%M:%S - %d/%b/%Y")), inline=True)
        embed.add_field(name="Attendees", value="None", inline=False)

        msg = await ctx.send(embed=embed)
        #msg = await ctx.send("Come to the epic event at {}\n{}".format(event_time.strftime("%H:%M:%S - %d/%b/%Y"), event))


        list_object = [msg, event_time, [], event, []]



        self.messages.append(list_object)

        msg_obj = await self.find_message_by_id(msg.id)
        # self.messages[index]["time"] = "hello"

        
       
        start_adding_reactions(msg, ["✅", "🌐"])
        
        print (self.messages)

    async def convert_time(self, ctx, org_time, loc_tz):
        time = org_time.astimezone(loc_tz)
        return time

    from concurrent.futures.thread import ThreadPoolExecutor


    executor = ThreadPoolExecutor(max_workers=1)


    @commands.command(pass_context=True, aliases=["rtz"])
    async def removetz(self, ctx):
        for guild in self.bot.guilds:
            Scheduler = await self.database.guild(guild).Scheduler()
            del Scheduler[str(ctx.author.id)]
            await self.database.guild(guild).Scheduler.set(Scheduler)

    @commands.command(pass_context=True, aliases=["tz"])
    async def timezone(self, ctx, *, city: str):
        #loop = asyncio.get_event_loop()
        #asyncio.get_event_loop().create_task(self.thread_settimezone(ctx, city))
        #await loop.run_in_executor(self.executor, await self.thread_settimezone(ctx,city))
        await self.thread_settimezone(ctx, city)


    async def thread_settimezone(self, ctx, city):
        await ctx.send("Please wait, setting timezone...")

        location = self.gn.geocode(city)
        lon = location[1][0]
        lat = location[1][1]

        tf = TimezoneFinder()


        print(lon, lat)

    

        loc_tz = timezone(tf.timezone_at(lng=lat, lat=lon))

        for guild in self.bot.guilds:
            Scheduler = await self.database.guild(guild).Scheduler()
            Scheduler[ctx.author.id] = loc_tz.zone
            await self.database.guild(guild).Scheduler.set(Scheduler)

        utc_dt = pytz.utc.localize(datetime.utcnow())
        time = utc_dt.astimezone(loc_tz)

        await ctx.send("Your timezone has been set to **{}**\nCurrent time should be: {}".format(loc_tz.zone, time.strftime("%H:%M:%S - %d/%b/%Y")))