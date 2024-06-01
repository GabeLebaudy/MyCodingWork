import re

new_patterns = ["5:433RD QUARTER", "8:35AM", "MIN Timberwolves", "IND Pacers", "BOS Celtics", "DAL Mavericks", "10:243RD QUARTER"]
for new_pattern in new_patterns:
    found_match = re.match("[0-9]:[0-9][0-9][0-9]", new_pattern)
    if found_match:
        match_text = found_match.group().split(':')
        print(match_text)
        minute, seconds, quarter = int(match_text[0]), match_text[1][:-1], int(match_text[1][-1])
        
        live_time_remaining = str(((4 - quarter) * 12) + minute) + ":" + seconds
        print("Live time remaining:", live_time_remaining)