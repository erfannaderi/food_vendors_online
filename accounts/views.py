from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from accounts.forms import RegisterClientForm
from accounts.models import User


# Create your views here.
class RegisterClientView(TemplateView):
    template_name = 'accounts/register-restaurant.html'  # Replace 'your_template_name.html' with the actual template name

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
            messages.success(request,"Successfully created a new user")
            return redirect('register_client')
        return render(request, self.template_name, {'form': form})


class RegisterRestaurantView(TemplateView):
    template_name = 'accounts/register-restaurant.html'
