from django.shortcuts import render

from .models import RegularData


def index(request):
	'''
	The main page view.
	'''

	results = RegularData.objects.filter(shift=0).filter(noshift=0).filter(trad_shift=0).filter(shift=0).order_by('pa')[4000:4050]
	# Need to figure out how to sort descending
	context = {'results': results}

	return render(request, 'query/index.html', context)

def methodology(request):
	'''
	The methodology page view.
	'''

	return render(request, 'query/methodology.html')