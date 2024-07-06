import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib import messages

# Models
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

# Forms
from .forms import UserForm, ProfileForm, ProfilePictureForm, EditUserForm, EditProfileForm, EditProfilePictureForm

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        print(request.user.profile.picture.image.url)
    return render(request, "dndlite/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = authenticate(request, username=username, password=password)
        except:
            return render(
                request,
                "dndlite/login.html",
                {
                    "message": "Viajero, parece que has ingresado mal tu nombre o contraseña."
                },
            )
        if user is not None:
            login(request, user)
            messages.success(request, "Bienvenido de nuevo, viajero.")
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "dndlite/login.html",
                {
                    "message": "Viajero, parece que has ingresado mal tu nombre o contraseña."
                },
            )
    return render(request, "dndlite/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Hasta la próxima, viajero.")
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method != "POST":
        userForm = UserForm()
        profileForm = ProfileForm()
        pictureForm = ProfilePictureForm()
        return render(
            request,
            "dndlite/register.html",
            {
                "userForm": userForm,
                "profileForm": profileForm,
                "pictureForm": pictureForm,
            },
        )
    else:
        userForm = UserForm(request.POST)
        profileForm = ProfileForm(request.POST)
        pictureForm = ProfilePictureForm(request.POST, request.FILES)
        if not userForm.is_valid():
            return render(
                request,
                "dndlite/register.html",
                {
                    "userForm": userForm,
                    "profileForm": profileForm,
                    "pictureForm": pictureForm,
                    "message": "Formulario de usuario inválido.",
                },
            )
        if not profileForm.is_valid():
            return render(
                request,
                "dndlite/register.html",
                {
                    "userForm": userForm,
                    "profileForm": profileForm,
                    "pictureForm": pictureForm,
                    "message": "Formulario de perfil inválido.",
                },
            )
        if not pictureForm.is_valid():
            return render(
                request,
                "dndlite/register.html",
                {
                    "userForm": userForm,
                    "profileForm": profileForm,
                    "pictureForm": pictureForm,
                    "message": "Formulario de imagen inválido.",
                },
            )
        try:
            # Creating user variables
            username = userForm.cleaned_data["username"]
            email = userForm.cleaned_data["email"]
            password = userForm.cleaned_data["password"]
            password2 = userForm.cleaned_data["password2"]
            if password != password2:
                return render(
                    request,
                    "dndlite/register.html",
                    {
                        "userForm": userForm,
                        "profileForm": profileForm,
                        "pictureForm": pictureForm,
                        "message": "Viajero, asegurate de colorcar la misma contraseña",
                    },
                )
            first_name = userForm.cleaned_data["first_name"]
            last_name = userForm.cleaned_data["last_name"]
            # Creating profile variables
            bio = profileForm.cleaned_data["bio"]
            pronouns = profileForm.cleaned_data["pronouns"]
            birthdate = profileForm.cleaned_data["birthdate"]
            # Creating picture variables
            image = pictureForm.cleaned_data["image"]
            # Creating user
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            # Creating profile
            profile = Profile(
                user=user, bio=bio, pronouns=pronouns, birthdate=birthdate
            )
            profile.save()
            # Creating picture
            picture = ProfilePicture(profile_id=profile.id, image=image)
            picture.save()
            # Logging in user
            login(request, user)
            messages.success(request, "Usuario creado exitosamente")
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            return render(
                request,
                "dndlite/register.html",
                {
                    "userForm": userForm,
                    "profileForm": profileForm,
                    "pictureForm": pictureForm,
                    "message": "Ese nombre ya ha sido tomado, viajero.",
                },
            )
        except Exception as e:
            print(e)
            return render(
                request,
                "dndlite/register.html",
                {
                    "userForm": userForm,
                    "profileForm": profileForm,
                    "pictureForm": pictureForm,
                    "message": f"Error: {e}",
                },
            )

def profile(request, user_id=None):
    if request.method != "POST":
        if user_id is not None:
            user = User.objects.get(id=user_id)
        else:
            user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user_id=user)
        picture = ProfilePicture.objects.get(profile_id=profile.id)
        userForm = EditUserForm(instance=user)
        profileForm = EditProfileForm(instance=profile)
        pictureForm = EditProfilePictureForm(instance=picture)
        for pronoun in profile.PRONOUNS_CHOICES:
            if pronoun[0] == profile.pronouns:
                user_pronoun = pronoun[1]
        return render(
            request,
            "dndlite/profile.html",
            {
                "userForm": userForm,
                "profileForm": profileForm,
                "pictureForm": pictureForm,
                "user": user,
                "profile": profile,
                "picture": picture,
                "user_pronoun": user_pronoun,
            },
        )
    
def change_picture(request):
    if request.method == "POST":
        form = ProfilePictureForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, "Error: formulario inválido.")
            return HttpResponseRedirect(reverse("profile"))
        try:
            picture = ProfilePicture.objects.get(profile_id=request.user.profile.id)
            picture.image = form.cleaned_data["image"]
            picture.save()
            messages.success(request, "Has cambiado tu imagen exitosamente.")
            return HttpResponseRedirect(reverse("profile"))
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return JsonResponse({"error": f"Error: {e}"})
    messages.error(request, "Error: método no permitido.")
    return HttpResponseRedirect(reverse("profile"))

def change_profile(request):
    if request.method == "PUT":
        return JsonResponse({"error": "PUT request required"})
    data = json.loads(request.body)
    name = data["name"]
    last_name = data["lastname"]
    user = User.objects.get(id=request.user.id)
    try:
        user.first_name = name
        user.last_name = last_name
        user.save()
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return JsonResponse({"error": f"Error: {e}"})
    bio = data["bio"]
    pronouns = data["pronouns"]
    birthdate = data["birthdate"]
    profile = Profile.objects.get(user_id=request.user.id)
    try:
        profile.bio = bio
        profile.pronouns = pronouns
        profile.birthdate = birthdate
        profile.save()
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return JsonResponse({"error": f"Error: {e}"})
    messages.success(request, "El perfil ha sido actualizado correctamente")
    return JsonResponse({"success": "El perfil ha sido actualizado correctamente"})
