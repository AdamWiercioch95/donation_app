from django.db.models import Sum
from django.views.generic import TemplateView

from project_app.models import Donation, Institution


class LandingPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_bags'] = Donation.objects.all().aggregate(Sum('quantity'))['quantity__sum'] or 0
        context['institutions'] = Institution.objects.count()
        return context


class AddDonationView(TemplateView):
    template_name = 'form.html'


class ConfirmDonationView(TemplateView):
    template_name = 'form-confirmation.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'
