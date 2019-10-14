
from django.urls import path, include
from . import views
app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail,name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/comment_create/', views.comment_create,name='comment_create'),
    path('<int:pk>/comment_delete/', views.comment_delete,name='comment_delete'),
]