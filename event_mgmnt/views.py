from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, EventForm
from .models import Event, Ticket

# Create your views here.

def home(request):

    # <h3>Or sign up using</h3>
    # <a href="{% url 'social:begin' 'google' %}">Google</a><br>
    # <a href="{% url 'social:begin' 'facebook' %}">Facebook</a>
    # Use this above code in register.html for social login options
    
    return render(request, 'home.html')

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = User._default_manager.get_by_natural_key(username)
        except User.DoesNotExist:
            return
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Retrieve the default authentication backend
            backend = EmailOrUsernameModelBackend()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user._wrapped if hasattr(request.user, '_wrapped') else request.user
            event.save()
            return redirect('dashboard')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    events = Event.objects.filter(organizer=user)
    return render(request, 'dashboard.html', {'events': events})

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    tickets = Ticket.objects.filter(event=event)
    return render(request, 'event_details.html', {'event': event, 'tickets': tickets})

def purchase_ticket(request, event_id, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    # Implement payment gateway integration here
    
    return redirect('event_details', event_id=event_id)
