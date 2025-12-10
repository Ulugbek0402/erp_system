from django.urls import path
from .views import (
    HomeNews, NewsByCategory, ViewNews, CreateNews, NewsUpdate,
    category, add_news, detail_new, update_new, del_new,

    CustomerListCreateApi, CustomerDetailApi,
    EmployeeListCreateApi, EmployeeDetailApi,
    OrderListCreateApi, OrderDetailApi,
    CommitApi
)

urlpatterns = [

    path('', HomeNews.as_view(), name='home'),
    path('category/<int:pk>/', category, name='category'),
    path('news/<int:pk>/', detail_new, name='news_detail'),
    path('news/add/', add_news, name='add_news'),
    path('news/update/<int:pk>/', update_new, name='update_news'),
    path('news/delete/<int:pk>/', del_new, name='delete_news'),

    path('api/customers/', CustomerListCreateApi.as_view(), name='customers'),
    path('api/customers/<int:id>/', CustomerDetailApi.as_view(), name='customer_detail'),


    path('api/employees/', EmployeeListCreateApi.as_view(), name='employees'),
    path('api/employees/<int:id>/', EmployeeDetailApi.as_view(), name='employee_detail'),


    path('api/orders/', OrderListCreateApi.as_view(), name='orders'),
    path('api/orders/<int:id>/', OrderDetailApi.as_view(), name='order_detail'),


    path('api/commits/', CommitApi.as_view(), name='commits'),
]
