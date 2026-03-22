import discord
from discord.ext import commands

from utility import build_tower_page, build_role_page, send_followup
from globals import HYPNO_SWAPS, RIG_LIST, EMOJIS_TO_REACT, FUN_ROLES, RIGS_DESCRIPTION, MSG_SENT, LAST_RIG, RIG_COOLDOWNS, COOLDOWN_DESCRIPTIONS, EXTRA_ROLES
from rated import DEFER, FOLLOWUP, INTERACTION
from views import ShowProfile, ShowEggs, ShowCommands
from database import get_user_stats, list_decoded_entries

class PersonalCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="show", description="Show profiles, eggs, or commands")
    @discord.app_commands.choices(type=[
        discord.app_commands.Choice(name="Profile", value="profile"),
        discord.app_commands.Choice(name="Eggs", value="eggs"),
        discord.app_commands.Choice(name="Cooldowns", value="cd"),
    ])
    @discord.app_commands.describe(
        type="What do you want to see?",
        target="Optional: The user you want to look up (defaults to you)"
    )
    async def show(self, interaction: discord.Interaction, type: str, target: discord.Member = None):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return
        
        newType = type

        if target is None:
            target = interaction.user

        if EXTRA_ROLES['hypno'] in interaction.user.roles:
            newType = HYPNO_SWAPS.get(type, type)

        await DEFER(interaction)

        try:
            if newType == "profile":
                await self._show_profile(interaction, target)
            elif newType == "eggs":
                await self._show_eggs(interaction, target)
            elif newType == "cd":
                await self._show_cd(interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/show {newType}`: {exc}", interaction)
            raise

    @discord.app_commands.command(name="help", description="Get Help")
    async def help(self, interaction: discord.Interaction):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        await DEFER(interaction)

        try:
            view = ShowCommands(timeout=500)
            view.requester = interaction.user
            view.channel = interaction.channel
            view.message = await FOLLOWUP(None, interaction, False, view)
            await view.update_message()
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/help`: {exc}", interaction)
            raise

    async def _show_profile(self, interaction, target):
        view = ShowProfile(timeout=500)
        view.target = target
        view.requester = interaction.user
        view.counter = {"Secret": 0, "Locked": 0, "AllSecret": 0, "AllLocked": 0}

        # Fetch stats
        user_stats = {k.decode("utf-8"): v.decode("utf-8") for k, v in get_user_stats(target).items()}

        # Page 1: Climbs
        user_climbs = ""
        total_climbs = 0
        for alignment in RIG_LIST:
            if alignment in ["none", "janitor"]: continue
            ali_climbs = user_stats.get(f"{alignment.upper()}_climbs", "0")
            user_climbs += f'{EMOJIS_TO_REACT[f"cs{alignment.capitalize()}"]}: {ali_climbs}\n\n'
            if ali_climbs.isdigit(): total_climbs += int(ali_climbs)

        view.data[0] = user_climbs
        view.footers[0] = f"{total_climbs} climbs in total!" if total_climbs > 0 else "Type 'bd link' to start tracking!"

        # Pages 2-4: Towers
        build_tower_page(user_stats, "classic", 1, view)
        build_tower_page(user_stats, "pro", 2, view)
        build_tower_page(user_stats, "infinite", 3, view)

        # Page 5 & 6: Roles
        build_role_page(view, target, 4)

        # Page 7: Misc Stats
        messages = MSG_SENT.get(target.id, "0")
        lastrig = LAST_RIG.get(target.id, "None")
        view.data[6] = f"**Latest messages sent:** {messages}\n**Last rig cast:** {str(lastrig).capitalize()}"
        
        rig_key = str(lastrig).lower().replace(" rig", "")
        view.footers[6] = RIGS_DESCRIPTION.get(rig_key, "No rig data found.")

        view.message = await FOLLOWUP(None, interaction, False, view)
        await view.update_message()

    async def _show_eggs(self, interaction, target):
        view = ShowEggs()
        view.target = target
        view.requester = interaction.user

        egg_roles = "## Egg Hunt 2025\n\n"
        # Prepare list to show in PAGE 1 (2025 egg hunt)
        for role in FUN_ROLES["Easter"]:
            view.counter["AllEggs"] += 1
            if str(target.id) in list_decoded_entries(role):
                view.counter["Eggs"] += 1
                egg_roles += "**" + str(role) + "** 🧺\n"
            else:
                egg_roles += "**???** 🧺\n"

        view.data[0] = egg_roles
        view.footers[0] = f"{target.name} found all the {view.counter['Eggs']} eggs, wow!" if view.counter["Eggs"] == view.counter["AllEggs"] else f"{view.counter['Eggs']} out of {view.counter['AllEggs']} eggs."

        egg_roles = "## Egg Hunt 2026\n\n"
        # Prepare list to show in PAGE 2 (2026 egg hunt)
        for role in FUN_ROLES["Easter26"]:
            view.counter["AllEggs"] += 1
            if str(target.id) in list_decoded_entries(role):
                view.counter["Eggs"] += 1
                egg_roles += "**" + str(role) + "** 🧺\n"
            else:
                egg_roles += "**???** 🧺\n"

        view.data[1] = egg_roles
        view.footers[1] = f"{target.name} found all the {view.counter['Eggs']} eggs, wow!" if view.counter["Eggs"] == view.counter["AllEggs"] else f"{view.counter['Eggs']} out of {view.counter['AllEggs']} eggs."

        # Send view... hopefully
        view.message = await FOLLOWUP(None, interaction, False, view)
        await view.update_message()

    async def _show_cd(self, interaction):
        cd = False
        for i, v in RIG_COOLDOWNS.items():
            if v and i != 'janitor':
                cd = True
                break

        cdList = ""
        for i, v in RIG_COOLDOWNS.items():
            cdList += COOLDOWN_DESCRIPTIONS[i]
            if v:
                cdList += ":x: \n"
            else:
                cdList += ":white_check_mark: \n"


        header = "One or more rigs are still in cooldown. \n" if cd else "Janitor is taking a rest. \n"
        final_msg = f"{header}{cdList}"

        await send_followup(interaction.channel, final_msg, interaction)