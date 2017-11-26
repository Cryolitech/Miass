import datetime

# Obtain the UTC Offset for the current system:
def get_utc_offset_timezone(local_time_utc, unix_timestamp):
    UTC_OFFSET_TIMEDELTA = datetime.datetime.fromtimestamp(unix_timestamp) - local_time_utc
    result_utc_datetime = local_time_utc + UTC_OFFSET_TIMEDELTA
    return result_utc_datetime.hour - local_time_utc.hour

def get_time_from_another_timezone(current_time,UTC_offset):
    current_time_in_utc = datetime.datetime.now()
    return current_time_in_utc + datetime.timedelta(hours=UTC_offset)
