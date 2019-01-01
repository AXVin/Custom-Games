import discord
import os
import asyncio
from discord.ext import commands
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
        server_emojis = [k for k in servers]
        server_emoji_objects = []
        for emoji in server_emojis:
            server_emoji_objects.append(self.bot.get_emoji(emoji))
        self.server_emoji_objects = server_emoji_objects



    @commands.command(name="customgame")
    async def _customgame(self, ctx):
        """
        Make an awesome custom games message!
        """
        
        author = ctx.author
        server = ctx.guild
        
        await ctx.message.delete()

        try:
            cg_channel = discord.utils.get(server.channels, name="custom-rooms")
        except:
            await ctx.send('There was trouble finding the custom-rooms channel. Try again')
            return
        else:
            if cg_channel == None:
                await ctx.send('There is no channel named `#custom-rooms` in this server!')
                return
            else:
                pass
        member = author

        intro = await member.send("Hello <@{0.id}>!\nThis is the custom game portal for **{0.guild.name}** server!\nReact with ✅ to begin or ❌ to cancel!".format(author))
        for emoji in yes_no:
            await intro.add_reaction(emoji)
            await asyncio.sleep(0.5)
        
        react1, user1 = await self.wait_for_reaction(member, intro, ["✅", "❌"], 35)
        if react1.emoji == "❌":
            await member.send("Okay! I cancelled it")
            return
        elif react1 == None:
            await member.send("You took too long to respond! Cancelling the procedure.")
            return
        else:
            pass
        id_message = await member.send("What is the ID of the custom room?")
        room_id = await self.wait_for_message(member, 35)
        try:
            int(room_id.content)
        except:
            await member.send("That doesn't look like a room ID! Try the command again!")
            return
        await id_message.delete()
            
        pass_message = await member.send("What is the password of the custom room?")
        room_pass = await self.bot.wait_for_message(member, 35)
        await pass_message.delete()
        
        name_message = await member.send("What is the name of the custom room?")
        room_name = await self.bot.wait_for_message(member, 35)
        await name_message.delete()
           

# Room Server - Asia, NA etc.
        server_message = await member.send("What server is this Custom Game in?\n"
                                                             "*(Click on the appropriate reaction)*")
        
        for emoji in self.server_emoji_objects:
            await server_message.add_reaction(emoji)
            await asyncio.sleep(0.5)
        
        room_server, user2 = await self.wait_for_reaction(member, server_message, self.server_emoji_objects, 35)
  #      room_server = await self.bot.wait_for_reaction(timeout=35, emoji=self.server_emoji_objects, message=server_message, check=check)
        await server_message.delete()


# Type Arcade/Casual
        arcade_casual_message = await self.bot.send_message(member, "Is the server arcade or casual?\n\n🎮 Arcade\n🎯 Casual")
        arcade_casual_emojis = [k for k in ac_types]
        for emoji in arcade_casual_emojis:
            await arcade_casual_message.add_reaction(emoji)
            await asyncio.sleep(0.5)
        arcade_casual, user3 = await self.wait_for_reaction(member, arcade_casual_message, arcade_casual_emojis, 35)
       # arcade_casual = await self.bot.wait_for_reaction(timeout=35, emoji=arcade_casual_emojis, message=arcade_casual_message, check=check)
        await arcade_casual_message.delete()
            
                # SubType of Arcade
        if arcade_casual.emoji == "🎮":
            arcade_message = await self.bot.send_message(member, "What arcade type is used in the custom room?\n\n💥 War Mode\n💣 Quick Match\n🌀 Sniper Training\n🚧 Mini-Zone\n🚨 Hardcore Mode")
            arcade_emojis = [k for k in arcades]
            for emoji in arcade_emojis:
                await arcade_message.add_reaction(emoji)
                await asyncio.sleep(0.5)
            arcade, user4 = await self.wait_for_reaction(member, arcade_message, arcade_emojis, 35)
          #  arcade = await self.bot.wait_for_reaction(timeout=35, emoji=arcade_emojis, message=arcade_message, check=check)
            await arcade_message.delete()
        else:
        
            map_message = await self.bot.send_message(member, "What Map is being used in the custom room?\n\n🌲 Erangel\n🌵 Miramar\n🌴 Sanhok\n❄ Vikendi")
            map_emojis = [k for k in maps]
            for emoji in map_emojis:
                await map_message.add_reaction(emoji)
                await asyncio.sleep(0.5)
            map_choice, user5 = await self.wait_for_reaction(member, map_message, map_emojis, 35)
           # map_choice = await self.bot.wait_for_reaction(timeout=35, emoji=map_emojis, message=map_message, check=check)
            await map_message.delete()
            
            ftpp_message = await self.bot.send_message(member, "What perspective is being used in the custom room?\n\n1⃣ FPP\n3⃣ TPP")
            ftpp_emojis = [k for k in ftpp]
            for emoji in ftpp_emojis:
                await ftpp_message.add_reaction(emoji)
                await asyncio.sleep(0.5)
            ftpp_choice, user6 = await self.wait_for_reaction(member, ftpp_message, ftpp_emojis, 35)
         #   ftpp_choice = await self.bot.wait_for_reaction(timeout=35, emoji=ftpp_emojis, message=ftpp_message, check=check)
            await ftpp_message.delete()

        colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        embed = discord.Embed(title='Custom Games', colour=discord.Colour(value=colour))
        avatar = member.avatar_url if member.avatar else member.default_avatar_url
        
        embed.set_author(name='By {0}'.format(member), icon_url=avatar)
        embed.add_field(name='Room Name', value=room_name.content)
        embed.add_field(name='Room ID', value=room_id.content, inline=True)
        embed.add_field(name='Room Password', value=room_pass.content, inline=True)
        embed.add_field(name='Room Server', value=str(room_server.emoji) + ' ' + servers[room_server.emoji.id])
        embed.add_field(name='Room Type', value=ac_types[arcade_casual.emoji])
        if arcade_casual.emoji == "🎮":
            embed.add_field(name='Arcade Type', value=arcades[arcade.emoji])
        else:
            embed.add_field(name='Map', value=maps[map_choice.emoji])
            embed.add_field(name='Perspective', value=ftpp[ftpp_choice.emoji])

        trial_message = await self.bot.send_message(member, content=msg, embed=embed)
        trial_confirm_message = await self.bot.send_message(member, 'Do you want to send the above message to <#{0}>?'.format(cg_channel.id))
        for emoji in yes_no:
            await trial_confirm_message.add_reaction(emoji)
            await asyncio.sleep(0.5)
        trial_confirm, user6 = await self.wait_for_reaction(member, trial_confirm_message, yes_no, 35)
       # trial_confirm = await self.bot.wait_for_reaction(timeout=35, emoji=yes_no, message=trial_confirm_message, check=check)

        if trial_confirm.emoji == yes_no[0]:
            final_message = await self.bot.send_message(cg_channel, content=msg, embed=embed)

            await self.bot.send_message(member, '**Done!**')
            await final_message.delete()
        else:
            await self.bot.send_message(member, "Okay! The message wasn't sent. GoodBye!")
            return

# await self.wait_for_reaction(member, message, 35, emojis)

    async def wait_for_reaction(self, author:discord.Member, message:discord.Message, emoji, timeout=None):
        """
        Yup! I can't live without my old wait_for_reactions.
        This one require you to specify timeout as a float
        emojis must be a list of emoji objects
        """
        def check(reaction, user):
            return not user.bot and reaction.emoji in emoji and user == author and reaction.message == message
        if timeout:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=35, check=check)
            except Exception as e:
                await author.send('Timed out!')
                print(e)
                return
            else:
                return reaction, user
        else:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            return reaction, user


    async def wait_for_message(self, author:discord.Member, timeout=None):
        def check(message):
            return not user.bot and message.author==author
        if timeout:
            return await self.bot.wait_for('message', timeout=timeout, check=check)
        else:
            return await self.bot.wait_for('message', check=check)



def setup(bot):
    n = CGames(bot)
    bot.add_cog(n)