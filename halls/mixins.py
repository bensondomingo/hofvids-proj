from django.http import JsonResponse
from .models import Video, Hall
from django.urls import reverse_lazy


class AddVideoMixin(object):

    def form_invalid(self, form):
        if self.request.is_ajax():
            error = form.errors.get('url')[0]
            return JsonResponse({'error': error}, status=422)
        else:
            return super(AddVideoMixin, self).form_invalid(form)

    def form_valid(self, form):

        # Create and store Video object
        video = Video()
        video.title = form.cleaned_data['title']
        video.url = form.cleaned_data['url']
        video.youtube_id = form.cleaned_data['youtube_id']
        video.hall = Hall.objects.get(pk=self.kwargs.get('pk'))
        video.save()

        self.success_url = reverse_lazy('detailhall', kwargs=self.kwargs)

        if self.request.is_ajax():
            data = {
                'video_title': video.title,
                'hall_title': video.hall.title,
                'redirect_url': self.success_url,
            }
            return JsonResponse(data)
        else:
            return super(AddVideoMixin, self).form_valid(form)
