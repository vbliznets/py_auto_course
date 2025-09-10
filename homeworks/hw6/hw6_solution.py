from datetime import datetime


def motor_time(n: int):
    hh, mm = divmod(n, 60)
    tm = f"{hh: 02d}: {mm: 02d}"
    print(tm)
    result = int(tm[0]) + int(tm[1]) + int(tm[3]) + int(tm[4])
    return result


def level_up(xp_now, lv_up, xp_get: int) -> bool:
    return xp_now + xp_get >= lv_up


def time_converter(time_str: str) -> str:
    full_h = datetime.strptime(time_str, "%H:%M")
    part_h = full_h.strftime("%I:%M %p").lower().replace('pm', 'p.m.')\
        .replace('am', 'a.m.').lstrip('0')
    return part_h
