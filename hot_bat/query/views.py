from django.shortcuts import render

from .models import RegularData


def index(request):
	'''
	The main page view.
	'''

	top10results = RegularData.objects.order_by('avg')[:10]
	context = {'top10results': top10results}

	return render(request, 'query/index.html', context)

# def person_list(request):
#     table = PlayerTable(RegularData.objects.all())

#     return render(request, 'person_list.html', {
#         'table': table
#     })