from django import forms
from .models import (
    User,
    Profile,
    ProfilePicture,
    Character,
    CharacterPicture,
    CharacterStats,
    CharacterInfo,
    Campaign,
    CampaignPicture,
    CampaignMap,
    Movements,
    Action,
    Reaction,
    CampaignLog,
)


class UserForm(forms.ModelForm):
    username = forms.CharField(
        label="Ingresa el nombre de usuario:",
        required=True,
        widget=forms.TextInput(
            attrs={
                "required": "true",
                "class": "form-control my-2",
                "placeholder": "Ingrese el nombre de usuario",
            }
        ),
    )
    email = forms.CharField(
        label="Ingresa tu correo electrónico:",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "required": "true",
                "type": "email",
                " class": "form-control my-2",
                "placeholder": "Ingrese tu correo electrónico",
            }
        ),
    )
    password = forms.CharField(
        label="Ingresa tu contraseña:",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "required": "true",
                "minlenght": "8",
                "type": "password",
                "class": "form-control my-2",
                "pattern": "(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
                "placeholder": "Confirme la contraseña",
            },
        ),
    )
    password2 = forms.CharField(
        label="Confirma tu contraseña:",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "required": "true",
                "minlenght": "8",
                "type": "password",
                "class": "form-control my-2",
                "pattern": "(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
                "placeholder": "Confirme la contraseña",
            }
        ),
    )
    first_name = forms.CharField(
        label="Ingresa tu nombre:",
        required=True,
        widget=forms.TextInput(
            attrs={
                "required": "true",
                "class": "form-control my-2",
                "placeholder": "Ingrese su nombre",
            }
        ),
    )
    last_name = forms.CharField(
        label="Ingresa tu apellido:",
        required=True,
        widget=forms.TextInput(
            attrs={
                "required": "true",
                "class": "form-control my-2",
                "placeholder": "Ingrese su apellido",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        label="Escribe una biografía (Opcional):",
        widget=forms.Textarea(
            attrs={
                "class": "bio-form form-control my-2",
                "placeholder": "Ingrese una biografía",
            }
        ),
    )
    birthdate = forms.DateTimeField(
        required=True,
        label="Escoge tu fecha de nacimiento:",
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(
            attrs={
                "class": "form-control datetimepicker-input",
                "data-target": "#datetimepicker1",
            }
        ),
    )
    pronouns = forms.ChoiceField(
        choices=Profile.PRONOUNS_CHOICES,
        required=False,
        label="Escoge tus pronombres (Opcional):",
        initial=Profile.PRONOUNS_CHOICES[5],
        widget=forms.Select(attrs={"class": "form-control my-2"}),
    )

    class Meta:
        model = Profile
        fields = ["bio", "pronouns", "birthdate"]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields["bio"].required = False


class ProfilePictureForm(forms.ModelForm):
    image = forms.ImageField(
        label="Escoger una foto de perfil (Opcional):",
        widget=forms.FileInput(attrs={"class": "form-control my-2"}),
    )

    class Meta:
        model = ProfilePicture
        fields = ["image"]


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Ingresa tu nombre:",
        required=True,
        widget=forms.TextInput(
            attrs={
                "required": "true",
                "class": "form-control my-2",
                "placeholder": "Ingrese su nombre",
            }
        ),
    )
    last_name = forms.CharField(
        label="Ingresa tu apellido:",
        required=True,
        widget=forms.TextInput(
            attrs={
                "required": "true",
                "class": "form-control my-2",
                "placeholder": "Ingrese su apellido",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class EditProfileForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        label="Escribe una biografía (Opcional):",
        widget=forms.Textarea(
            attrs={
                "class": "bio-form form-control my-2",
                "placeholder": "Ingrese una biografía",
            }
        ),
    )
    pronouns = forms.ChoiceField(
        choices=Profile.PRONOUNS_CHOICES,
        required=False,
        label="Escoge tus pronombres (Opcional):",
        initial=Profile.PRONOUNS_CHOICES[5],
        widget=forms.Select(attrs={"class": "form-control my-2"}),
    )
    birthdate = forms.DateTimeField(
        required=True,
        label="Escoge tu fecha de nacimiento:",
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(
            attrs={
                "class": "form-control datetimepicker-input",
                "data-target": "#datetimepicker1",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ["bio", "pronouns", "birthdate"]

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["bio"].required = False


class EditProfilePictureForm(forms.ModelForm):
    image = forms.ImageField(required=False,
        label="Cambia tu foto de perfil:",
        widget=forms.FileInput(attrs={"class": "form-control my-2"}),
    )

    class Meta:
        model = ProfilePicture
        fields = ["image"]