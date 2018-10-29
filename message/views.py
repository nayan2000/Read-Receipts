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

@csrf_exempt
def broadcast(request):
    try:
        data = request.POST
        message_text = data.get('message','')
        status = ''
        user = request.user
        instance = Conversation(message=message_text, status=status, user=user)
        instance.save()

        message = {
            'name': instance.user.username,
            'status': instance.status,
            'message': instance.message,
            'id': instance.id
        }

        pusher_client.trigger(u'a_channel', u'an_event', message)
        return JsonResponse(message, safe = False)

def conversations(request):
    data = Conversation.objects.all()
    context = [{'name':person.user.username, 'status': person.status, 'message':person.message, 'id':person.id} for person in data]
    return JsonResponse(context, safe = False)

def delivered(request, id):
    message = Conversation.objects.get(id = id)
    if request.user.id != message.user.id:
        socket_id = request.POST.get('socket_id', '')
        message.status =  'Delivered'
        message.save()

        message = {
            'name': message.user.username,
            'status': message.status,
            'message': message.message,
            'id': message.id
        }

        pusher.trigger(u'a_channel', u'delivered_message', message, socket_id )
        return HttpResponse('ok')

    else:
        return HttpResponse('Awaiting Delivery')