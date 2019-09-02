from django.conf.urls import url
from . import views
app_name='music'

urlpatterns = [

    url(r'^signup/$', views.signup,name='signup'),

    url(r'^$', views.IndexView.as_view(),name='index'),
    url(r'^register/$', views.UserFormView.as_view(),name='register'),
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),
    #music/album/add/
    url(r'album/add/$',views.AlbumCreate.as_view(),name='album-add'),
    url(r'(?P<album_id>[0-9]+)/addsong/$',views.SongCreate,name='song-add'),

    url(r'album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(),name='album-update'),

    url(r'album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name='album-delete'),
    url(r'album/(?P<album_id>[0-9]+)/deletealbum/$',views.deletealbum,name='deletealbum'),

    


]
