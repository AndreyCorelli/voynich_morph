import urllib.parse

from django import forms
from django.http import JsonResponse
from django.views.generic import ListView, TemplateView, FormView

from apps.vnlp.corpus_manager import CorpusManager
from apps.vnlp.training.corpus_features import CorpusFeatures
from corpus.corpus_data import CORPUS_ROOT


class CorpusListView(ListView):
    model = CorpusFeatures
    template_name = 'vgui/corpusfeatures_list.html'
    context_object_name = "corpusfeatures_list"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object_list = CorpusManager.read_corpus_by_lang(CORPUS_ROOT, False, False)
        for corpus in self.object_list:
            setattr(corpus, 'url', f'/{urllib.parse.quote_plus(corpus.cache_file_path)}')
        content = {
            'paginator': None,
            'page_obj': None,
            'is_paginated': False,
            'object_list': self.object_list
        }
        return self.render_to_response(content)


class CorpusCompareView(FormView):
    template_name = 'vgui/corpusfeatures.html'
    form_class = forms.Form

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})

    def post(self, request, *args, **kwargs):
        data = {}
        if 'list' in request.POST:
            data = self.read_corpus_paths()
        return JsonResponse(data)

    def form_valid(self, form):
        return True

    def read_corpus_paths(self):
        file_paths = CorpusManager.get_cached_corpus_file_paths()
        return {
            'discrete_paths': [(p, l,) for p, l in file_paths if l],
            'language_paths': [(p, l,) for p, l in file_paths if not l]
        }
