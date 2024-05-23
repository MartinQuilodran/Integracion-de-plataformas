from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label=_('Correo electrónico'))
    password2 = forms.CharField(
        label=_('Confirmar Contraseña'),
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': _('Nombre de usuario'),
            'password': _('Contraseña'),  # <-- Aquí cambiamos el label de 'password'
        }

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError(_("Las contraseñas no coinciden."))

        return password2
