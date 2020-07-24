import json
import os
import urllib.parse

from django import forms
from django.http import JsonResponse
from django.views.generic import ListView, TemplateView, FormView

from apps.vgui.models.corpus_brief import CorpusBrief
from apps.vnlp.corpus_manager import CorpusManager
from apps.vnlp.training.alphabet import alphabet_by_code
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
        elif 'corpus_path' in request.POST:
            data = self.read_corpus_brief(request.POST['corpus_path']).to_dict()
        return JsonResponse(data, safe=False)

    def form_valid(self, form):
        return True

    def read_corpus_brief(self, corpus_path: str):
        features = CorpusManager.get_cached_corpus_by_path(corpus_path)
        brief = CorpusBrief()
        brief.build_from_corpus(features)
        return brief

    def read_corpus_paths(self):
        file_paths = CorpusManager.get_cached_corpus_file_paths()
        discrete_paths = {}
        path_by_language = {}
        for p, l in file_paths:
            if not l:
                lang_name = os.path.splitext(os.path.basename(p))[0]
                path_by_language[lang_name] = p
                continue
            paths_list = discrete_paths.get(l)
            if not paths_list:
                paths_list = []
                discrete_paths[l] = paths_list
            paths_list.append((os.path.basename(p), p,))

        language_title = {l: alphabet_by_code[l].title for l in alphabet_by_code}

        for l in discrete_paths:
            discrete_paths[l].sort(key=lambda p: p[0])

        return {
            'discrete_paths': discrete_paths,
            'language_title': language_title,
            'path_by_language': path_by_language
        }
