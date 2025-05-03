import random
from globals import FUN_ROLES, CHANNELS, EXTRA_ROLES, GIT_COMMITTERS, EVENTS
from rated import SEND

# Convert milliseconds to seconds
def ms_to_s(num):
    try:
        return f"{int(num) / 1000:.2f} seconds"
    except (ValueError, TypeError):
        return "N/A" 