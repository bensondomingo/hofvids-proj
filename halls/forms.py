from django.forms import Form, ModelForm
from .models import Hall, Video

# class HallForm(forms.Form):
#     title = forms.CharField(label='Hall title', max_length=255)

class HallForm(ModelForm):
    class Meta:
        model = Hall
        fields = ['title']

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'url', 'youtube_id']
        labels = {
            'youtube_id': 'YouTube Id'
        }