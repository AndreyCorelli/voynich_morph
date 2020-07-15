from django.views.generic import ListView

from apps.vnlp.corpus_manager import CorpusManager
from apps.vnlp.training.corpus_features import CorpusFeatures


class CorpusListView(ListView):
    model = CorpusFeatures
    template_name = 'vgui/corpusfeatures_list.html'
    context_object_name = "corpusfeatures_list"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object_list = CorpusManager.read_corpus_by_text(False, True)
        context = {
            'paginator': None,
            'page_obj': None,
            'is_paginated': False,
            'object_list': self.object_list
        }
        return self.render_to_response(context)
