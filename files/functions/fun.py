
def ingame_time(current_time):
    total_seconds = int(current_time / 1000)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"