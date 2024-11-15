from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import UserRegistrationForm, SongUploadForm, UserDetailUpdateForm
from .models import Song, User

# Helper function to check if the user is an admin
def is_admin(user):
    return user.is_staff

# User registration view
def register(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'register.html', {'form': form})

# Login view with redirection for admin users
def login_view(request):
    # Define default admin credentials
    DEFAULT_ADMIN_USERNAME = 'admin'
    DEFAULT_ADMIN_PASSWORD = '123456'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check for default admin credentials
        if username == DEFAULT_ADMIN_USERNAME and password == DEFAULT_ADMIN_PASSWORD:
            # Check if the default admin user exists; create if it doesn't
            user, created = User.objects.get_or_create(
                username=DEFAULT_ADMIN_USERNAME,
                defaults={'is_staff': True, 'is_superuser': True}
            )
            if created:
                # Set the password and save the user
                user.set_password(DEFAULT_ADMIN_PASSWORD)
                user.is_staff = True
                user.is_superuser = True
                user.save()

            # Authenticate the admin user
            user = authenticate(request, username=DEFAULT_ADMIN_USERNAME, password=DEFAULT_ADMIN_PASSWORD)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# Home page view for regular users
@login_required
def home(request):
    songs = Song.objects.all()
    artists = {song.artist: [] for song in songs}
    for song in songs:
        artists[song.artist].append(song)
    return render(request, 'home.html', {'songs': songs, 'artists': artists})

# Admin dashboard view with song upload functionality
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    form = SongUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        song = form.save(commit=False)
        song.uploaded_by = request.user
        song.save()
        return redirect('admin_dashboard')

    context = {
        'form': form,
        'songs': Song.objects.all(),
        'artists_count': Song.objects.values('artist').distinct().count(),
        'songs_count': Song.objects.count(),
        'users_count': User.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)

# View to edit an existing song
@login_required
@user_passes_test(is_admin)
def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    form = SongUploadForm(request.POST or None, request.FILES or None, instance=song)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'edit_song.html', {'form': form, 'song': song})

# View to delete an existing song
@login_required
@user_passes_test(is_admin)
def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == 'POST':
        song.delete()
        return redirect('admin_dashboard')
    return render(request, 'confirm_delete.html', {'song': song})

@login_required
def update_user_details(request):
    # Pass the request object to the form
    form = UserDetailUpdateForm(request.POST or None, instance=request.user, request=request)
    
    if form.is_valid():
        user = form.save()

        # Display success message
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('home')

    return render(request, 'update_user_details.html', {'form': form})



