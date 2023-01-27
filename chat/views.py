
from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from .models import Chat, Message
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
""" from .forms import NewUserForm """
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic

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
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username = request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request,'auth/login.html', { 'wrongPassword': True, 'redirect': redirect})
    return render(request,'auth/login.html', { 'redirect': redirect })


    
    
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class signup_view(generic.CreateView):
    form_class = NewUserForm
    success_url = reverse_lazy("/login/?next=/chat/" )
    template_name = "auth/signup.html"
    
    

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("chat:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="auth/signup.html", context={"register_form":form})