import random
from globals import RIG_LIST, EMOJIS_TO_REACT
from rated import SEND

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