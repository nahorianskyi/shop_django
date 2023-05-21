from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index),
    path('product_list', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    path('about_us', views.about_us, name='about_us'),
    path('questions_answer', views.questions_answer, name='questions_answer'),
    path('contact', views.contact, name='contact'),
    path('review', views.review, name='review'),
]