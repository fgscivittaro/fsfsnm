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
	position = request.GET.get('position')
	pa = request.GET.get('pa')
	min_woba = request.GET.get('min_woba')
	max_woba = request.GET.get('max_woba')
	sort = request.GET.get('sort')

	baseQuery = Marcel.objects

	if search:
		baseQuery = baseQuery.filter(name__icontains=search)
	if year:
		baseQuery = baseQuery.filter(year=year)
	if team:
		baseQuery = baseQuery.filter(team=team)
	if pa:
		baseQuery = baseQuery.filter(pa__gte=int(pa))
	if min_woba:
		baseQuery = baseQuery.filter(woba__gte=float(min_woba))
	if max_woba:
		baseQuery = baseQuery.filter(woba__lte=float(max_woba))

	if position:
		baseQuery = baseQuery.filter(position__contains=position)

	years = Marcel.objects\
		.values_list('year', flat=True)\
		.distinct()

	team_names = Marcel.objects\
		.values_list('team', flat=True)\
		.distinct()

	if sort == 'name':
		results = baseQuery.order_by(''+sort)[0:50]
	elif sort == 'age' or 'pa':
		results = baseQuery.order_by('-'+sort)[0:50]
	else:
		results = baseQuery.order_by('-woba')[0:50]

	player_ids = []
	for player in results:
		if player.player_id != "player_id":
			player_ids.append(player.player_id)

	regression = Regression.objects.filter(player_id__in=list(player_ids))

	regression_dict = {}
	for r in regression:
		regression_dict[r.player_id] = r

	for result in results:
		result.regression = regression_dict.get(result.player_id)

	context = {
		'results': results,
		'sort_by': ['age', 'pa', 'name'],
		'years': ['2016','2017'],
		'min_woba_values': ['0.250', '0.275', '0.300', '0.325', '0.350', '0.375', '0.400'],
		'max_woba_values': ['0.400', '0.375', '0.350', '0.325', '0.300', '0.275', '0.250'],
		'team_names': ['Angels',
 'Astros',
 'Athletics',
 'Blue Jays',
 'Braves',
 'Brewers',
 'Cardinals',
 'Cubs',
 'Diamondbacks',
 'Dodgers',
 'Giants',
 'Indians',
 'MarinersRays',
 'Marlins',
 'Mets',
 'Nationals',
 'Orioles',
 'Padres',
 'Phillies',
 'Pirates',
 'Rangers',
 'Red Sox',
 'Reds',
 'Rockies',
 'Royals',
 'Tigers',
 'Twins',
 'White Sox',
 'Yankees'],
		'positions':['DH', 'C', '1B', '2B', '3B','SS', 'OF', 'PH','PR'],
		'url_params': url_params,
		'pa_range': ["650", "600", "550", "500", "450", "400", "350", "300", "250", "200", "150", "100", "50"],
	}
	return render(request, 'query/index.html', context)

def methodology(request):
	'''
	The methodology page view.
	'''

	return render(request, 'query/methodology.html')