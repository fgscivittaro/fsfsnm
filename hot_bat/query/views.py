from django.shortcuts import render

from .models import RegularData


def index(request):
	'''
	The main page view.
	'''

	top50results = RegularData.objects.order_by('pa')[:50]
	context = {'top50results': top50results}

	return render(request, 'query/index.html', context)
