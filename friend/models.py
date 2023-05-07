from django.contrib.auth.models import User
from django.db import models


class Friend(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1_friend", verbose_name="Пользователь 1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2_friend", verbose_name="Пользователь 2")


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user_friend_request",
                                  verbose_name="Пользователь 1")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user_friend_request",
                                verbose_name="Пользователь 2")
