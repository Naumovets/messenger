import time

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, Q
from django.http import JsonResponse

from dialogue.models import Dialogue, Message


def _get_my_dialogues(user: User) -> QuerySet:
    """ Находит все диалоги пользователя """
    return Dialogue.objects.filter(Q(user1=user) | Q(user2=user))


def _get_last_message_of_dialogue(dialogue: Dialogue) -> Message:
    """ Получает последнее сообщение диалога """
    return Message.objects.filter(dialogue=dialogue).last()


def get_my_dialogues_content(user: User) -> list:
    """ Формирует список диалогов пользователя
        С последними сообщениями в диалогах и id собеседника"""
    dialogues = _get_my_dialogues(user)
    if dialogues:
        content = []
        for dialogue in dialogues:
            message = _get_last_message_of_dialogue(dialogue)
            if message:
                content.append({
                    'dialogue': dialogue,
                    'last_message_author': 'Вы' if message.from_user == user else message.from_user.first_name,
                    'last_message': message.text,
                    'friend_id': message.to_user.pk if message.from_user == user else message.from_user.pk,
                })
            else:
                content.append({
                    'dialogue': dialogue,
                    'last_message_author': 'Админ',
                    'last_message': 'Ну напиши сюда хоть что-то...',
                    'friend_id': dialogue.user2.pk if dialogue.user1 == user else dialogue.user2.pk,
                })
        return content
    return []


def find_dialogue(user1: User, user2: int) -> Dialogue:
    """ Находит конкретный диалог 2 пользователей """
    try:
        return Dialogue.objects.get(Q(user1=user1) & Q(user2_id=user2) | Q(user1_id=user2) & Q(user2=user1))
    except:
        return None


def find_messages_in_dialogue(dialogue: Dialogue) -> QuerySet:
    """ Находит все сообщения в конкретном диалоге """
    return Message.objects.filter(dialogue=dialogue).order_by('time')


def update_reading_status_of_messages(dialogue: Dialogue) -> None:
    """ Обновляет статус непрочитанных сообщений на прочитанный """
    messages = Message.objects.filter(dialogue=dialogue)
    messages.update(is_read=True)


def long_poll(to_user: User, from_user_id: int) -> JsonResponse:
    """ Проверка сообщений с помощью long polling.
        Сервер не отвечает на запрос, пока не произойдет обновление
        т.е пока не появятся непрочитанные сообщения от собеседника """
    new_messages = Message.objects.filter(
        Q(to_user=to_user) & Q(from_user_id=from_user_id) & Q(is_read=False)).values(
        'text', 'from_user__first_name', 'from_user__last_name'
    )
    while len(new_messages) == 0:
        time.sleep(.5)
        new_messages = Message.objects.filter(
            Q(to_user=to_user) & Q(from_user_id=from_user_id) & Q(is_read=False)).values(
            'text', 'from_user__first_name', 'from_user__last_name'
        )
    result = JsonResponse({"data": list(new_messages)})
    new_messages.update(is_read=True)
    return result


def send_message(from_user: int, to_user: int, text: str) -> None:
    """ Сохраняет сообщение в базе данных """
    message = Message()
    message.from_user_id = from_user
    message.to_user_id = to_user
    try:
        dialogue = Dialogue.objects.get(
            Q(user1_id=from_user) & Q(user2_id=to_user) | Q(user1_id=to_user) & Q(user2_id=from_user))
    except ObjectDoesNotExist:
        dialogue = Dialogue()
        dialogue.user1_id = from_user
        dialogue.user2_id = to_user
        dialogue.save()
    message.dialogue = dialogue

    message.text = text
    message.save()


def check_exist_account(user_id: int) -> bool:
    return User.objects.filter(pk=user_id).exists()
