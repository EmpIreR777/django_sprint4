from django import forms
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

from .models import Post, User, Comment


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class PostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        label='Дата и время публикации',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    class Meta:
        model = Post
        exclude = ('author',)

    def clean(self):
        super().clean()
        send_mail(
            subject="Новая публикация!",
            message=f"Новая публикация \"{self.cleaned_data.get('title')}\"."
            f"с названием {self.cleaned_data['title']}",
            from_email="publicat_form@blogicum.not",
            recipient_list=["admin@blogicum.not"],
            fail_silently=True,
        )
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
