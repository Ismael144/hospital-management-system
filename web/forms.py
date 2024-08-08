from django import forms
from .models import Message
from .models import Doctor, Patient
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Nurse, Receptionist, Appointment, Treatment, Bill, CustomUser, Payment, Inventory 
from django.utils import timezone
from django.contrib.auth import get_user_model

customUser = get_user_model()

