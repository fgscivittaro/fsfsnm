from django.shortcuts import render

from .models import RegularData, Regression, Marcel


def index(request):
	'''
	The main page view.
	'''

	url_params = request.GET

	search = request.GET.get('q')
	year = request.GET.get('year')
	team = request.GET.get('team')
	pa = request.GET.get('pa')

	baseQuery = RegularData.objects\
		.filter(shift=0).filter(noshift=0)\
		.filter(trad_shift=0).filter(shift=0)

	if search:
		baseQuery = baseQuery.filter(name__icontains=search)
	if year:
		baseQuery = baseQuery.filter(year=year)
	if team:
		baseQuery = baseQuery.filter(team=team)
	if pa:
		baseQuery = baseQuery.filter(pa__gte=int(pa))
	
	# import pdb; pdb.set_trace();

	years = RegularData.objects\
		.values_list('year', flat=True)\
		.distinct()

	team_names = RegularData.objects\
		.values_list('team', flat=True)\
		.distinct()

	results = baseQuery.order_by('pa')[0:50]

	player_ids = []
	for player in results:
		player_ids.append(player.player_id)

	marcel = Marcel.objects.filter(player_id__in=list(player_ids))
	regression = Regression.objects.filter(player_id__in=list(player_ids))

	marcel_dict = {}
	for m in marcel:
		marcel_dict[m.player_id] = m

	regression_dict = {}
	for r in regression:
		regression_dict[r.player_id] = r

	for result in results:
		result.marcel = marcel_dict.get(result.player_id)
		result.regression = regression_dict.get(result.player_id)

	context = {
		'results': results,
		'years': years,
		'team_names': team_names,
		'url_params': url_params,
		'pa_range': ["500", "450", "400", "350", "300", "250", "200", "150", "100", "50"],
	}
	return render(request, 'query/index.html', context)

def methodology(request):
	'''
	The methodology page view.
	'''

	return render(request, 'query/methodology.html')