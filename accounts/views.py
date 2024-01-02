from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView
from accounts.forms import RegisterClientForm
from accounts.models import User, UserProfile
from accounts.utils import detect_user
from vendor.forms import RestaurantForm


# Create your views here.
# class RegisterClientView(View):  # Inherit from the base View class
#     template_name = 'accounts/register-client.html'
#
#     def get(self, request, *args, **kwargs):
#         form = RegisterClientForm()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = RegisterClientForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = User.objects.create_user
#             <-(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
#             user.role = User.CLIENT
#             user.save()
#             messages.success(request, "Successfully created a new user")
#             return redirect('register_client')
#         return render(request, self.template_name, {'form': form})
# class RegisterClientView(TemplateView):
#     template_name = 'accounts/register-client.html'
#
#     def get(self, request, *args, **kwargs):
#         form = RegisterClientForm()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = RegisterClientForm(request.POST)
#         if form.is_valid():
#             # Process the form data
#             # create user using form
#
#             # password = form.cleaned_data
#             # user = form.save(commit=False)
#             # user.set_password(password)
#             # user.role = User.CLIENT
#             # form.save()
#
#             # create a user using create_user method
#
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = User.objects.create_user
#             <-(first_name=first_name, last_name=last_name, username=username, email=email,
#                                             password=password)
#             user.role = User.CLIENT
#             user.save()
#             messages.success(request, "Successfully created a new user")
#             return redirect('register_client')
#         return render(request, self.template_name, {'form': form})
#
#
# class RegisterRestaurantView(TemplateView):
#     template_name = 'accounts/register-restaurant.html'
#
#     def get(self, request, *args, **kwargs):
#         client_form = RegisterClientForm
#         restaurant_form = RestaurantForm
#         return render(request, self.template_name, {'client_form': client_form, 'restaurant_form': restaurant_form})
#
#     def post(self, request, *args, **kwargs):
#         client_form = RegisterClientForm(request.POST)
#         restaurant_form = RestaurantForm(request.POST)
#         if client_form.is_valid():
#             # user = client_form.save(commit=False)
#             # user.set_password(client_form.cleaned_data['password'])
#             # user.role = User.RESTAURANT
#             # user.save()
#             #
#             # restaurant = restaurant_form.save(commit=False)
#             # # Assuming there's a foreign key field in RestaurantForm pointing to the User model
#             # restaurant.user = user
#             # restaurant.save()
#             first_name = client_form.cleaned_data['first_name']
#             last_name = client_form.cleaned_data['last_name']
#             username = client_form.cleaned_data['username']
#             email = client_form.cleaned_data['email']
#             password = client_form.cleaned_data['password']
#             # return HttpResponse(last_name)
#             user = User.objects.create_user
#             <-(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
#             user.role = User.RESTAURANT
#             user.save()
#             restaurant = restaurant_form.save()
#             restaurant.user = user
#             user_profile = user.objects.get(user=user)
#             restaurant.user_profile = user_profile
#         else:
#             return render
#             (request, self.template_name, {'client_form': client_form, 'restaurant_form': restaurant_form})
#
#         return render(request, self.template_name, {'client_form': client_form, 'restaurant_form': restaurant_form})
class RegisterClientView(CreateView):
    model = User
    form_class = RegisterClientForm
    template_name = 'accounts/register-client.html'
    success_url = reverse_lazy('register_client')
    3

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in.')
            return redirect('my_account')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = User.CLIENT
        user.save()
        messages.success(self.request, "Successfully created a new user")
        return super().form_valid(form)


def register_restaurant(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You already logged in. If you want a new account logout then register. ')
        return redirect('my_account')

    else:
        if request.method == 'POST':
            client_form = RegisterClientForm(request.POST)
            restaurant_form = RestaurantForm(request.POST, request.FILES)
            if client_form.is_valid() and restaurant_form.is_valid:
                first_name = client_form.cleaned_data['first_name']
                last_name = client_form.cleaned_data['last_name']
                username = client_form.cleaned_data['username']
                email = client_form.cleaned_data['email']
                password = client_form.cleaned_data['password']
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                email=email,
                                                password=password)
                user.role = User.RESTAURANT
                user.save()
                # we need to add user and userprofile to the restaurant
                restaurant = restaurant_form.save(commit=False)
                restaurant.user = user
                user_profile = UserProfile.objects.get(user=user)
                restaurant.user_profile = user_profile
                restaurant.save()
                messages.success(request, "Restaurant saved successfully")
                return redirect(reverse_lazy('register_restaurant'))

        else:
            client_form = RegisterClientForm()
            restaurant_form = RestaurantForm()
        context = {
            "client_form": client_form,
            "restaurant_form": restaurant_form
        }
        return render(request, 'accounts/register-restaurant.html', context)


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('my_account')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        # Redirect to the login page after logout
        return redirect(reverse_lazy('homepage'))


@login_required(login_url='login')
def my_account(request):
    user = request.user
    redirect_url = detect_user(user)
    return redirect(redirect_url)


@login_required(login_url='login')
def restaurant_dashboard(request):
    return render(request, 'restaurant_dashboard.html')


@login_required(login_url='login')
def client_dashboard(request):
    return render(request, 'client_dashboard.html')
