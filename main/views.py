from collections import defaultdict

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.db.models import F, Q, Count, Min
# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, FormView

from main.forms import RegisterForm, SellerProductForm, ProductSearchForm
from django.shortcuts import render

from .models import Product, SellerProduct, Brand, Smartphones, MarketProduct, Market, Cart, CartItem, Favorite
from .models import Category
from django.contrib.auth.models import Group, User
from .models import Model
from django.db.models import Q

from django.db.models import Q
from .models import Brand, Model

from django.db.models import Q
from .models import Model  # Подставьте здесь вашу модель
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import matplotlib.pyplot as plt



def index(request):
    # Получаем все объекты MarketProduct
    market_products = MarketProduct.objects.select_related('smartphone__model')

    # Получаем 4 случайных объекта
    random_products = random.sample(list(market_products), min(4, market_products.count()))

    return render(request, 'main/index.html', {'random_products': random_products})



@login_required
def profile_view(request):
    # Получаем текущего пользователя
    user = request.user

    # Получаем роль пользователя
    if user.groups.filter(name='seller').exists():
        role = 'Продавец'
        is_seller = True
    else:
        role = 'Покупатель'
        is_seller = False

    # Передаем роль в контекст
    context = {'user': user, 'role': role, 'is_seller': is_seller}

    return render(request, 'main/profile.html', context)

def sign_in(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("main/profile.html")

    else:
        # Return an 'invalid login' error message.
        print('error')

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('main:profile')

    def form_valid(self, form):
        user = form.save(commit=False)

        # Проверяем, активирован ли чекбокс "Я продавец"
        is_seller = self.request.POST.get('is_seller', False)
        if is_seller:
            # Если чекбокс активирован, добавляем пользователя в группу продавцов
            seller_group, _ = Group.objects.get_or_create(name='seller')
            user.save()  # Сначала сохраняем пользователя, чтобы получить идентификатор
            user.groups.add(seller_group)
        else:
            user.save()  # Сохраняем пользователя, если он не продавец

        login(self.request, user)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

def display_products(request):
    products = Product.objects.using('Products').all()
    return render(request, 'main/products.html', {'products': products})


def search_results(request):
    query = request.GET.get('search_query')
    results = None
    if query:
        query_parts = query.split()
        filters = Q()
        for part in query_parts:
            filters &= (Q(smartphone__model__name__icontains=part) | Q(smartphone__brand__name__icontains=part))
        # Фильтруем товары из таблицы MarketProduct
        results = MarketProduct.objects.filter(filters).select_related('smartphone__brand', 'smartphone__model')

        # Получаем категорию из модели смартфона
        category_id = results.first().smartphone.category_id if results.exists() else None

        # Получаем уникальные модели товаров
        unique_models = results.values('smartphone__model_id').annotate(model_count=Count('smartphone__model_id'))

        # Фильтруем только уникальные модели
        unique_model_ids = [model['smartphone__model_id'] for model in unique_models]
        unique_results = results.filter(smartphone__model_id__in=unique_model_ids)

        # Отображаем только один товар для каждой уникальной модели
        unique_results = unique_results.distinct('smartphone__model_id')

        # Вычисляем минимальную цену для каждой уникальной модели
        min_prices = []
        for result in unique_results:
            min_price = MarketProduct.objects.filter(smartphone__model_id=result.smartphone.model_id).aggregate(min_price=Min('price'))['min_price']
            min_prices.append(min_price)
        for idx, result in enumerate(unique_results):
            result.min_price = min_prices[idx]

        results = unique_results

    return render(request, 'main/search_results.html', {'results': results, 'query': query, 'category_id': category_id})



class DisplayProducts(View):
    def get(self, request):
        products = Product.objects.using('Products').all()
        return render(request, 'main/products.html', {'products': products})

class AutocompleteProducts(View):
    def get(self, request):
        query = request.GET.get('term', '')
        products = Product.objects.using('Products').all().filter(Q(product_name__icontains=query))[:20]

        # Обновим структуру данных
        results = [{'label': f"{product.product_name} - {product.price} тг.", 'value': f"{product.product_name} - {product.price} тг."} for product in products]

        return JsonResponse(results, safe=False)

class ProductDetailView(View):
    template_name = 'product_detail.html'

    def get(self, request, brand, model):
        # Получите объект продукта из базы данных по бренду и модели
        product = get_object_or_404(Product, brand=brand, model=model)
        return render(request, self.template_name, {'product': product})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    # Получаем уникальные модели смартфонов для данной категории
    unique_smartphones = Smartphones.objects.filter(category_id=category_id).values(
        'brand__name', 'model__name', 'model_id', 'img', 'color', 'size'
    ).distinct()

    # Словарь для отслеживания уже добавленных уникальных моделей
    unique_models_dict = {}

    # Собираем список уникальных моделей и их брендов
    brands_and_models = []
    for smartphone in unique_smartphones:
        brand_name = smartphone['brand__name']
        model_name = smartphone['model__name']
        brand_model_key = (brand_name, model_name)

        # Проверяем, была ли уже добавлена модель с таким брендом и именем
        if brand_model_key not in unique_models_dict:
            market_product = MarketProduct.objects.filter(smartphone__model_id=smartphone['model_id']).order_by('price').first()
            if market_product:
                brands_and_models.append((
                    brand_name, model_name, smartphone['model_id'],
                    smartphone['img'], smartphone['color'], smartphone['size'], market_product.price
                ))
                unique_models_dict[brand_model_key] = True

    # Получаем уникальные цвета смартфонов для данной категории
    unique_colors = Smartphones.objects.filter(category_id=category_id).values_list('color', flat=True).distinct()

    # Разбиваем список брендов и моделей на страницы по 24 товара на каждую страницу
    paginator = Paginator(brands_and_models, 24)
    page_number = request.GET.get('page')
    try:
        page_brands_and_models = paginator.page(page_number)
    except PageNotAnInteger:
        page_brands_and_models = paginator.page(1)
    except EmptyPage:
        page_brands_and_models = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'page_brands_and_models': page_brands_and_models,
        'unique_colors': unique_colors,
    }
    return render(request, 'main/category_detail.html', context)



def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'main/all_categories.html', {'categories': categories})


@login_required
def cart_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    context = {
        'cart_items': cart_items
    }
    return render(request, 'main/cart.html', context)

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(SellerProduct, id=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            cart_item.quantity += 1
        cart_item.save()

        return redirect('main:cart')
    return redirect('main:index')

def remove_from_cart(request, item_id):
    # Находим товар в корзине по его id
    cart_item = get_object_or_404(CartItem, id=item_id)
    # Удаляем товар из корзины
    cart_item.delete()
    # Перенаправляем пользователя обратно на страницу корзины
    return redirect('main:cart')


@login_required
def add_to_favorites(request):
    if request.method == "POST":
        model_id = request.POST.get('model_id')
        favorite, created = Favorite.objects.get_or_create(user=request.user, model_id=model_id)
        if created:
            favorite.save()
        return redirect('main:favorites')
    return redirect('main:index')

@login_required
def remove_from_favorites(request, favorite_id):
    if request.method == "POST":
        favorite = get_object_or_404(Favorite, id=favorite_id)
        favorite.delete()
        return redirect('main:favorites')
    return redirect('main:index')


@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('model')
    return render(request, 'main/favorites.html', {'favorites': favorites})


@login_required
def seller_panel(request):
    # Проверяем, является ли текущий пользователь продавцом
    if request.user.groups.filter(name='seller').exists():
        if request.method == 'POST':
            if 'delete_product' in request.POST:
                product_id = request.POST.get('product_id')
                product = get_object_or_404(SellerProduct, id=product_id, seller=request.user)
                product.delete()
                return redirect('main:seller_panel')
            elif 'update_product' in request.POST:
                product_id = request.POST.get('product_id')
                product = get_object_or_404(SellerProduct, id=product_id, seller=request.user)
                price = request.POST.get('price')
                quantity = request.POST.get('quantity')
                if price and quantity:
                    product.price = price
                    product.quantity = quantity
                    product.save()
                return redirect('main:seller_panel')
            else:
                form = SellerProductForm(request.POST)
                if form.is_valid():
                    category = form.cleaned_data['category']
                    brand = form.cleaned_data['brand']
                    model = form.cleaned_data['model']
                    color = form.cleaned_data['color']
                    storage = form.cleaned_data['storage']
                    price = form.cleaned_data['price']
                    quantity = form.cleaned_data['quantity']
                    description = form.cleaned_data['description']
                    # Создание записи в таблице seller_products
                    seller_product = SellerProduct.objects.create(
                        seller_id=request.user.id,
                        category=category,
                        brand=brand,
                        model=model,
                        color=color,
                        storage=storage,
                        price=price,
                        quantity=quantity,
                        description=description
                    )
                    # После успешного создания продукта перенаправляем пользователя на страницу успешного создания или еще куда-нибудь
                    return redirect('main:seller_panel')
        else:
            form = SellerProductForm()

        # Извлечение данных продавца
        seller_products = SellerProduct.objects.filter(seller_id=request.user.id)

        # Если пользователь - продавец, отображаем страницу продавца
        return render(request, 'main/seller_panel.html', {'form': form, 'seller_products': seller_products})
    else:
        # Если пользователь не является продавцом, можем отобразить страницу с ошибкой или перенаправить его
        return redirect('main:index')




def product_detail(request, category_id, model_id):
    category = get_object_or_404(Category, id=category_id)
    model = get_object_or_404(Model, pk=model_id)

    # Фильтруем товары по переданному model_id
    market_products = MarketProduct.objects.filter(smartphone__model_id=model_id)

    # Определение минимальной цены
    min_price = market_products.aggregate(min_price=Min('price'))['min_price']

    # Получаем информацию о модели товара
    model = get_object_or_404(Model, id=model_id)

    # Получаем товары от продавцов для данной модели
    seller_products = SellerProduct.objects.filter(model=model)

    context = {
        'category': category,
        'model': model,
        'market_products': market_products,
        'min_price': min_price,
        'seller_products': seller_products,
    }
    return render(request, 'main/product_detail.html', context)









