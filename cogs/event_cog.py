import asyncio
import random
import discord
from discord import app_commands
from discord.ext import commands

from globals import EDIBLE_EGGS, EGG_EATER, EVENTS, EXTRA_ROLES, MAX_EGGS, MEGA_SECRET_LAUNCHER, MORPHABLE_ROLES, BUTTONS, RIG_LIST, SPECIAL_ROLES
from rated import ADD_ROLES, DEFER, FOLLOWUP, INTERACTION, REMOVE_ROLES, SEND
from database import check_full_egg_conditions, check_perfect_egg_conditions, delete_entry_by_value, list_decoded_entries
from utility import launch_egg

class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="launch", description="Launch an egg with your trusty Egg Launcher!")
    @discord.app_commands.choices(type=[
        discord.app_commands.Choice(name="Max", value="max"),
        discord.app_commands.Choice(name="Full", value="full"),
        discord.app_commands.Choice(name="Perfect", value="perfect"),
        discord.app_commands.Choice(name="Mega Secret", value="mega"),
        discord.app_commands.Choice(name="Admin (Admins Only)", value="admin"),
        discord.app_commands.Choice(name="Murdurator (Murdurators Only)", value="murdurator"),
        discord.app_commands.Choice(name="Master (Drone Masters Only)", value="master"),
    ])
    async def launch(self, interaction: discord.Interaction, type: str = None):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        usr = interaction.user
        ch = interaction.channel

        await DEFER(interaction)

        try:
            if not EVENTS["Easter"] and ch.id != 813882658156838923:
                await FOLLOWUP(f"{usr.mention} threw the Sleazy Egg! ...But it fell on the ground and broke.", interaction)
                return

            from views import ButtonEgg_Throw
            view = ButtonEgg_Throw(timeout=30)
            view.thrower = usr.id
            view.disabled = False
            view.type = None

            if SPECIAL_ROLES["Admin"][0] in usr.roles and type == "admin":
                BUTTONS["easterStaffStatus"] = True
                view.type = "Admin"
            elif EXTRA_ROLES["murdurator"] in usr.roles and type == "murdurator":
                BUTTONS["easterStaffStatus"] = True
                view.type = "Murdurator"
            elif EXTRA_ROLES["admin"] in usr.roles and type == "master":
                BUTTONS["easterStaffStatus"] = True
                view.type = "Broken Drone"
            else:
                if BUTTONS["easterStatus"]:
                    await FOLLOWUP("The Egg Launcher is charging. This stuff takes time.", interaction)
                    return
                
                BUTTONS["easterStatus"] = True

                for role in reversed(usr.roles):
                    if role.name.lower() in RIG_LIST:
                        view.type = role.name
                        break

                if type:
                    if type.title() == "Max" and str(view.thrower) in list_decoded_entries(f"{view.type.title()} Egg"):
                        view.type = MAX_EGGS[view.type.title()]
                    elif type.title() == "Max":
                        await FOLLOWUP("To launch that egg, you must first have the base one.", interaction)
                        BUTTONS["easterStatus"] = False
                        return

                    if (type.title() == "Full" and check_full_egg_conditions(usr)):
                        view.type = type.title()
                    elif type.title() == "Full":
                        await FOLLOWUP("Aren't you full of yourself? Or perhaps not full enough.", interaction)
                        BUTTONS["easterStatus"] = False
                        return

                    if (type.title() == "Perfect" and check_perfect_egg_conditions(usr)):
                        view.type = type.title()
                    elif type.title() == "Perfect":
                        await FOLLOWUP(f"Nobody's perfect, but you aren't even close.", interaction)
                        BUTTONS["easterStatus"] = False
                        return
                    
                    if (type.title() == "Mega" and (MEGA_SECRET_LAUNCHER["user"] == usr.id or MEGA_SECRET_LAUNCHER["user"] == None)):
                        view.type = "Mega Secret"
                    elif type.title() == "Mega":
                        await FOLLOWUP("The Mega Secret Egg Launcher can only be used once, and by the person who found it. Maybe that person is you... someday.", interaction)
                        BUTTONS["easterStatus"] = False
                        return
                    
            if random.randint(1, 11) == 1:
                view.type = "Super Secret"

            if view.type == None:
                await FOLLOWUP("The Egg Launcher is confused... It doesn't know which Egg to launch!", interaction)
                BUTTONS["easterStatus"] = False
                return
            
            if view.type == BUTTONS["easterLast"]:
                await FOLLOWUP("The Egg Launcher refuses to launch the same egg twice in a row! It seems to be craving some variety.", interaction)
                BUTTONS["easterStatus"] = False
                return
                    
            BUTTONS["easterLast"] = view.type
            view.picker = None
            view.channel = ch
            view.toolate = True
            viewMsg = ""

            if view.type == "Super Secret":
                viewMsg = f"{usr.mention}'s Egg Launcher malfunctioned and threw a strange looking egg!"
            else:
                viewMsg = f"{usr.mention} threw the {view.type} Egg!"

            view.message = await FOLLOWUP(viewMsg, interaction, False, view)
            await view.wait()
            await view.too_late()

            if BUTTONS["easterStatus"] and not BUTTONS["easterStaffStatus"]:
                await asyncio.sleep(BUTTONS["easterTimer"])
                await SEND(ch, "The egg launcher is ready!")
                BUTTONS["easterStatus"] = False

            if BUTTONS["easterStaffStatus"]:
                BUTTONS["easterStaffStatus"] = False
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/launch`: {exc}", interaction)
            BUTTONS["easterStatus"] = False
            BUTTONS["easterStaffStatus"] = False
            raise

    @discord.app_commands.command(name="eat", description="Eat a base Alignment egg you own.")
    @discord.app_commands.choices(type=[discord.app_commands.Choice(name=k.title(), value=k.lower()) for k in MAX_EGGS.values()])
    async def eat(self, interaction: discord.Interaction, type: str):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        usr = interaction.user
        ch = interaction.channel

        if not EVENTS["Easter"] and ch.id != 813882658156838923:
            await INTERACTION(interaction, "I ate all the eggs, sorry not sorry.", True)
            return

        await DEFER(interaction)

        try:
            errorMsg = None
            if type.lower() not in EDIBLE_EGGS:
                errorMsg = "You cannot eat this."
            elif not str(usr.id) in list_decoded_entries(f"{type.title()} Egg"):
                errorMsg = "You ate some air. Delicious!"
            elif MORPHABLE_ROLES[type.title()][0] in usr.roles:
                errorMsg = "The egg said no."
            elif usr.id in EGG_EATER:
                errorMsg = "Too many eggs are bad for your health."

            if errorMsg:
                await FOLLOWUP(errorMsg, interaction)
                return
            
            if random.randint(1, 3) == 1:
                await launch_egg(ch, "Secret", "Before you get the chance to eat the egg, it cracks and reveals... Another egg?", interaction)
            else:
                EGG_EATER.append(usr.id)

                delete_entry_by_value(f"{type.title()} Egg", str(usr.id))

                role_list = []
                for role in usr.roles:
                    if (role.name in MORPHABLE_ROLES):
                        role_list.append(role)
                await REMOVE_ROLES(usr, role_list)
                await asyncio.sleep(1)

                await ADD_ROLES(usr,MORPHABLE_ROLES[type.title()][0])

                await FOLLOWUP(f"{usr.mention} ate the {type.title()} Egg! They feel different now.", interaction)
                await asyncio.sleep(3600)
                EGG_EATER.remove(usr.id)    
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/eat`: {exc}", interaction)
            raise