
from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from .models import Chat, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django import forms
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import login


@login_required(login_url='/login/')
def index(request):
    """this is a view to render the chat

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        print("Received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json',[new_message])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})


def login_view(request):
    """ redirect = request.GET.get('next') """
    if request.method == 'POST':
        user = authenticate(username = request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            """ return HttpResponseRedirect(request.POST.get('redirect')) """
            return render(request,'chat/index.html')
        else:
            """ return render(request,'auth/login.html', { 'wrongPassword': True, 'redirect': redirect}) """
            return render(request,'auth/login.html', { 'wrongPassword': True})
    """ return render(request,'auth/login.html', { 'redirect': redirect }) """
    return render(request,'auth/login.html')

def home(request):
    return render(request, 'chat/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')    
            """ return redirect('login') """
            return render(request, 'chat/index.html')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'auth/signup.html', context)


def logout_view(request):
    logout(request)
    return render(request, 'auth/logout.html')   
    


