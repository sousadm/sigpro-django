from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label="Usuário", max_length=100, initial='gerente')
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput(), initial='123456')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'autofocus': ''})
