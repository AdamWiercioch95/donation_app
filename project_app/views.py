from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import redirect
from django.views.generic import TemplateView

from project_app.models import Donation, Institution, TYPES


class LandingPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_bags'] = Donation.objects.all().aggregate(Sum('quantity'))['quantity__sum'] or 0
        context['institutions'] = Institution.objects.all()
        context['institution_types'] = TYPES

        return context


class AddDonationView(TemplateView):
    template_name = 'form.html'


class ConfirmDonationView(TemplateView):
    template_name = 'form-confirmation.html'


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
