
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message, UserProfile
from chat.serializers import MessageSerializer, UserSerializer
from django.contrib import messages


def index(request):
    if request.user.is_authenticated: #If the user is authenticated then redirect to the chat console
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST": #Authentication of user
        username, password = request.POST['username'], request.POST['password'] #Retrieving username and password from the POST data.
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
        else:
            messages.error(request, 'Такого пользователя нет')
            return redirect('index')
        return redirect('chats')



# Decorator to make the view csrf excempt.
@csrf_exempt
def user_list(request, pk=None):

    # List all required user, or create a new user.

    if request.method == 'GET':
        if pk:                                     # If PrimaryKey (id) of the user is specified in the url
            users = User.objects.filter(id=pk)              # Select only that particular user
        else:
            users = User.objects.all()                             # Else get all user list
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)               # Return serialized data

    elif request.method == 'POST':
        data = JSONParser().parse(request)           # On POST, parse the request object to obtain the data in json
        try:
            user = User.objects.create_user(username=data['username'], password=data['password'])
            UserProfile.objects.create(user=user)
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Something went wrong"}, status=400)


@csrf_exempt
def message_list(request, sender=None, receiver=None):
        # List all required messages, or create a new message.
        if request.method == 'GET':
            messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
            serializer = MessageSerializer(messages, many=True, context={'request': request})
            for message in messages:
                message.is_read = True
                message.save()
            return JsonResponse(serializer.data, safe=False)

        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)


# Simply render the template
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'chat/register.html', {})

def chat_view(request):
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)}) #Returning context for all users except the current logged-in user

#Takes arguments 'sender' and 'receiver' to identify the message list to return
def message_view(request, sender, receiver):
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username), #List of users
                       'receiver': User.objects.get(id=receiver), # Receiver context user object for using in template
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)}) # Return context with message objects where users are either sender or receiver.