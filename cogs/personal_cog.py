import discord
import views
from discord.ext import commands

from utility import build_tower_page, build_role_page
from globals import RIG_LIST, EMOJIS_TO_REACT, FUN_ROLES, RIGS_DESCRIPTION, MSG_SENT, LAST_RIG
from rated import DEFER, FOLLOWUP, INTERACTION
from views import ShowProfile, ShowEggs, ShowCommands
from database import get_user_stats, list_decoded_entries

class PersonalCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="show", description="Show profiles, eggs, or help")
    @discord.app_commands.choices(type=[
        discord.app_commands.Choice(name="Profile", value="profile"),
        discord.app_commands.Choice(name="Help", value="help"),
        discord.app_commands.Choice(name="Eggs", value="eggs"),
    ])
    @discord.app_commands.describe(
        type="What do you want to see?",
        target="Optional: The user you want to look up (defaults to you)"
    )
    async def show(self, interaction: discord.Interaction, type: str, target: discord.Member = None):
        if interaction.guild is None or interaction.channel is None:
            await INTERACTION(interaction, "Use this command in the Crazy Stairs server!", True)
            return

        if target is None:
            target = interaction.user

        await DEFER(interaction)

        try:
            if type == "profile":
                await self._show_profile(interaction, target)
            elif type == "eggs":
                await self._show_eggs(interaction, target)
            elif type == "help":
                await self._show_help(interaction)
        except Exception as exc:
            await FOLLOWUP(f"Something went wrong with `/show {type}`: {exc}", interaction)
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
        self._prepare_role_pages(view, target)
        build_role_page(view, target, 4)

        # Page 7: Misc Stats
        messages = MSG_SENT.get(target.id, "0")
        lastrig = LAST_RIG.get(target.id, "None")
        view.data[6] = f"**Latest messages sent:** {messages}\n**Last rig cast:** {str(lastrig).capitalize()}"
        
        rig_key = str(lastrig).lower().replace(" rig", "")
        view.footers[6] = RIGS_DESCRIPTION.get(rig_key, "No rig data found.")

        await FOLLOWUP("", interaction, False, view)

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
        await FOLLOWUP("", interaction, False, view)

    async def _show_help(self, interaction):
        view = ShowCommands(timeout=500)
        view.requester = interaction.user
        view.channel = interaction.channel
        await FOLLOWUP("", interaction, False, view)
