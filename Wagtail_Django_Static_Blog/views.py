from django.shortcuts import render, redirect
from wagtail.core.models import Page
from wagtail.search.models import Query


def search(request):
    # Search
    search_query = request.GET.get('query', None)
    if search_query:
        search_results = Page.objects.live().search(search_query)

        # Log the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    # Render template
    return render(request, 'search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
    })

# Lets redirect user to last vistied page after login
'''def get_next_page(request):
    return request.GET.get('next', '')

def login(request):
	return render(request, 'auth/login.html', {'next_page': get_next_page(request)})'''
