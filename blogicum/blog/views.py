from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DetailView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.core.mail import send_mail

from .forms import PostForm, CommentForm
from blog.models import Post, Category, User, Comment
from core.constants import (
    PAGINATOR_POST, PAGINATOR_PROFILE, PAGINATOR_CATEGORY)


def get_filtered_posts():
    return (
        Post.objects.select_related('category', 'location', 'author')
        .filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )


class PostDispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Post,
            pk=kwargs.get("post_id"),
        )
        if instance.author != request.user:
            return redirect("blog:post_detail", self.kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)


class CommentMixin:
    model = Comment
    template_name = "blog/comment.html"


class IndexListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = get_filtered_posts()
    paginate_by = PAGINATOR_POST


class ProfileListView(ListView):
    paginate_by = PAGINATOR_PROFILE
    template_name = 'blog/profile.html'
    model = Post

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        user = self.get_object()
        if self.request.user != user:
            return (
                user.posts.filter(is_published=True)
                .annotate(comment_count=Count('comments'))
                .order_by('-pub_date')
            )
        return (
            user.posts.all()
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/user.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('blog:edit_profile')

    def get_object(self, queryset=None):
        return self.request.user


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def send_mail(self, form):
        send_mail(
            subject='Новая публикация!',
            message=f'с названием {form.cleaned_data["title"]}',
            from_email='publicat_form@blogicum.not',
            recipient_list=['admin@blogicum.not'],
            fail_silently=True,
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.send_mail(form)
        return super().form_valid(form)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related(
            'author').order_by(
            'created_at'
        )
        return context

    def get_queryset(self):
        q = Q(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )
        if self.request.user.is_authenticated:
            q |= Q(author=self.request.user)
        return Post.objects.select_related(
            'category', 'location', 'author').filter(q)


class PostDeleteView(PostDispatchMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy("blog:index")


class PostUpdateView(PostDispatchMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    exclude = ('-pub_date',)
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])


class CategoryListView(LoginRequiredMixin, ListView):
    paginate_by = PAGINATOR_CATEGORY
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'category'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True
        )
        return get_filtered_posts().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    post_instance = None
    form_class = CommentForm
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_instance
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={
            'post_id': self.post_instance.pk})


class CommentUpdateView(CommentMixin, LoginRequiredMixin, UpdateView):
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs.get('comment_id'))
        if self.request.user != instance.author:
            return redirect('blog:post_detail', self.kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )


class CommentDeleteView(CommentMixin, LoginRequiredMixin, DeleteView):
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('comment_id'))
        if self.request.user != comment.author:
            raise PermissionDenied('Вы не имеете разрешения на это действие.')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
        )
