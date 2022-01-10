from django.shortcuts import render
from learning_user_app.forms import UserForm, UserProfileForm

#new import for login and logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'my_stuff/index.html')

@login_required(login_url='/learning_user_app/user_login')
def special(request):
    return HttpResponse('You are logged in, Nice!')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered =  False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            print("is recived form ?????????????")
            user = user_form.save()
            print("the password will hashing///////////////")
            user.set_password(user.password)
            print("the password hashed @@@@@@@@@@@@@@@@@@@")
            user.save()
            print("password is saved +++++++++++++ ")

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
                print('image is upload!!!!!!!!!!!!!!!!')
            
            profile.save()
            print("profile saved#################")
            registered=True

        else:
            print("error !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(user_form.errors, profile_form.errors)
    else:
        user_form= UserForm()
        profile_form = UserProfileForm()
    return render(request, 'my_stuff/registration.html',
                            {'registered':registered,
                            'user_form':user_form,
                            'profile_form':profile_form})


def user_login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account Not ACTIVE")
        else:
            print("someone tried to login and failed!")
            print(f"Username: {username}, Password: {password}")

            return HttpResponse("Invallid login details supplied")

    else:
        return render(request, 'my_stuff/login.html', {})