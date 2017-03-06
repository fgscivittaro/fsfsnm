from django.shortcuts import render

from .models import RegularData

def index(request):
	'''
	The main page view.
	'''

	top10results = RegularData.objects.order_by('avg')[:10]
	context = {'top10results': top10results}

	return render(request, 'query/index.html', context)