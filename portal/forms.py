from django import forms
from .models import Review
from django.contrib.auth.models import User
from .models import UserProfile, Comment


class OrderForm(forms.Form):
    quantity = forms.IntegerField(label='Количество',
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Введите количество'})
    )
    first_name = forms.CharField(label='Имя',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваше имя'})
    )
    last_name = forms.CharField(label='Фамилия',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Введите вашу фамилию'})
    )
    phone = forms.CharField(label='Телефон',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваш телефон'})
    )
    email = forms.EmailField(label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Введите ваш email'})
    )
    address = forms.CharField(label='Адрес',
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваш адрес'})
    )
    delivery_date = forms.DateField(label='Дата доставки',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    delivery_time = forms.TimeField(label='Время доставки',
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    wishes = forms.CharField(label='Пожелания', required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Напишите ваши пожелания'})
    )
    option = forms.ChoiceField(label='Способ получения',
        choices=[
            ('При получении', 'При получении'),
            ('Оплата онлайн', 'Оплата онлайн')
        ],
        widget=forms.RadioSelect, required=True
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'phone', 'email', 'comment_text']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ваш телефон'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email'}),
            'comment_text': forms.Textarea(attrs={'placeholder': 'Ваш комментарий'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={
                'placeholder': 'Ваш отзыв',
                'rows': 4,
                'cols': 50
            }),
        }

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        min_length=4,
        label='Логин',
        widget=forms.TextInput(attrs={'placeholder': 'Логин'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(
        min_length=4,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )
    password_confirm = forms.CharField(
        min_length=4,
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля'})
    )
    first_name = forms.CharField(
        max_length=20,
        label='Имя',
        widget=forms.TextInput(attrs={'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        max_length=20,
        label='Фамилия',
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия'})
    )
    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        widget=forms.TextInput(attrs={'placeholder': 'Телефон'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone']
            )
        return user


class LoginForm(forms.Form):
     username = forms.CharField(
         label='Логин',
         widget=forms.TextInput(attrs={
         'placeholder': 'Логин'
     }))
     password = forms.CharField(
         label='Пароль',
         widget=forms.PasswordInput(attrs={
     'placeholder': 'Пароль'
     }))


