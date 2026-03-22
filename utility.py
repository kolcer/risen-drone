import random
from globals import RIG_LIST, EMOJIS_TO_REACT, BUTTONS, FUN_ROLES, GIT_COMMITTERS
from rated import SEND, FOLLOWUP, SEND_VIEW
from database import list_decoded_entries, list_entries

# Convert milliseconds to seconds
def convert_best_times(num):
    try:
        return round(int(num) / 100, 2)
    except (ValueError, TypeError):
        return "N/A" 

# Create page for tower best times   
def build_tower_page(user_stats, tower_type, page_index, view):
    user_times = ""
    avg_time = 0
    valid_entries = 0

    for alignment in RIG_LIST:
        if alignment in ["none", "janitor"]:
            continue
        
        ali_time = convert_best_times(user_stats.get(f"{alignment.upper()}_{tower_type}", "N/A"))

        if ali_time != "N/A":
            avg_time += ali_time
            ali_time = f"{ali_time} seconds"
            valid_entries += 1

        emoji = EMOJIS_TO_REACT.get(f"cs{alignment.capitalize()}", "❓")
        user_times += f"{emoji}: {ali_time}\n\n"

    view.data[page_index] = user_times
    if valid_entries:
        view.footers[page_index] = f"Average climb time is {avg_time / valid_entries:.2f} seconds!"
    else:
        view.footers[page_index] = "Type 'bd link' to link your account and start tracking your times!"

async def launch_egg(ch, eggType, msg, interaction=None):
    from views import ButtonEgg_Throw
    BUTTONS["status"] = True
    view = ButtonEgg_Throw(timeout=30)
    view.thrower = None
    view.picker = None
    view.disabled = False

    view.type = eggType

    view.channel = ch
    view.toolate = True
    if interaction is not None:
        view.message = await FOLLOWUP(msg, interaction, False, view)
    else:
        view.message = await SEND_VIEW(ch, msg, view)
    await view.wait()
    await view.too_late()
    BUTTONS["status"] = False

async def send_followup(ch, msg, interaction=None, ephemeral=False, view=None, embed=None):
    if interaction is not None:
        try:
            # Try to use the interaction first
            return await FOLLOWUP(msg, interaction, ephemeral, view, embed)
        except Exception:
            # If the token is invalid/expired, fall back to a normal message
            return await SEND(ch, msg, view, embed)
    else:
        return await SEND(ch, msg, view, embed)
    
def build_role_page(view, target, index):
    # --- PAGE 5: SECRET ROLES (Available & Recurring) ---
    secret_roles = "## Available Roles\n\n"
    for role in FUN_ROLES["Available"]:
        view.counter["AllSecret"] += 1

        if str(target.id) in list_decoded_entries(role):
            view.counter["Secret"] += 1
            secret_roles += f"**{role}**\n"
        else:
            secret_roles += "**???**\n"

    secret_roles += "\n## Recurring Roles\n\n"
    for role, desc in FUN_ROLES["Recurring"].items():
        view.counter["AllSecret"] += 1
        if str(target.id) in list_decoded_entries(role):
            view.counter["Secret"] += 1
            secret_roles += f"**{role}** 🔁 {desc}\n"
        else:
            secret_roles += f"**???** 🔁 {desc}\n"

    view.data[index] = secret_roles
    view.footers[index] = ("All secret roles collected!" if view.counter["Secret"] == view.counter["AllSecret"] 
                        else f"{view.counter['Secret']} / {view.counter['AllSecret']} secret roles.")

    # --- PAGE 6: LOCKED ROLES (Limited & Removed) ---
    locked_roles = "## Limited Roles\n\n"
    for role, desc in FUN_ROLES["Limited"].items():
        view.counter["AllLocked"] += 1
        if str(target.id) in list_decoded_entries(role):
            view.counter["Locked"] += 1
            locked_roles += f"**{role}** 🔒 {desc}\n"
        else:
            locked_roles += f"**???** 🔒 {desc}\n"

    locked_roles += "\n## Removed Roles\n\n"
    for role, desc in FUN_ROLES["Removed"].items():
        if str(target.id) in list_decoded_entries(role):
            locked_roles += f"**{role}** ❌ {desc}\n"
        else:
            locked_roles += f"**???** ❌ {desc}\n"

    view.data[index + 1] = locked_roles
    view.footers[index + 1] = (f"{view.counter['Locked']} / {view.counter['AllLocked']} locked roles.")

    # --- DEVELOPER OVERRIDE ---
    if target.id in GIT_COMMITTERS.values():           
        view.data[index] = 'Empty...'
        view.data[index + 1] = 'Empty...'
        view.footers[index] = "This person knows how to get the roles, what's the point?"
        view.footers[index + 1] = "Nothing to see here."

#print tips
async def print_entries(channel, key):
    entries = list_entries(key)
    combined_string = ""
    for i in range(len(entries)):
        new_string = combined_string + str(i) + ") " + entries[i].decode("utf-8") + "\n"
        if len(new_string) > 2000:
            await SEND(channel,combined_string)
            combined_string = str(i) + ") " + entries[i].decode("utf-8") + "\n"
        else:
            combined_string = new_string
    await SEND(channel, combined_string)