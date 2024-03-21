from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password


@require_http_methods(["POST"])
def register(request):
    try:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role', 'client')  # Default role is 'client'

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create(username=username, password=make_password(password), email=email,
                                   first_name=first_name, last_name=last_name)
        UserProfile.objects.create(user=user, role=role)

        return JsonResponse({'message': 'User registered successfully'})
    except KeyError:
        return JsonResponse({'error': 'Missing username or password'}, status=400)


@require_http_methods(["POST"])
def create_admin_user(request):
    # Ensure this endpoint is secured and accessible only to superusers or through a secure method
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    if not username or not password:
        return JsonResponse({'error': 'Username and password are required.'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists.'}, status=400)

    user = User.objects.create_superuser(username=username, email=email,
                                         password=password, first_name=first_name, last_name=last_name)
    return JsonResponse({'message': f'Admin user {username} created successfully.'})


@require_http_methods(["POST"])
def user_login(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'})
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

@require_http_methods(["POST"])
def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})