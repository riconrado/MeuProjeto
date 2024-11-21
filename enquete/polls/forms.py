from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class CadastraUsuarios(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'password1', 'password2']
        labels = {'username':'Login','first_name':'Nome','last_name':'Sobrenome'}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()

        self.helper.layout = Layout(
                Field('first_name', css_class='m-3 w-75'),
                Field('last_name', css_class='m-3 w-75'),
                Field('username', css_class='m-3 w-75'),
                Field('password1', css_class='m-3 w-75'),
                Field('password2', css_class='m-3 w-75'),
            )
        
        self.helper.add_input(Submit('submit', 'Cadastrar', css_class='btn-primary'))

class AlteraUsuarios(forms.ModelForm):

    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['email','first_name','last_name', 'is_active']
        labels = {'first_name':'Nome','last_name':'Sobrenome'}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()

        self.helper.layout = Layout(
                Field('first_name', css_class='m-3 w-75'),
                Field('last_name', css_class='m-3 w-75'),
                Field('email', css_class='m-3 w-75'),
                Field('is_active'),
            )
        
        self.helper.add_input(Submit('submit', 'Atualizar', css_class='btn-primary'))