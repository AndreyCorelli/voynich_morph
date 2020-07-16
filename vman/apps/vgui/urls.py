from django.conf.urls import url

from apps.vgui.views import CorpusListView

urlpatterns = [
    url(
        r'^corpus/$',
        CorpusListView.as_view(),
        name='corpus'
    ),
]