from .models import Comment, Media, Image, Video
from django import forms
from betterforms.multiform import MultiForm

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class SearchForm(forms.Form):
    q = forms.CharField()

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ("media",)

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = ("media",)

class PostForm(forms.ModelForm):
    class Meta:
        model = Media
        exclude = ("created", "updated", 'last_seen', 'views')
        # fields = ('image', 'video')

class AdminCreateForm(MultiForm):
    form_classes = {
        'post': PostForm,
        'image': ImageForm,
        'video': VideoForm,
    }
