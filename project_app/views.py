import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from project_app.models import Donation, Institution, TYPES, Category


class LandingPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_bags'] = Donation.objects.all().aggregate(Sum('quantity'))['quantity__sum'] or 0
        context['institutions'] = Institution.objects.all()
        context['institution_types'] = TYPES

        return context


class AddDonationView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        categories = Category.objects.all()
        organizations = Institution.objects.all()
        for organization in organizations:
            category_ids = list(organization.categories.values_list('id', flat=True))
            organization.category_ids_json = json.dumps(category_ids)

        context = {
            'categories': categories,
            'organizations': organizations,
        }

        return render(request, 'form.html', context)

    def post(self, request):
        quantity = request.POST.get('bags')
        categories = request.POST.getlist('categories')
        institution_id = request.POST.get('organization')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')

        if not all([quantity, institution_id, address, phone_number, city, zip_code, pick_up_date, pick_up_time]):
            return HttpResponseBadRequest("Missing required fields.")

        try:
            institution = Institution.objects.get(id=institution_id)
        except Institution.DoesNotExist:
            return HttpResponseBadRequest("Invalid organization.")

        donation = Donation(
            quantity=quantity,
            address=address,
            phone_number=phone_number,
            city=city,
            zip_code=zip_code,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=request.user,
            institution=institution
        )
        donation.save()
        donation.categories.set(categories)

        return redirect('confirm')


class ConfirmDonationView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            return redirect('register')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing_page')
        else:
            messages.error(request, 'Nieprawidłowe hasło.')
            return self.render_to_response(self.get_context_data())


class RegisterView(TemplateView):
    template_name = 'register.html'

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Podane hasła nie są takie same.')
            return self.render_to_response(self.get_context_data())

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Użytkownik o podanym adresie email już istnieje.')
            return self.render_to_response(self.get_context_data())

        User.objects.create_user(first_name=name, last_name=surname, email=email, password=password, username=email)

        return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile.html'


