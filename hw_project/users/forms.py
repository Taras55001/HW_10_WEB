from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Author, Quote
from quotes.models import Tag


class RegistrationForm(UserCreationForm):
    pass


class LoginForm(AuthenticationForm):
    pass


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            'born_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class PostForm(forms.Form):
    quote = forms.CharField()
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple()
                                          )
    #
    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     sorted_tags_choices = sorted([(tag.name, tag.name) for tag in Tag.objects.all()], key=lambda x: x[1])
    #     self.fields['tags'].choices = sorted_tags_choices
