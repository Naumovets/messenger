from braces.views import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from friend.services.friends_functions import my_friends, friend_requests


class ListFriends(LoginRequiredMixin, ListView):
    login_url = 'login'
    context_object_name = 'friends'
    template_name = 'friend/friends.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListFriends, self).get_context_data(**kwargs)
        context['friend_requests'] = friend_requests(self.request.user)
        return context

    def get_queryset(self):
        return my_friends(self.request.user)


def cancel_request_friend_api(request):
    return JsonResponse()


def accept_request_friend_api(request):
    return JsonResponse()


