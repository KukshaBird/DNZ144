# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import ApiUser
from django import forms
from django.conf import settings

from django.core.mail import send_mail

class UserCreateForm(UserCreationForm):
    #Add request for access to KID
    kid_request = forms.CharField(max_length=30, min_length=2, required=True)

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "phone", "password1", "password2")
        model = ApiUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Имя которое будет отображаться на сайте. Не должно содержать пробелов."
        self.fields["email"].label = "Электронная почта. Не обязательно для заполнения, но необходима для восстановления пароля."
        self.fields["kid_request"].label = "Фамилия ребенка к которому будет привязана учетная запись. Обязательна для заполнения."
        self.fields["phone"].label = "Номер телефона. Не обязательно для заполнения."

    # send mail to admin with the last name of the kid wich new user wants to be connected.
    def send_request(self):
        send_mail(
            'Запрос на регистрацию',
            self.cleaned_data["kid_request"] + " от " + self.cleaned_data["username"],
            settings.EMAIL_HOST_USER,
            ['samoilovartem1989@gmail.com'],
            fail_silently=False,
        )

class DateInput(forms.DateInput):
    input_type = 'date'

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = ApiUser
        fields = ['phone', 'email', 'birth_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget = DateInput()




class UserLoginForm(AuthenticationForm):
    model = ApiUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Имя которое будет отображаться на сайте"
