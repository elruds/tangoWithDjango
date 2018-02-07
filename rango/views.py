from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from rango.models import Category

from rango.models import Page

from rango.forms import CategoryForm

from rango.forms import PageForm

from rango.forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login, logout

from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required


def index(request):
	#return HttpResponse("Rango says hey there partner! <br/><a href='/rango/about/'>About</a>")
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5] #added 25 Jan 17 by LAR
	context_dict = {'categories': category_list, 'pages': page_list} #{'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	return render(request, 'rango/index.html', context_dict)


def about(request):
	#return HttpResponse("Rango says here is the about page. <a href="/rango/">Index</a>")
	return render(request, 'rango/about.html', {})


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


def add_category(request):
	form = CategoryForm()

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit = True)

			return index(request)
		else:

			print(form.errors)

	return render(request, 'rango/add_category.html', {'form': form})



def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug = category_name_slug)
	except Category.DoesNotExist:
		category = None

	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)

		else:
			print(form.errors)

	context_dict = {'form':form, 'category':category}
	return render(request, 'rango/add_page.html', context_dict)


# def register(request):
# 	registered = False

# 	if request.method == 'POST':

# 		user_form = UserForm(data=request.POST)
# 		profile_form = UserProfileForm(data=request.POST)

# 		if user_form.is_valid() and profile_form.is_valid():
# 			user = user_form.save()

# 			user.set_password(user.password)
# 			user.save()

# 			profile = profile_form.save(commit=False)
# 			profile.user = user

# 			if 'picture' in request.FILES:
# 				profile.picture = request.FILES['picture']

# 				profile.save()

# 				registered = True

# 			else:
# 				print(user_form.errors, profile_form.errors)

# 		else:
# 			user_form = UserForm()
# 			profile_form = UserProfileForm()

# 		return render(request, 'rango/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})

def register(request):
	# A boolean value for telling the template
	# whether the registration was successful.
	# Set to False initially. Code changes value to
	# True when registration succeeds.
	registered = False
	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
	# Attempt to grab information from the raw form information.
	# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		# If the two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()
			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()
			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves,
			# we set commit=False. This delays saving the model
			# until we're ready to avoid integrity problems.

			profile = profile_form.save(commit=False)
			profile.user = user
			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and
			#put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				# Now we save the UserProfile model instance.
				profile.save()
				# Update our variable to indicate that the template
				# registration was successful.
				registered = True
			else:
					# Invalid form or forms - mistakes or something else?
					# Print problems to the terminal.
				print(user_form.errors, profile_form.errors)
	else:
		# Not a HTTP POST, so we render our form using two ModelForm instances.
		# These forms will be blank, ready for user input.
		user_form = UserForm()
		profile_form = UserProfileForm()
		# Render the template depending on the context.
	return render(request,
	'rango/register.html',
	{'user_form': user_form,
	'profile_form': profile_form,
	'registered': registered})

def user_login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your Rango account is disabled.")

		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")

	else:
		return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
	return render(request, 'rango/restricted.html', {})

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse ('index'))


