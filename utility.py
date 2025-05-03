import random
from globals import FUN_ROLES, CHANNELS, EXTRA_ROLES, GIT_COMMITTERS, EVENTS
from rated import SEND

# Convert milliseconds to seconds
def cs_to_s(num):
    try:
        return f"{int(num) / 100:.2f} seconds" if int(num) != 0 else "Not Recorded"
    except (ValueError, TypeError):
        return "N/A" 