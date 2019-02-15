from django import forms
from django.contrib.auth import authenticate, get_user_model 

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    '''
    Clean method activates when
    form is submited and cleans data
    '''
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password) 
            if not user:
                raise forms.ValidationError('This user does not exits')
            if not user.check_password:
                raise forms.ValidationError('Wrong password')
            if not user.is_active:
                raise forms.ValidationError('User is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)
    

class UserRegisterFrom(forms.ModelForm):
    email = forms.EmailField(label='Email adress')
    email2 = forms.EmailField(label='Comfirm adress')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError('emails must match')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email is alredy in use')
        return super(UserRegisterFrom, self).clean(*args, *kwargs)