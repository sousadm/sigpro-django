from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário", max_length=100)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': ''})
