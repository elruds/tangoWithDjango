from django.shortcuts import render

from django.http import HttpResponse

from rango.models import Category

from rango.models import Page

def index(request):
	#return HttpResponse("Rango says hey there partner! <br/><a href='/rango/about/'>About</a>")
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5] #added 25 Jan 17 by LAR
	context_dict = {'categories': category_list, 'pages': page_list} #{'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	return render(request, 'rango/index.html', context_dict)


def about(request):
	#return HttpResponse("Rango says here is the about page. <a href="/rango/">Index</a>")
	return render(request, 'rango/about.html')


def show_category(request, category_name_slug):
	context_dict = {}



	try:
		category = Category.objects.get(slug=category_name_slug)

		pages = Page.objects.filter(category=category)

		context_dict['pages'] = pages

		context_dict['category'] = category
	except Category.DoesNotExist:

		context_dict['category'] = None
		context_dict['pages'] = None


	return render(request, 'rango/category.html', context_dict)