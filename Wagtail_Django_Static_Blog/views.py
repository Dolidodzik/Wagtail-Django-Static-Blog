from django.shortcuts import render, redirect

# Lets redirect user to last vistied page after login
def get_next_page(request):
    return request.GET.get('next', '')

def login(request):
	return render(request, 'auth/login.html', {'next_page': get_next_page(request)})
