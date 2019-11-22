import datetime as dt

def parse_str_to_date(date_str):
    """
    Recieves a Date String (e.g. 2019-10-09)
    and returns a datetime object
    """
    #T22:25:00-03:00
    if type(date_str) != str:
        return None

    return dt.datetime(
        int(date_str[0:4]), #Year
        int(date_str[5:7]), #Month
        int(date_str[8:10]), #Day
    )