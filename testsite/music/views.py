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
from .models import Album
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy ,reverse
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import UserForm

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

class AlbumUpdate(UpdateView):
    model= Album
    fields=['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
    model=Album
    success_url = reverse_lazy('music:index')


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