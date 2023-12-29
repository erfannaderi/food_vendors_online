from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from accounts.forms import RegisterClientForm
from accounts.models import User
from vendor.forms import RestaurantForm


# Create your views here.
class RegisterClientView(TemplateView):
    template_name = 'accounts/register-client.html'

    def get(self, request, *args, **kwargs):
        form = RegisterClientForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterClientForm(request.POST)
        if form.is_valid():
            # Process the form data
            # create user using form

            # password = form.cleaned_data
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CLIENT
            # form.save()

            # create a user using create_user method

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                            password=password)
            user.role = User.CLIENT
            user.save()
            messages.success(request, "Successfully created a new user")
            return redirect('register_client')
        return render(request, self.template_name, {'form': form})


class RegisterRestaurantView(TemplateView):
    template_name = 'accounts/register-restaurant.html'

    def get(self, request, *args, **kwargs):
        client_form = RegisterClientForm
        restaurant_form = RestaurantForm
        return render(request, self.template_name, {'client_form': client_form, 'restaurant_form': restaurant_form})

    def post(self, request, *args, **kwargs):
        client_form = RegisterClientForm(request.POST)
        restaurant_form = RestaurantForm(request.POST)
        if client_form.is_valid():
            # user = client_form.save(commit=False)
            # user.set_password(client_form.cleaned_data['password'])
            # user.role = User.RESTAURANT
            # user.save()
            #
            # restaurant = restaurant_form.save(commit=False)
            # # Assuming there's a foreign key field in RestaurantForm pointing to the User model
            # restaurant.user = user
            # restaurant.save()
            first_name = client_form.cleaned_data['first_name']
            last_name = client_form.cleaned_data['last_name']
            username = client_form.cleaned_data['username']
            email = client_form.cleaned_data['email']
            password = client_form.cleaned_data['password']
            # return HttpResponse(last_name)
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                            password=password)
            user.role = User.RESTAURANT
            user.save()
            restaurant = restaurant_form.save()
            restaurant.user = user
            user_profile = user.objects.get(user=user)

            # resturant.user_profile = user_profile.
        else:
            return render(request, self.template_name, {'client_form': client_form, 'restaurant_form': restaurant_form})

        return render(request, self.template_name, {'client_form': client_form, 'restaurant_form': restaurant_form})
