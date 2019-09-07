'''from  django.http import HttpResponse
from django.http import Http404
from .models import Album,Song
from django.shortcuts import render,get_object_or_404 

def index(request):
    all_albums=Album.objects.all()
    context={
        'all_albums':all_albums,
    }
    return render(request,'music/index.html',context)
def detail(request,album_id): 

    #try:
    #    album =Album.objects.get(id=album_id)
    #except Album.DoesNotExist:
    #    raise Http404("Album is not available")
    
    album = get_object_or_404(Album , id=album_id)
    return render(request,'music/detail.html',{'album':album})
only when you want to use functions 
'''
from django.views import generic
from .models import Album,Song
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse_lazy ,reverse
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import UserForm,songform,LoginForm
from django.contrib.auth.forms import AuthenticationForm
import subprocess,os
def signup(request):
    return render(request,'music/signup.html')
class IndexView(generic.ListView):
    template_name='music/index.html'
    context_object_name="all_albums"#is used to overwrite the object_list (that displays all the objects)  
    
    
    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model=Album
    template_name='music/detail.html'

        
class AlbumCreate(CreateView):
    model= Album
    fields=['artist','album_title','genre','album_logo']


def SongCreate(request,album_id):
    form_class =songform
    template_name ='music/song_form.html'
    if request.method=="GET":
        form =form_class(None)
        return render(request,template_name,{"form": form})
    if request.method =="POST":
        form = form_class(request.POST)
        if form.is_valid():
            song=form.save(commit=False)
            song_title=form.cleaned_data['song_title']
            file_type=form.cleaned_data['file_type']
            song.album=Album.objects.get(id=album_id)
            song.save()
            #r=subprocess.call(['bash','/home/ayush/test.sh'])This was just a test to execute subprocess
            #t=subprocess.call([ 'mv','/home/ayush/Documents/django/testsite/fuckit.txt','/home/ayush'])
            return redirect('music:detail' ,album_id)#reverse can also be used 
            
class AlbumUpdate(UpdateView):
    model= Album
    fields=['artist','album_title','genre','album_logo']
    template_name_suffix = '_update_form'#cause default is _form suffix (album_form)

class AlbumDelete(DeleteView):
    model=Album
    success_url = reverse_lazy('music:index')


def deletealbum(request,album_id):
    Album.objects.filter(id=album_id).delete()
    return redirect('music:index')
#def addsong(request,album_id)
def my_logout(request):
    logout(request)
    return redirect('music:register')
def my_login(request):
    template_name='music/login.html'
    if request.method=="POST":
        form1 = AuthenticationForm(data=request.POST)
        if form1.is_valid():
            username= form1.cleaned_data['username']
            password =form1.cleaned_data['password']
            a=authenticate(username=username,password=password )
            if a is not None:
                login(request,a)
                return redirect('music:index')
    else:
        form1=AuthenticationForm(None)
    
    return render(request,template_name,{"form":form1})
class UserFormView(View):
    form_class= UserForm
    template_name ='music/registration_form.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form': form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user  =form.save(commit=False)
            username= form.cleaned_data['username']
            password =form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password =password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('music:index')
            
        return render(request,self.template_name,{'form': form})
'''
This is based on function
def UserFormView(request):
    form_class= UserForm
    template_name ='music/registration_form.html'

    if request.method=='GET' :
        form = form_class(None)
        return render(request,template_name,{'form': form})

    if request.method == 'POST' :
        form = form_class(request.POST)

        if form.is_valid():
            user  =form.save(commit=False)
            username= form.cleaned_data['username']
            password =form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password =password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('music:index')
            
        return render(request,template_name,{'form': form})
'''