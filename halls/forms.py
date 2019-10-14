from django import forms
from .models import Hall, Video
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
import requests

YOUTUBE_API_KEY = 'AIzaSyDd_yJ-TyaWGzGNN0DyAC3rZPy9izKkjmQ'


class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ['title']


class AddVideoForm(forms.Form):
    url = forms.URLField(
        max_length=255, label='YouTube URL')
    search_term = forms.CharField(
        max_length=255, label='YouTube search', strip=True, required=False)

    def clean_url(self):
        url = self.cleaned_data['url']
        parsed_url = urlparse(url)
        if len(parsed_url.query.split('=')) < 2:
            raise ValidationError('%(value)s is not a YouTube URL.', params={'value': url})

        youtube_id = parsed_url.query.split('=')[1]
        try:
            response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={youtube_id}&key={YOUTUBE_API_KEY}')
        except requests.exceptions.HTTPError as http_err:
            pass
        else:
            rj = response.json()
            if len(rj.get('items')) != 1:
                raise ValidationError('Unable to find video with id %(value)s', params={'value': youtube_id})
            self.cleaned_data['youtube_id'] = youtube_id
            self.cleaned_data['title'] = rj.get('items')[0].get('snippet').get('title')
            return url


# class YoutubeUrlField(forms.CharField):

#     def validate(self, value):
#         parsed_url = urlparse(value)
#         if parsed_url.query.split('=') < 2:
#             raise ValidationError('Invalid URL: %(value)s',
#                                   params={'value': value})

#         youtube_id = parsed_url.query.split('=')[1]
#         try:
#             response = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={youtube_id}&key={YOUTUBE_API_KEY}')
#         except requests.exceptions.HTTPError as http_err:
#             pass
#         else:
#             rj = response.json()

#     def clean_




class SearchForm(forms.Form):
    search_term=forms.CharField(max_length = 255, label = 'YouTube search')
