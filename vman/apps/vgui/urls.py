from django.conf.urls import url

from apps.vgui.views import CorpusListView, CorpusCompareView

urlpatterns = [
    url(
        r'^corpus/compare/$',
        CorpusCompareView.as_view(),
        name='corpus_compare'
    ),
    url(
        r'^corpus/$',
        CorpusListView.as_view(),
        name='corpus'
    ),
]
