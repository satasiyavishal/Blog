from django.shortcuts import render, redirect

# Create your views here.

from .form import *
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/')

def home(request):
    context = {'blogs': BlogModel.objects.all()}
    return render(request, 'home.html',context)

def login_view(request):
    return render(request, 'login.html')    

def register_view(request):
    return render(request, 'register.html')   

def blog_detail(request , slug):
    try:
        blog_obj ={'blog_obj':BlogModel.objects.filter(slug=slug).first()}
    except Exception as e :
        print(e)
    return render(request, 'blog_detail.html',blog_obj)

def see_blog(request):
    try:
        blog_obj ={'blog_obj':BlogModel.objects.filter(user=request.user)}
    except Exception as e :
        print(e)    

    return render(request, 'see_blog.html',blog_obj)

def blog_update(request , slug):
    blog_obj={}
    try:
        blog_o=BlogModel.objects.get(slug=slug)
        if blog_o.user != request.user:
            return redirect('/')
        initial_dict = {'content': blog_o.content}
        form = BlogForm(initial = initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            image =request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']
            blog_o.title=title
            blog_o.content=content
            blog_o.image=image
            blog_o.save()
            # BlogModel.objects.create(
            #     user = user, title =title,
            #     content = content, image = image
            # )
        blog_obj['blog_obj'] =blog_o
        blog_obj['form'] = form
    except Exception as e :
        print(e)
    return render(request, 'update_blog.html',blog_obj)

def blog_delete(request , id):
    try:
        blog_obj = BlogModel.objects.get(id=id)
        if blog_obj.user == request.user:
            blog_obj.delete()
    except Exception as e :
        print(e)
    return redirect('/see-blog/')

def add_thing(request):
    context ={'form' : BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            image =request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            BlogModel.objects.create(
                user = user, title =title,
                content = content, image = image
            )
            return redirect('/addContent/')

    except Exception as e :
        print(e)


    return render(request, 'add_thing.html',context)    

def verify(request,token):
    try:
        profile_obj = Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
        return redirect('/login/')
    except Exception as e :
        print(e)
    return redirect('/')