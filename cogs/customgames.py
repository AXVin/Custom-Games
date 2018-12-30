import discord
import os
import asyncio
from discord.ext import commands
#from __main__ import send_cmd_help
#from .utils.dataIO import dataIO
#from .utils import checks
from random import choice, randint




yes_no = ["✅","❌"]

ftpp = {"1⃣" : "First Person Perspective(FPP)",
        "3⃣" : "Third Person Perspective(TPP)"}

servers = {"524968326498222112":   "NA",
           "524968325990842378":   "EU",
           "524968326489702415":   "SA",
           "524968326523387934": "ASIA",
           "524968326292832257": "KRJP"}
 
ac_types = {"🎯": 'Casual',    # 🎯
            "🎮": 'Arcade'}    # 🎮

time = {'🕐': 60*5,         # 🕐 5m
        '🕑': 60*10,        # 🕑 10m
        '🕒': 60*15,        # 🕒 15m
        '🕓': 60*20,        # 🕓 20m
        '🕔': 60*25,        # 🕔 25m
        '🕕': 60*30}        # 🕕 30m

maps = {'🌲': 'Erangel',    # 🌲
        '🌵': 'Miramar',    # 🌵
        '🌴': 'Sanhok',     # 🌴
        '❄': 'Vikendi'}     # ❄

arcades = {'💥': 'War Mode',        # 💥
           '💣': 'Quick Match',     # 💣
           '🌀': 'Sniper Training', # 🌀
           '🚧': 'Mini-Zone',       # 🚧
           '🚨': 'Hardcore Mode'}   # 🚨
  
class CGames:
    """A cog for awesome custom games notifications!"""
    
    def __init__(self, bot):
        self.bot = bot
   #     self.file_path = "data/cgames/system.json"
   #     self.system = dataIO.load_json(self.file_path)
        self.emoji_server = await self.bot.get_server('431374578409799681')
        server_emojis = [k for k in servers]
        server_emoji_objects = []
        for x in self.emoji_server.emojis:
            if x.id in server_emojis:
                server_emoji_objects.append(x)
        self.server_emoji_objects = server_emoji_objects



    @commands.command(pass_context=True, no_pm=True)
    async def customgame(self, ctx):
        """
        Make an awesome custom games message!
        """
        
        author = ctx.message.author
        server = author.server
  #      settings = self.check_server_settings(author.server)
        
        await self.bot.delete_message(ctx.message)
        
        
  #      if not settings["CG Channel"]:
  #          await self.bot.say('This feature isn\'t set up yet')
  #          return
        
  #      cg_channel = self.bot.get_channel(settings["CG Channel"])
        try:
            cg_channel = discord.utils.get(server.channels, name="custom-rooms")
        except:
            await self.bot.say('There was trouble finding the custom-rooms channel. Try again')
            return
        else:
            if cg_channel == None:
                self.bot.say('There is no channel named `#custom-rooms` in this server!')
                return
            else:
                pass
        #member = await self.bot.get_member(author.id)
        member = author
        
        
        def check(reaction, user):
                return not user.bot

        intro = await self.bot.send_message(member, "Hello <@{0.id}>!\nThis is the custom game portal for **{0.server.name}** server!\nReact with ✅ to begin or ❌ to cancel!".format(author))
        for emoji in yes_no:
            await self.bot.add_reaction(intro, emoji)
            await asyncio.sleep(0.5)
        react1 = await self.bot.wait_for_reaction(timeout=35, emoji=["✅", "❌"], message=intro, check=check)
        if react1.reaction.emoji == "❌":
            await self.bot.send_message(member, "Okay! I cancelled it")
            return
        elif react1 == None:
            await self.bot.send_message(member, "You took too long to respond! Cancelling the procedure.")
            return
        else:
            pass
        id_message = await self.bot.send_message(member, "What is the ID of the custom room?")
        room_id = await self.bot.wait_for_message(timeout=35, author=member)
        try:
            int(room_id.content)
        except:
            await self.bot.send_message(member, "That doesn't look like a room ID! Try the command again!")
            return
        await self.bot.delete_message(id_message)
            
        pass_message = await self.bot.send_message(member, "What is the password of the custom room?")
        room_pass = await self.bot.wait_for_message(timeout=35, author=member)
        await self.bot.delete_message(pass_message)
        
        name_message = await self.bot.send_message(member, "What is the name of the custom room?")
        room_name = await self.bot.wait_for_message(timeout=35, author=member)
        await self.bot.delete_message(name_message)
           

# Room Server - Asia, NA etc.
        server_message = await self.bot.send_message(member, "What server is this Custom Game in?\n"
                                                             "*(Click on the appropriate reaction)*")
        
        for emoji in self.server_emoji_objects:
            await self.bot.add_reaction(server_message, emoji)
            await asyncio.sleep(0.5)
        room_server = await self.bot.wait_for_reaction(timeout=35, emoji=self.server_emoji_objects, message=server_message, check=check)
        await self.bot.delete_message(server_message)


# Type Arcade/Casual
        arcade_casual_message = await self.bot.send_message(member, "Is the server arcade or casual?\n\n🎮 Arcade\n🎯 Casual")
        arcade_casual_emojis = [k for k in ac_types]
        for emoji in arcade_casual_emojis:
            await self.bot.add_reaction(arcade_casual_message, emoji)
            await asyncio.sleep(0.5)
        arcade_casual = await self.bot.wait_for_reaction(timeout=35, emoji=arcade_casual_emojis, message=arcade_casual_message, check=check)
        await self.bot.delete_message(arcade_casual_message)
            
                # SubType of Arcade
        if arcade_casual.reaction.emoji == "🎮":
            arcade_message = await self.bot.send_message(member, "What arcade type is used in the custom room?\n\n💥 War Mode\n💣 Quick Match\n🌀 Sniper Training\n🚧 Mini-Zone\n🚨 Hardcore Mode")
            arcade_emojis = [k for k in arcades]
            for emoji in arcade_emojis:
                await self.bot.add_reaction(arcade_message, emoji)
                await asyncio.sleep(0.5)
            arcade = await self.bot.wait_for_reaction(timeout=35, emoji=arcade_emojis, message=arcade_message, check=check)
            await self.bot.delete_message(arcade_message)
        else:
            # Map
        
            map_message = await self.bot.send_message(member, "What Map is being used in the custom room?\n\n🌲 Erangel\n🌵 Miramar\n🌴 Sanhok\n❄ Vikendi")
            map_emojis = [k for k in maps]
            for emoji in map_emojis:
                await self.bot.add_reaction(map_message, emoji)
                await asyncio.sleep(0.5)
            map_choice = await self.bot.wait_for_reaction(timeout=35, emoji=map_emojis, message=map_message, check=check)
            await self.bot.delete_message(map_message)
            
            ftpp_message = await self.bot.send_message(member, "What perspective is being used in the custom room?\n\n1⃣ FPP\n3⃣ TPP")
            ftpp_emojis = [k for k in ftpp]
            for emoji in ftpp_emojis:
                await self.bot.add_reaction(ftpp_message, emoji)
                await asyncio.sleep(0.5)
            ftpp_choice = await self.bot.wait_for_reaction(timeout=35, emoji=ftpp_emojis, message=ftpp_message, check=check)
            await self.bot.delete_message(ftpp_message)
        
# Start Time - 5m 10m 15m 20m 25m 30m
    #    time_message = await self.bot.send_message(member, "In what time will the match begin from now?\nMust be just a number between 5 and 30 and should be in minutes\nFor eg- 15")
    #    time = await self.bot.wait_for_message(timeout=35, author=member)
        
   #     try:
    #        int(time.content)
    #        pass
  #      except:
    #        t11 = await self.bot.send_message(member, "Must be a number. You have one more chance to try.\nTip: Only type the number. It must be an integer")
   #         time = await self.bot.wait_for_message(timeout=35, author=member)
    #        try:
    #            int(time.content)
    #            await self.bot.delete_message(t11)
    #        except:
    #            await self.bot.send_message(member, "You are still doing it wrong. Contact a Mod to kno da wae!!")
   #             return
        
  #      if int(time.content) < 30 and int(time.content) > 0:
   #         pass
  #      else:
   #         t22 = await self.bot.send_message(member, "Must be a number between 5 and 30. You have one more chance to try.")
   #         time = await self.bot.wait_for_message(timeout=35, author=member)
   #         if not int(time.content) < 30 and int(time.content) > 0:
   #             await self.bot.send_message(member, "You are still doing it wrong. Contact a Mod to kno da wae!!")
   #             return
   #         else:
    #            await self.bot.delete_message(t22)
   #     await self.bot.delete_message(time_message)
# Start making the embed
        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        embed = discord.Embed(title='Custom Games', colour=discord.Colour(value=colour))
        avatar = member.avatar_url if member.avatar else member.default_avatar_url
        
        embed.set_author(name='By {0}'.format(member), icon_url=avatar)
        embed.add_field(name='Room Name', value=room_name.content)
        embed.add_field(name='Room ID', value=room_id.content, inline=True)
        embed.add_field(name='Room Password', value=room_pass.content, inline=True)
        embed.add_field(name='Room Server', value=str(room_server.reaction.emoji) + ' ' + servers[room_server.reaction.emoji.id])
        embed.add_field(name='Room Type', value=ac_types[arcade_casual.reaction.emoji])
        if arcade_casual.reaction.emoji == "🎮":
            embed.add_field(name='Arcade Type', value=arcades[arcade.reaction.emoji])
        else:
            embed.add_field(name='Map', value=maps[map_choice.reaction.emoji])
            embed.add_field(name='Perspective', value=ftpp[ftpp_choice.reaction.emoji])
  #      embed.add_field(name='Starts in-', value='{0} minutes'.format(time.content))
# For the ping, check server settings for mode
  #      Mode = settings["Mode"]
  #      if Mode == None:
  #          msg = 'Check out this new Custom Room!'
  #      elif Mode == 'everyone':
  #          msg = '@everyone Check out this new Custom Room!'
  #      elif Mode == 'here':
  #          msg = '@here Check out this new Custom Room guys!'
  #      elif Mode == 'custom games role':
  #          msg = '<&{0}> Check out this new Custom Room guys!'.format(settings["Role IDs"]["Custom Games"])
  #      elif Mode == 'servers':
  #          msg = '<&{0}> Check out this new Custom Room guys!'.format(settings["Role IDs"][servers[room_server.reaction.emoji]])
# Send a Preview and Ask if it is right!
        trial_message = await self.bot.send_message(member, content=msg, embed=embed)
        trial_confirm_message = await self.bot.send_message(member, 'Do you want to send the above message to <#{0}>?'.format(cg_channel.id))
        for emoji in yes_no:
            await self.bot.add_reaction(trial_confirm_message, emoji)
            await asyncio.sleep(0.5)
        trial_confirm = await self.bot.wait_for_reaction(timeout=35, emoji=yes_no, message=trial_confirm_message, check=check)
# Send Message
   #     if settings["Delete Wait Time"] != None:
   #         wait_time = (int(time.content)*60) + settings["Delete Wait Time"]
   #     else:
   #         wait_time = None
        if trial_confirm.reaction.emoji == yes_no[0]:
            final_message = await self.bot.send_message(cg_channel, content=msg, embed=embed)
   #         if wait_time == None:
            await self.bot.send_message(member, '**Done!**')
   #         else:
   #             if wait_time//60 != 0:
   #                 time_converted = str(int(wait_time/60)) + ' minutes' + ' and '+ str(wait_time//60) + ' seconds'
   #             else:
   #                 time_converted = str(wait_time/60) + 'minutes' if wait_time/60 > 1 else 'one minute'
   #             await self.bot.send_message(member, '**Done!**\nThe message will disappear after {0}'.format(time_converted))
   #             await asyncio.sleep(wait_time)
# Delete the message from custom game channel
   #             await self.bot.delete_message(final_message)
        else:
            await self.bot.send_message(member, "Okay! The message wasn't sent. GoodBye!")
            return





def setup(bot):
    n = CGames(bot)
    bot.add_cog(n)