from typing import Any
from django.db.models.base import Model as Model
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from blog.models import User, Post


class ProfileDetailView(DetailView):
    template_name = 'users/profile.html'
    queryset = User.objects.all()
    slug_url_kwarg = 'username'
    slug_field = 'username'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.select_related('author', 'category').filter(
            is_published=True, category__is_published=True, author=self.object
        )
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/user.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('users:edit_profile')

    def get_object(self, queryset=None):
        return self.request.user
