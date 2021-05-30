from django.conf.urls import url
from django.contrib import admin
from django.urls import path , include
from . import views


urlpatterns = [
    url(r'^$', views.Home, name='home'),
    url(r'^friendship/', include('friendship.urls')),
    url(r'^home-landing/$', views.Home_Landing, name='home-landing'),  
    url(r'^register/$', views.Register, name='register'),  
    url(r'^logout/$', views.Logout, name='logout'),  
    url(r'^search_product/$', views.Search, name='search_product'),  
    url(r'^wallet/$', views.Wallet, name='wallet'),  
    url(r'^select_account/(?P<temp>[\w-]+)/$', views.Select_Account, name='select_account'),  
    url(r'^transactions/(?P<id>\d+)/(?P<temp>[\w-]+)/(?P<request_id>\d+)/(?P<request_money>\d+\.\d+)/$' ,views.Transactions , name="transactions"),
    url(r'^add_fav/(?P<website>[\w-]+)/$' ,views.Add_Fav , name="add_fav"),
    url(r'^view_fav/(?P<temp>[\w-]+)/$' ,views.View_Fav , name="view_fav"),
    url(r'^remove_fav/(?P<id>\d+)/$' ,views.Remove_Fav , name="remove_fav"),
    url(r'^view_requests/$' ,views.View_Requests , name="view_requests"),
    url(r'^delete_request/(?P<id>\d+)/(?P<temp>\d+)/$' ,views.Delete_Request , name="delete_request"),
    url(r'^error_page/$' ,views.Error_Page , name="error_page"),
    url(r'^friends_list/$' ,views.Friends_List , name="friends_list"),
    url(r'^add_friends/$' ,views.Add_Friends , name="add_friends"),
    url(r'^view_frequests/$' ,views.View_Frequests , name="view_frequests"),
    url(r'^a_or_r/(?P<temp>[\w-]+)/(?P<from1>[\w-]+)/$' ,views.A_Or_R , name="a_or_r"),

]