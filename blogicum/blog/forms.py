from django import forms
from django.core.mail import send_mail
from django.utils import timezone
from .models import Post, User, Comment


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.localtime(
            timezone.now()).strftime(
            '%Y-%m-%dT%H:%M'
        ) 

    pub_date = forms.DateTimeField(
        label='Дата и время публикации',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )

    class Meta:

        model = Post
        exclude = ('author',)

    def clean(self):
        super().clean()
        send_mail(
            subject='Новая публикация!',
            message=f'с названием {self.cleaned_data["title"]}',
            from_email='publicat_form@blogicum.not',
            recipient_list=['admin@blogicum.not'],
            fail_silently=True,
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
