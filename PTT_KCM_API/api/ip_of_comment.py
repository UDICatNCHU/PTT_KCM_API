from django.shortcuts import get_object_or_404, render_to_response, render
from django.utils import timezone # auto generate create time.
from django.http import JsonResponse, Http404
from functools import wraps
import json, re

class pttJson(object):
	"""	A pttJson object having api for web to query
    Args:
        filePath: path to ptt json file.

    Returns:
		ptt articles with specific issue.
    """
	def __init__(self, filePath='PTT_KCM_API/api/ptt.json'):
		self.filePath = filePath
		self.articleLists = []
		self.json = self._get_pttJson()

	def _get_pttJson(self):
		with open(self.filePath, 'r', encoding='utf8') as f:
			result = json.load(f)
		return result

	def get_articles(self):
		return self.articleLists

	def fileter_with_issue(self, issue):
		for i in self.json['articles']:
			if issue in i['article_title'] or issue in i['content']:
				self.articleLists.append(i)

def queryString_required(str):
	"""	An decorator checking whether queryString key is valid or not
    Args:
        str: allowed queryString key

    Returns:
        if contains invalid queryString key, it will raise exception.
    """
	def _dec(function):
	    @wraps(function)
	    def _wrap(request, *args, **kwargs):
	        if str not in request.GET or request.GET[str] == '':
	        	raise Http404("api does not exist")
	        return function(request, *args, **kwargs)
	    return _wrap
	return _dec

@queryString_required('issue')
def ip(request):
	"""Generate list of term data source files
    Returns:
        if contains invalid queryString key, it will raise exception.
    """
	p = pttJson()
	issue = request.GET['issue']
	p.fileter_with_issue(issue)
	return JsonResponse(p.get_articles(), safe=False)

