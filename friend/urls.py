from django.urls import path

from friend.views import ListFriends

urlpatterns = [
    path('', ListFriends.as_view(), name='friends'),

]