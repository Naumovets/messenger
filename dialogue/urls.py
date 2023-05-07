from django.urls import path

from dialogue.views import home, MessagesView, check_message_api, send_message_api

urlpatterns = [
    path('', home, name='messages'),
    path('dialogue/<int:user_id>', MessagesView.as_view(), name='dialogue'),
    path('api/v1/check-message', check_message_api, name='check_message'),
    path('api/v1/long-poll', send_message_api, name='check_message'),

]
