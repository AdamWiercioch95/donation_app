from django.db.models import Sum
from django.views.generic import TemplateView

from project_app.models import Donation, Institution, TYPES


class LandingPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_bags'] = Donation.objects.all().aggregate(Sum('quantity'))['quantity__sum'] or 0
        context['institutions'] = Institution.objects.all()
        context['institution_types'] = TYPES

        context['institution_descriptions'] = {
            1: "W naszej bazie znajdziesz listę zweryfikowanych Fundacji, z którymi współpracujemy. Możesz sprawdzić czym się zajmują, komu pomagają i czego potrzebują.",
            2: "W naszej bazie znajdziesz listę zweryfikowanych Organizacji Pozarządowych, z którymi współpracujemy. Możesz sprawdzić czym się zajmują, komu pomagają i czego potrzebują.",
            3: "W naszej bazie znajdziesz listę zweryfikowanych Lokalnych Zbiórek, z którymi współpracujemy. Możesz sprawdzić czym się zajmują, komu pomagają i czego potrzebują.",
        }
        return context


class AddDonationView(TemplateView):
    template_name = 'form.html'


class ConfirmDonationView(TemplateView):
    template_name = 'form-confirmation.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'
