from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages


def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        # missing bcrypt 
        # first hash password
        # then use the hashed password to store in db
        one_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
            
            #password= hashed_pw
        )
       
        request.session['user_id'] = one_user.id
        # request.session['greeting'] = one_user.first_name
        print("We made it")
        print(one_user.password)
    return redirect('/home')

def login(request):   
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        print("Yes!")
        one_user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = one_user.id
        #request.session['greeting'] = one_user.first_name
        return redirect('/home')

def home(request):
    print(request.session['user_id'])
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'all_post': Post.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id']),
        }
        return render(request, "home.html", context)

def logout(request):
    #missing this line.
    # we want to clear request.session every time someone logs out
    request.session.flush()
    return redirect('/')

def edit(request):
    errors = Post.objects.simple_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/home')
    else:
        one_user = User.objects.get(id=request.session["user_id"])
        post = Post.objects.create(
        status = request.POST['status'],   
        posted_by  = one_user
        )
    return redirect('/home')

def delete(request, post_id):
    status = Post.objects.get(id=post_id)
    
    status.delete()

    return redirect('/home')

def like(request, post_id):
    user = User.objects.get(id=request.session["user_id"])
    post = Post.objects.get(id=post_id)
    if user not in post.liked.all():
        post.liked.add(user)
    else:
        post.liked.remove(user)
    print(user.liked_posts.all())
    return redirect('/home')

def status(request, post_id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'post': Post.objects.get(id=post_id),
            'this_user': User.objects.get(id=request.session["user_id"]),
        }
    return render(request, 'like_status.html', context)

def profile(request, this_user_id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'all_posts': Post.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id']),
        }
    return render(request, 'profile.html', context)
