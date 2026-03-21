import asyncio
import secrets
import string

from database import delete_entry, list_decoded_entries, redis_add_user_data, redis_check_token, redis_remove_token
import discord
from discord import app_commands
from discord.ext import commands

from globals import CHANNELS, FIX_BOT, EXTRA_ROLES, ACTIVE_RIGS, DETAILED_RIGS, MORPHABLE_ROLES, PRAISES, RIG_COOLDOWNS, BUTTONS, TIPS_KEYS, getScoldDictionary, getPraiseDictionary
from main import PRINT_ENTRIES
from rated import DEFER, FOLLOWUP, INTERACTION, SEND, SEND_DM
from quiz import FORCE_CLOSE_EVENT
from ladders import MG_RESET
from views import ButtonGames_ThrowingStuff
from database import add_entry_with_check, add_entry

class MiscCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="reset", description="Reset Broken Drone")
    async def reset(self, interaction: discord.Interaction):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        usr = interaction.user
        ch = interaction.channel

        if usr in FIX_BOT:
            await INTERACTION(interaction, "Not again.", True)
            return
        
        await DEFER(interaction)

        try:
            FIX_BOT.append(usr)
            if len(FIX_BOT) == 1 and not EXTRA_ROLES['admin'] in usr.roles:
                await FOLLOWUP("One User wants me to reset. 2 more people are required for it to take effect.", interaction, False)
                # await SEND(ch, "One User wants me to reset. 2 more people are required for it to take effect.")
            elif len(FIX_BOT) == 2 and not EXTRA_ROLES['admin'] in usr.roles:
                # await SEND(ch, "Two Users want me to reset. 1 more person is required for it to take effect.")
                await FOLLOWUP("Two Users want me to reset. 1 more person is required for it to take effect.", interaction, False)
            else:
                # await SEND(ch, "All Games and Rigs (along with their Cooldowns) have been reset.")
                await FOLLOWUP("All Games and Rigs (along with their Cooldowns) have been reset.", interaction, False)
                FIX_BOT.clear()
                FORCE_CLOSE_EVENT()
                MG_RESET()

                for rig in ACTIVE_RIGS:
                    ACTIVE_RIGS[rig] = False 

                for rig in DETAILED_RIGS:
                    DETAILED_RIGS[rig][0] = None
                    DETAILED_RIGS[rig][1] = None

                for cooldown in RIG_COOLDOWNS:
                    RIG_COOLDOWNS[cooldown] = False

                BUTTONS["status"] = False
                BUTTONS["easterStatus"] = False
                BUTTONS["easterStaffStatus"] = False

            await asyncio.sleep(60)

            if len(FIX_BOT) != 0:
                await SEND(ch, "Games have not been reset due to lack of users asking to.")
                FIX_BOT.clear()
            return
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/reset`: {exc}", interaction)
            raise
    
    @discord.app_commands.command(name="poll", description="Create a poll with buttons")
    async def poll(self, interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None, option6: str = None, option7: str = None, option8: str = None, option9: str = None, option10: str = None, option11: str = None, option12: str = None, option13: str = None, option14: str = None, option15: str = None, option16: str = None, option17: str = None, option18: str = None, option19: str = None, option20: str = None):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        usr = interaction.user
        ch = interaction.channel
        all_options = [
            option1, option2, option3, option4, option5, option6, 
            option7, option8, option9, option10, option11, option12, 
            option13, option14, option15, option16, option17, option18, 
            option19, option20
        ]
        active_options = [opt for opt in all_options if opt is not None]

        if BUTTONS["status"]:
            await INTERACTION(interaction, "A poll is already active.", True)
            return

        await DEFER(interaction)

        try:
            BUTTONS["status"] = True
            pollA = active_options
            pollQ = question

            if len(pollA) < 2:
                await FOLLOWUP('You need to provide at least 2 options to create a poll.', interaction, True)
                BUTTONS["status"] = False
                return

            for badword in self.bot.blacklist:
                for answer in pollA:
                    if (badword in answer.lower()) or (badword in pollQ.lower()):
                        await FOLLOWUP("Your poll contains inappropriate content.", interaction, True)
                        # await SEND(ch, "Your poll contains inappropriate content.")
                        BUTTONS["status"] = False
                        return

            view = ButtonGames_ThrowingStuff(timeout=600)
            view.choices = pollA
            view.customUser = usr

            for i in range(len(active_options)):
                view.votes[str(i)] = []
                
                btn = discord.ui.Button(
                    label=active_options[i], 
                    custom_id=f"throw{i}", 
                    style=discord.ButtonStyle.primary
                )

                async def callback_wrapper(interaction, button_index=str(i)):
                    await view.process_click(interaction, button_index, usr)
                btn.callback = callback_wrapper

                view.add_item(btn)

            close_btn = discord.ui.Button(label="Close Poll", style=discord.ButtonStyle.red)
            async def close_callback(interaction):
                await view.process_click(interaction, "throwclose", usr)
            close_btn.callback = close_callback

            view.add_item(close_btn)
            BUTTONS["view"] = view
            BUTTONS["channel"] = ch

            # view.message = await SEND_VIEW(BUTTONS["channel"], pollQ, view)
            view.message = await FOLLOWUP(pollQ, interaction, False, view=view)

            await view.wait()
            BUTTONS["status"] = False
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/poll`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="scold", description="Scold someone")
    async def scold(self, interaction: discord.Interaction, target: discord.Member):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        usr = interaction.user
        finalmsg = None

        try:
            ScoldDict = getScoldDictionary(target, usr)

            # Scold someone in the Dictionary (User itself included)
            if target.id in ScoldDict:
                finalmsg = ScoldDict[target.id]
            # Scolding a Bot
            elif target.bot:
                finalmsg = "I love my bot friends."
            # Scolding an User that is in the Server
            else:
                finalmsg = target.display_name + ", I am very disappointed in you."

            await INTERACTION(interaction, finalmsg)
            return
        except Exception as exc:
            await INTERACTION(interaction, f"Something went wrong with `/scold`: {exc}")
            raise

    @discord.app_commands.command(name="praise", description="Praise someone")
    async def praise(self, interaction: discord.Interaction, target: discord.Member):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        usr = interaction.user
        finalmsg = None

        try:
            praised_user_id = target.id
            praising_user_id = usr.id

            if praised_user_id not in PRAISES:
                PRAISES[praised_user_id] = []

            # Add the praising user's ID to the praised user's list if not already added
            if praising_user_id not in PRAISES[praised_user_id] and praising_user_id != praised_user_id:
                PRAISES[praised_user_id].append(praising_user_id)

            PraiseDict = getPraiseDictionary(target, usr)
            # Praise someone in the Dictionary (User itself included)
            if praised_user_id in PraiseDict:
                finalmsg = PraiseDict[praised_user_id]
            # Praising a Bot
            elif target.bot:
                finalmsg = "Well done, bot friend.\n-# Between us, I am the best."
            # Praising an User that is in the Server
            else:
                # Check if the praised user has been praised by three unique users
                if len(PRAISES[praised_user_id]) == 3:
                    finalmsg = f"{target.display_name}, everyone likes you. And so do I."

                    if not str(praised_user_id) in list_decoded_entries("Acclaimed"):
                        await add_entry_with_check("Acclaimed", target)
                else:
                    finalmsg = f"Well done, {target.display_name}. Most excellent."
                    
            await INTERACTION(interaction, finalmsg)
            return
        except Exception as exc:
            await INTERACTION(interaction, f"Something went wrong with `/praise`: {exc}")
            raise

    @discord.app_commands.command(name="link", description="Link account for Janitor role")
    async def link(self, interaction: discord.Interaction):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        usr = interaction.user
        ch = interaction.channel

        await DEFER(interaction)

        if redis_check_token(usr) != None: 
            await FOLLOWUP("Please unlink first. If you no longer have access to your account, contact mods.", interaction, True)
            return
        
        try:
            alphabet = string.ascii_letters + string.digits
            token = ''.join(secrets.choice(alphabet) for i in range(20))
        
            redis_add_user_data("USER_" + str(usr.id), "token", token)

            await SEND_DM(usr, 
                "Please copy this code. To link your Roblox account properly, you'll need to submit it as a feedback message within the Roblox game itself.\n\n"
                f"`LINK DISCORD {str(usr.id)} {token}`\n"
                "'LINK DISCORD' included!\n\n"
                "**DO NOT SHARE IT WITH ANYONE, WE WILL NEVER ASK YOU FOR THAT INFORMATION.**\n\n"
                "If successful, you will be pinged in <#1001034407966150746>.\n" + 
                "By doing this you agree for your Crazy Stairs Roblox data to be stored on external server and for Crazy Stairs to keep your discord user id.\n"
                "Your climbs, wins and personal records will be accessible via a 'bd show profile' command. Be aware that anyone in the server can view your profile at any time." + 
                "You can unlink and delete your data from external servers at any time by sending this command into Roblox postbox:\n\n" +
                "`UNLINK DISCORD`\n\n" +
                "If you no longer have access to your Roblox account and want us to remove your data, contact sleazel directly.")
            
            await asyncio.sleep(1)
            await SEND_DM(usr, "https://giphy.com/gifs/TskpnwGI2P1GCmtUJ0")
            await asyncio.sleep(1)
            await FOLLOWUP("I have sent you a direct message with further instructions.", interaction, False)
        except:
            redis_remove_token(usr)
            await SEND(ch, "You need to accept DMs from me, as I need to send you a verification code.")

    @discord.app_commands.command(name="tip_add", description="Add a tip to the database")
    @discord.app_commands.choices(type=[
        discord.app_commands.Choice(name="Tip", value="tip"),
        discord.app_commands.Choice(name="Trivia", value="trivia"),
    ])
    @discord.app_commands.choices(alignment=[discord.app_commands.Choice(name=k.title(), value=k) for k in TIPS_KEYS])
    async def tip_add(self, interaction: discord.Interaction, type: str, alignment: str, content: str):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        usr = interaction.user
        key = alignment

        await DEFER(interaction)

        try:
            if not MORPHABLE_ROLES["Janitor"][0] in usr.roles:
                await FOLLOWUP("Only Janitors can add new Tips and Trivia.", interaction, True)
                return
        
            #for trivia, key has extra "T" at the end
            if type == "trivia":
                key = alignment + "T"
                
            #add tip   
            add_entry(key, content)
            await FOLLOWUP(f"New " + type.title() + " for " + alignment.title() + " added.", interaction, False)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/tip_add`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="tip_list", description="List all tips and trivia")
    @discord.app_commands.choices(type=[
        discord.app_commands.Choice(name="Tip", value="tip"),
        discord.app_commands.Choice(name="Trivia", value="trivia"),
    ])
    @discord.app_commands.choices(alignment=[discord.app_commands.Choice(name=k.title(), value=k) for k in TIPS_KEYS])
    async def tip_list(self, interaction: discord.Interaction, alignment: str, type: str):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        usr = interaction.user
        ch = interaction.channel
        key = alignment

        await DEFER(interaction)

        try:
            if not MORPHABLE_ROLES["Janitor"][0] in usr.roles:
                await FOLLOWUP("Only Janitors can add new Tips and Trivia.", interaction, True)
                return
            
            #for trivia, key has extra "T" at the end
            if type == "trivia":
                key = alignment + "T"
               
            await FOLLOWUP(f"Listing all " + type.title() + " for " + alignment.title() + ":", interaction, False)
            await asyncio.sleep(1)
            await PRINT_ENTRIES(ch, key)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/tip_list`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="tip_delete", description="Delete a tip or trivia")
    @discord.app_commands.choices(type=[
        discord.app_commands.Choice(name="Tip", value="tip"),
        discord.app_commands.Choice(name="Trivia", value="trivia"),
    ])
    @discord.app_commands.choices(alignment=[discord.app_commands.Choice(name=k.title(), value=k) for k in TIPS_KEYS])
    async def tip_delete(self, interaction: discord.Interaction, alignment: str, type: str, position: int):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        usr = interaction.user
        ch = interaction.channel
        key = alignment

        await DEFER(interaction)

        try:
            if not MORPHABLE_ROLES["Janitor"][0] in usr.roles:
                await FOLLOWUP("Only Janitors can add new Tips and Trivia.", interaction, True)
                return
          
            #for trivia, key has extra "T" at the end
            if type == "trivia":
                key = alignment + "T"
               
            #delete tip   
            delete_entry(key, int(position))
            await FOLLOWUP(f"Deleted " + type.title() + " number " + str(position) + " for " + alignment.title() + ".", interaction, False)
            await asyncio.sleep(1)
            await PRINT_ENTRIES(ch, key)
            return
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/tip_delete`: {exc}", interaction)
            raise