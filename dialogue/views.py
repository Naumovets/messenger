from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from dialogue.services.message_functions import get_my_dialogues_content, \
    find_dialogue, \
    find_messages_in_dialogue, \
    update_reading_status_of_messages, \
    long_poll, send_message


@login_required(login_url='login')
def home(request):
    content = get_my_dialogues_content(request.user)
    return render(request, 'dialogue/index.html',
                  {'title': "Диалоги", 'content': content})


class MessagesView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'dialogue/dialogue.html'
    context_object_name = 'messages'

    """
    Проблема в том, что у нас отображаются диалоги, которых на самом деле нет с сообщениями из других диалогов
    Не понятно почему так происходит, но сообщения из диалога между 1 и 2 есть в диалоге 1 и 1, а так же в 2 и 2
    Даже чужому пользователю будет доступен диалог.

    Ответ:
    Проблема заключалась в самом ListView, дело в том, что он выводит все данные модели, независимо от условий
    поэтому придется использовать def ...(request):
    
    update:
    Оказывается нужно указывать запросы в специальном методе get_queryset(self):
    
    """

    def get_queryset(self):
        dialogue = find_dialogue(self.request.user, self.kwargs['user_id'])
        if dialogue:
            messages = find_messages_in_dialogue(dialogue)
            update_reading_status_of_messages(dialogue)
            return messages
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auth'] = self.request.user.is_authenticated
        context['me'] = self.request.user.pk

        return context


def check_message_api(request):
    if request.method == 'POST':
        to_user = request.user
        from_user_id = request.POST.get('id', -1)

        return long_poll(to_user, from_user_id)


def send_message_api(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        to_user = request.POST.get('id', 0)
        from_user = request.user
        send_message(from_user=from_user.pk, to_user=to_user, text=text)
        return JsonResponse({"name": from_user.first_name, "lastname": from_user.last_name, "text": text})
