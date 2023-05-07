from django.contrib.auth.models import User
from django.db.models import QuerySet, Q

from friend.models import Friend, FriendRequest


def my_friends(user: User) -> QuerySet:
    return Friend.objects.filter(Q(user1=user) | Q(user2=user))


def friend_requests(user: User) -> QuerySet:
    return FriendRequest.objects.filter(Q(from_user=user) | Q(to_user=user))
