def motor_time(n: int):
    tm ='{:02d}:{:02d}'.format(*divmod(n, 60))
    print(tm)
    result = int(tm[0]) + int(tm[1]) + int(tm[3]) + int(tm[4])
    return result


def level_up (xpNow, levelUp, xpGet: int) -> bool:
    return xpNow + xpGet >= levelUp


from datetime import datetime
def time_converter(timeStr: str) -> str:
    full_h = datetime.strptime(timeStr, "%H:%M")
    part_h = full_h.strftime("%I:%M %p").lower().replace('pm', 'p.m.').replace('am', 'a.m.').lstrip('0')
    return part_h

