from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import NewsForm
from .models import Category, News, Customer, Employee, Order, Commit

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CustomerSerializer, EmployeeSerializer, OrderSerializer, CommitSerializer
from rest_framework.permissions import IsAuthenticated




def category(request, pk):
    news = News.objects.filter(category=pk)
    category = Category.objects.all()
    context = {
        "news": news,
        "category": category,
        "title": "NEWS TITLE",
    }
    return render(request, 'category.html', context=context)


def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NewsForm()
    return render(request, 'add_news.html', {'form': form})


def detail_new(request, pk):
    new = get_object_or_404(News, id=pk)
    context = {"new": new}
    return render(request, 'detail_new.html', context=context)


def update_new(request, pk):
    new = get_object_or_404(News, id=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=new)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NewsForm(instance=new)
    return render(request, 'update_new.html', {'form': form, 'new': new})


def del_new(request, pk):
    new = get_object_or_404(News, id=pk)
    new.delete()
    news = News.objects.all()
    category = Category.objects.all()
    context = {
        "news": news,
        "category": category,
        "title": "NEWS TITLE",
    }
    return render(request, 'index.html', context=context)


class HomeNews(ListView):
    model = News
    template_name = 'index.html'
    context_object_name = 'news'
    extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'NEWS TITLE'
        context['category'] = Category.objects.all()
        return context

    def get_queryset(self):
        # field name in model is "bool"
        return News.objects.filter(bool=True)


class NewsByCategory(ListView):
    model = News
    template_name = 'index.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context

    def get_queryset(self):
        return News.objects.filter(category=self.kwargs['pk'])


class ViewNews(DetailView):
    model = News
    context_object_name = 'news'
    template_name = 'index.html'
    pk_url_kwarg = 'pk'


class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'add_news.html'
    success_url = reverse_lazy('home')


class NewsUpdate(UpdateView):
    form_class = NewsForm
    template_name = "update_new.html"
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'pk'


def index(request):
    return render(request, 'index.html')


class CustomerListCreateApi(APIView):

    def get(self, request):
        customers = Customer.objects.all()
        from .serializers import CustomerSerializer
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        from .serializers import CustomerSerializer
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomerDetailApi(APIView):

    def get(self, request, id):
        customer = get_object_or_404(Customer, id=id)
        from .serializers import CustomerSerializer
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, id):
        customer = get_object_or_404(Customer, id=id)
        from .serializers import CustomerSerializer
        serializer = CustomerSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        customer = get_object_or_404(Customer, id=id)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeListCreateApi(APIView):

    def get(self, request):
        employees = Employee.objects.all()
        from .serializers import EmployeeSerializer
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        from .serializers import EmployeeSerializer
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmployeeDetailApi(APIView):

    def get(self, request, id):
        employee = get_object_or_404(Employee, id=id)
        from .serializers import EmployeeSerializer
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, id):
        employee = get_object_or_404(Employee, id=id)
        from .serializers import EmployeeSerializer
        serializer = EmployeeSerializer(employee, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        employee = get_object_or_404(Employee, id=id)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListCreateApi(APIView):

    def get(self, request):
        orders = Order.objects.all()
        from .serializers import OrderSerializer
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        from .serializers import OrderSerializer
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailApi(APIView):

    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        from .serializers import OrderSerializer
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, id):
        order = get_object_or_404(Order, id=id)
        from .serializers import OrderSerializer
        serializer = OrderSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        order = get_object_or_404(Order, id=id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommitApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        commits = Commit.objects.filter(author=request.user)
        serializer = CommitSerializer(commits, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
