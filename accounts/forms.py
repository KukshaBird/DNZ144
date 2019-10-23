# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import ApiUser
from django import forms

from django.core.mail import send_mail

class UserCreateForm(UserCreationForm):
    #Add request for access to KID
    kid_request = forms.CharField(max_length=30, min_length=2, required=True)

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "password1", "password2")
        model = ApiUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Имя которое будет отображаться на сайте"
        self.fields["email"].label = "Электронная почта"
        self.fields["kid_request"].label = "Фамилия ребенка"

    def send_request(self):
        send_mail(
            'Запрос на регистрацию',
            self.cleaned_data["kid_request"] + " от " + self.cleaned_data["username"],
            'subslavyan01@gmail.com',
            ['samoilovartem1989@gmail.com'],
            fail_silently=False,
        )



class UserLoginForm(AuthenticationForm):
    model = ApiUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Имя которое будет отображаться на сайте"
