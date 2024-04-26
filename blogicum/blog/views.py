from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


from .form import PostForm
from blog.models import Post, Category
from core.constants import MAX_POSTS


def get_filtered_list():
    return Post.objects.select_related('category', 'location', 'author').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    exclude = ('pub_date',)
    template_name = 'blog/create.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class IndexListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = get_filtered_list()
    ordering = '-pub_date'
    paginate_by = MAX_POSTS


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    queryset = get_filtered_list()


class CategotyListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        category_slug = self.kwargs['category_slug']
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=category_slug)
        context['category'] = category
        context['page_obj'] = get_filtered_list().filter(category=category)
        return context


class RegistrCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')
