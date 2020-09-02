from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('email/create/', views.EmailCreate.as_view(), name='email_create'),
    path('email/update/<int:pk>', views.email_update, name='email_update'),
    path('category/create/', views.CategoryCreate.as_view(), name='category_create'),
    path('category/update/<int:pk>', views.CategoryUpdate.as_view(), name='category_update'),
    path('all/', views.EmailListView.as_view(), name='all_emails'),
    path('allcategories/', views.CategoryList.as_view(), name='all_categories'),
    path('email/<int:pk>', views.EmailDetailView.as_view(), name='email_detail'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category_detail'),
]