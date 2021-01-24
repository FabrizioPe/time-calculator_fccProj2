import re


def extract_times(start, duration):
    """
    Takes the problem data and extracts relevant information for processing.
    :param start: string of start time (ex: "10:50 PM")
    :param duration: string duration to be added to start time (ex: "2:15")
    :return: two dictionaries containing the data of interest in numerical form
            (ex: {'hrs': 22, 'mins': 50}, {'hrs': 3, 'mins': 15}.
    [Pay attention to the second dictionary with hours 2+1 because 50+15 >= 60]
    """
    # extracting hrs and mins from start time
    pattern = '([0-9]+):([0-9]+) ([APM]+)'
    hrs_mins_ampm = [x for x in re.findall(pattern, start)[0]]
    hrs_mins_ampm[0], hrs_mins_ampm[1] = int(hrs_mins_ampm[0]), int(hrs_mins_ampm[1])
    if hrs_mins_ampm[2] == 'PM': hrs_mins_ampm[0] += 12  # convert to 24-hours format
    start_d = {'hrs': hrs_mins_ampm[0], 'mins': hrs_mins_ampm[1]}

    # extracting hrs and mins from duration time
    dur_list = duration.split(':')
    dur_d = {'hrs': int(dur_list[0]), 'mins': int(dur_list[1])}
    dur_d['hrs'] = dur_d['hrs'] + (start_d['mins'] + dur_d['mins']) // 60  # see docstring for explan.

    return start_d, dur_d


def processing_data(start_d, dur_d, starting_day=''):
    """
    Takes two dictionaries with input data and returns a dict. with all the data
    that constitutes the answer to the problem.
    :param start_d: dict. with hrs and mins of start time
    :param dur_d: dict. with hrs and mins of duration time
    :param starting_day: optional parameter
    :return: dict. with [mins, hrs, period(AM or PM),
        number_of_days_elapsed(0 to inf.), [final day if starting_day specified]]
    """
    # calculating minutes
    mins = (start_d['mins'] + dur_d['mins']) % 60
    # calculating hours and period (AM or PM)
    hrs = (start_d['hrs'] + dur_d['hrs']) % 12
    if hrs == 0:
        hrs = 12
    if (start_d['hrs'] + dur_d['hrs']) % 24 >= 12:
        period = 'PM'
    else:
        period = 'AM'
    # calculating elapsed days since start time:
    no_of_days = (start_d['hrs'] + dur_d['hrs']) // 24
    # calculating final day
    if starting_day:
        weekday = ('fakeday', 'Monday', "Tuesday", "Wednesday", "Thursday",
                   "Friday", "Saturday", "Sunday")
        k = weekday.index(starting_day.title())
        weekday_index = (k + no_of_days) % 7
        if weekday_index == 0: weekday_index = 7;
        final_day = weekday[weekday_index]
    else:
        final_day = ''

    return {'hrs': hrs, 'mins': mins, 'period': period,
            'no_of_days': no_of_days, 'final_day': final_day}


def new_time_str(d):
    """
    Takes the dictionary with new time data and returns the string in the
    specified format.
    Ex. of output: "12:03 AM, Thursday (2 days later)"
    """

    new_time = f"{d['hrs']}:{d['mins']:02d} {d['period']}"
    if not d['final_day']:
        if d['no_of_days'] == 1:
            new_time += f' (next day)'
        elif d['no_of_days'] > 1:
            new_time += f" ({d['no_of_days']} days later)"
    else:
        new_time += f", {d['final_day']}"
        if d['no_of_days'] == 1:
            new_time += f' (next day)'
        elif d['no_of_days'] > 1:
            new_time += f" ({d['no_of_days']} days later)"

    return new_time


def add_time(start, duration, starting_day=''):
    """
    Takes the start time, the duration to add and returns the final time
    in a proper string format.
    """

    # put the data in a dict. form
    start_d, dur_d = extract_times(start, duration)
    # return a dict. with end-time data
    end_d = processing_data(start_d, dur_d, starting_day)

    return new_time_str(end_d)
