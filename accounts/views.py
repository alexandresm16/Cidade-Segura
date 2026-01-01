# accounts/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import CreateView, View
from django.contrib.messages.views import SuccessMessageMixin

from occurrences.models import Occurrence
from .forms import UserRegisterForm
from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from .forms import UserLoginForm


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    success_message = 'Conta criada! Verifique seu e-mail para ativação.'

    def form_valid(self, form):
        # Salva o usuário primeiro
        response = super().form_valid(form)  # isso chama form.save() e dispara signals
        user = self.object  # usuário criado e salvo

        # Agora geramos token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        activation_link = self.request.build_absolute_uri(
            reverse_lazy('activate-account', kwargs={'uidb64': uid, 'token': token})
        )

        # Envia e-mail
        email = EmailMessage(
            subject='Ative sua conta',
            body=f'Clique no link para ativar sua conta:\n{activation_link}',
            to=[user.email],
        )
        email.send()

        return response


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'Link inválido.')
            return redirect('login')

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Conta ativada com sucesso!')
        else:
            messages.error(request, 'Token inválido ou expirado.')

        return redirect('login')


class UserLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = UserLoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy('home')


class UserLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Você saiu da sua conta com sucesso!")
        return redirect('home')  # redireciona para home


class OccurrenceListView(LoginRequiredMixin, ListView):
    model = Occurrence
    template_name = 'user.html'
    context_object_name = 'occurrences'

    def get_queryset(self):
        user = self.request.user
        return Occurrence.objects.filter(reporter=user).order_by('created_at')
