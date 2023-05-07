from django.contrib.auth.models import User
from django.db.models import QuerySet, Q


def find_people(info: str) -> QuerySet:
    if info is not None:
        info_as_list = info.split()
        return User.objects.filter(
            Q(first_name__in=info_as_list) | Q(last_name__in=info_as_list) |
            Q(first_name__icontains=info) | Q(last_name__icontains=info))
    else:
        return User.objects.filter(
            Q(first_name__icontains=info) | Q(last_name__icontains=info))
