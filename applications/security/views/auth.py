from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from applications.security.models import User as CustomUser

# ----------------- Cerrar Sesion -----------------
@login_required
def signout(request):
    logout(request)
    return redirect("security:signin")

# # ----------------- Iniciar Sesion -----------------
def signin(request):
    
    data = {"title": "Login",
            "title1": "Inicio de Sesión"}
    if request.method == "GET":
        # Obtener mensajes de éxito de la cola de mensajes
        success_messages = messages.get_messages(request)
        return render(request, "security/auth/signin.html", {
            "form": AuthenticationForm(),
            "success_messages": success_messages,  # Pasar mensajes de éxito a la plantilla
            **data
        })
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return render(request, "security/auth/signin.html", {
                    "form": form,
                    "error": "El usuario o la contraseña son incorrectos",
                    **data
                })
        else:
            return render(request, "security/auth/signin.html", {
                "form": form,
                 "error": "Datos invalidos",
                **data
            })

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 focus:outline-none',
            'placeholder': 'Ingrese su contraseña'
        })
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 focus:outline-none',
            'placeholder': 'Confirme su contraseña'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'dni', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 focus:outline-none',
                'placeholder': 'Nombre de usuario'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 focus:outline-none',
                'placeholder': 'Nombres'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 focus:outline-none',
                'placeholder': 'Apellidos'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 focus:outline-none',
                'placeholder': 'correo@ejemplo.com'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 focus:outline-none',
                'placeholder': 'Cédula o RUC'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 focus:outline-none',
                'placeholder': 'Número de teléfono'
            }),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# ----------------- Registro de Usuario -----------------
def signup(request):
    data = {"title": "Registro", "title1": "Crear Cuenta"}
    
    if request.method == "GET":
        return render(request, "security/auth/signup.html", {
            "form": CustomUserCreationForm(),
            **data
        })
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Crear o obtener el grupo "User" y asignarlo al usuario
            user_group, created = Group.objects.get_or_create(name='User')
            user.groups.add(user_group)
            
            if created:
                print(f"Grupo 'User' creado automáticamente")
            
            messages.success(request, f"Usuario {user.username} creado exitosamente y asignado al grupo User. Puede iniciar sesión.")
            return redirect("security:signin")
        else:
            return render(request, "security/auth/signup.html", {
                "form": form,
                "error": "Por favor corrija los errores en el formulario",
                **data
            })