from django.shortcuts import render
from message.models import Conversation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decoratos.csrf import csrf_exempt
from pusher_message.settings_config.keyconfig import *
from pusher import Pusher
from django.http import JsonResponse, HttpResponse

#Initialising Pusher Creds
pusher_client = Pusher(
    app_id = APP_ID,
    key = KEY,
    secret = SECRET,
    cluster = CLUSTER,
    ssl = True
)

@login_required(login_url='login/')
def index(request):
    return render(request, "chat.html")
