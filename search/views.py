from braces.views import LoginRequiredMixin
from django.views.generic import ListView

from search.services.search_functions import find_people


class SearchView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'search/search.html'
    context_object_name = 'results'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return find_people(info=self.request.GET.get('info'))

