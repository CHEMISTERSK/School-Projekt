
def ingame_t(current_time):
    total_seconds = int(current_time / 1000)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    ingame_time = f"{minutes:02d}:{seconds:02d}"
    return ingame_time