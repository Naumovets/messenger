from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy


class Dialogue(models.Model):
    user1 = models.ForeignKey(User, 
                                on_delete=models.CASCADE,
                                verbose_name="Первый пользователь",
                                related_name="user1")
    user2 = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                verbose_name="Второй пользователь",
                                related_name="user2")


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                  verbose_name="Первый пользователь",
                                  related_name="from_user")
    to_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    verbose_name="Второй пользователь",
                                    related_name="to_user")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Дата сообщения")
    is_read = models.BooleanField(default="False", verbose_name="Прочитано")
    text = models.CharField(max_length=8192, verbose_name="Сообщение")
    dialogue = models.ForeignKey(Dialogue,
                                    on_delete=models.CASCADE,
                                    verbose_name="Диалог",
                                    related_name="dialogue")

    def get_absolute_url(self):
        return reverse_lazy('dialogues', kwargs={'user_id': self.to_user.pk})

    def __str__(self):
        return f"{self.from_user.first_name} {self.from_user.last_name} {self.text}"
