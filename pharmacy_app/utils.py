from django.utils import timezone

from .models import OperatingHours


def open_now_map(pharmacy_ids):
    """
    {pharmacy_id: True/False/None} -- True = open right now, False = closed,
    None = the pharmacy hasn't set hours for today.
    """
    now = timezone.localtime()
    result = {pid: None for pid in pharmacy_ids}
    rows = OperatingHours.objects.filter(
        pharmacy_id__in=list(pharmacy_ids), days_of_week=now.weekday()
    )
    for row in rows:
        if row.is_closed or not row.opening_time or not row.closing_time:
            result[row.pharmacy_id] = False
        else:
            result[row.pharmacy_id] = row.opening_time <= now.time() <= row.closing_time
    return result
