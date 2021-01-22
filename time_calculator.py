import re

def add_time(start, duration, starting_day=''):

    # extract hrs, mins, AM/PM from start. Convert from 12 hrs to 24 hrs format and build
    # a dictionary (start_d) with hrs and mins
    pattern = '([0-9]+):([0-9]+) ([APM]+)'
    l = [x for x in re.findall(pattern, start)[0]]
    l[0], l[1] = int(l[0]), int(l[1])
    if l[2] == 'PM': l[0] += 12
    start_d = {'hrs': l[0], 'mins': l[1]}

    # create dictionary of duration hrs and mins
    dur_list = duration.split(':')
    dur_d = {'hrs': int(dur_list[0]), 'mins': int(dur_list[1])}
    dur_d['hrs'] = dur_d['hrs'] + (start_d['mins'] + dur_d['mins']) // 60

    # processing ...
    mins = (start_d['mins'] + dur_d['mins']) % 60
    if (start_d['hrs'] + dur_d['hrs']) % 12 == 0:
        hrs = 12
    else:
        hrs = (start_d['hrs'] + dur_d['hrs']) % 12
    period = ''
    if (start_d['hrs'] + dur_d['hrs']) % 24 >= 12:
        period += 'PM'
    else:
        period += 'AM'
    no_of_days = (start_d['hrs'] + dur_d['hrs']) // 24

    # building string with new time
    weekday = {1: 'Monday', 2: "Tuesday", 3: "Wednesday", 4: "Thursday",
            5: "Friday", 6: "Saturday", 7: "Sunday"}
    if not starting_day:
        new_time = f'{hrs}:{mins:02d} {period}'
        if no_of_days == 1:
            new_time += f' (next day)'
        elif no_of_days > 1:
            new_time += f' ({no_of_days} days later)'
    else:
        new_time = f'{hrs}:{mins:02d} {period}, '
        for k, v in weekday.items():
            if starting_day.title() == v:
                if (k + no_of_days) % 7 == 0:
                    weekday_index = 7
                else:
                    weekday_index = (k + no_of_days) % 7
                new_time += f'{weekday[weekday_index]}'
        if no_of_days == 1:
            new_time += f' (next day)'
        elif no_of_days > 1:
            new_time += f' ({no_of_days} days later)'

    # return start_d, dur_d, hrs, mins, period, no_of_days
    return new_time