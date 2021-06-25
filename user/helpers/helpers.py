import datetime


def generate_ot_confirmation_code(date_time):
    var = str(date_time).split(':')
    var[-1] = var[-1].replace('.', '')
    return var[-1]


def get_time_between(first_time: datetime, later_time: datetime) -> int:
    difference = later_time - first_time
    datetime.timedelta(0, 8, 562000)
    seconds_in_day = 24 * 60 * 60
    time_between = divmod(difference.days * seconds_in_day +
                          difference.seconds, 60)
    return time_between[1]
