from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label="Usuário", max_length=100)
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['senha'].widget.attrs.update({'autofocus': ''})
