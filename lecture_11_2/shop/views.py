from django.shortcuts import render, redirect
from .models import Product, Category, BasketItem
from .forms import CategoryProductForm, ProductForm, CategoryForm
from django.contrib import messages
from django.core.paginator import Paginator

DEFAULT_SIZE = 12
DEFAULT_PAGE = 1
DEFAULT_ORDER_BY = 'name'

sizes = [4, 8, 12, 24]


def products_page_view(request):
    page = request.GET.get('page', DEFAULT_PAGE)
    size = request.GET.get('size', DEFAULT_SIZE)
    most_expensive_price = Product.objects.all().order_by('-price')[0].price
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', most_expensive_price)
    name = request.GET.get('name', '')
    # name -name price -price
    order_by = request.GET.get('order_by', DEFAULT_ORDER_BY)
    products = Product.objects \
        .filter(name__contains=name) \
        .filter(price__lte=max_price) \
        .filter(price__gte=min_price) \
        .order_by(order_by)
    paginator = Paginator(products, size)
    page_obj = paginator.get_page(page)
    return render(request, 'shop/products.html', {
        'paginator': paginator,
        'page_obj': page_obj,
        'sizes': sizes,
        'order_by': order_by,
        'min_price': min_price,
        'max_price': max_price,
        'name': name
    })


def index_page_view(request):
    categories = Category.objects.all()
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = Category(name=form.data.get('name'))
            category.save()
        return render(request, 'shop/index.html', {'categories': categories, 'form': form})
    return render(request, 'shop/index.html', {'categories': categories, 'form': form})


def category_page_view(request, pk):
    if request.method == 'GET':
        category = Category.objects.get(id=pk)
        products = Product.objects.filter(category_id=category.id)
        form = CategoryProductForm()
        return render(request, 'shop/category.html', {'category': category, 'products': products, 'form': form})
    if request.method == 'POST':
        category = Category.objects.get(id=pk)
        products = Product.objects.filter(category_id=category.id)
        form = CategoryProductForm(request.POST)
        if form.is_valid():
            name = form.data.get('name')
            price = form.data.get('price')
            amount = form.data.get('amount')
            description = form.data.get('description')
            product = Product(name=name, price=price, amount=amount, description=description, category_id=category.id)
            product.save()
            products = Product.objects.filter(category_id=category.id)
            form = CategoryProductForm()
            return render(request, 'shop/category.html', {'category': category, 'products': products, 'form': form})
        return render(request, 'shop/category.html', {'category': category, 'products': products, 'form': form})


def edit_product_page_view(request, pk):
    product = Product.objects.get(id=pk)
    categories = Category.objects.all()
    if request.method == 'GET':
        form = ProductForm(data={'name': product.name, 'price': product.price, 'amount': product.amount,
                                 'description': product.description, 'category': product.category.id})
        return render(request, 'shop/edit-product.html', {'product': product, 'form': form, 'categories': categories})
    if request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.data.get('name', product.name)
            product.price = form.data.get('price', product.price)
            product.amount = form.data.get('amount', product.amount)
            product.description = form.data.get('description', product.description)
            product.category_id = form.data.get('category', product.category.id)
            product.save()
            return redirect(to='products_page')
        else:
            form = ProductForm(data={'name': product.name, 'price': product.price, 'amount': product.amount,
                                     'description': product.description, 'category': product.category.id})
            return render(request, 'shop/edit-product.html',
                          {'product': product, 'form': form, 'categories': categories})


def product_details_page_view(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'shop/product-details.html', {'product': product})


def delete_product_page_view(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        return redirect(to='products_page')
    except Product.DoesNotExist as e:
        messages.error(request, 'Could delete product since it does not exist')
        return redirect(to='products_page')


def basket_page_view(request):
    if request.user and request.user.is_authenticated:
        orders = BasketItem.objects.filter(owner_id=request.user.id)
        return render(request, 'shop/basket.html', {'orders': orders})
    else:
        return redirect('/auth/login/')


def add_to_basket_view(request, pk):
    if request.user and request.user.is_authenticated:
        product = Product.objects.get(id=pk)
        try:
            prev_order = BasketItem.objects.get(product_id=product.id, owner_id=request.user.id)
            prev_order.amount += 1
            prev_order.save()
        except BasketItem.DoesNotExist as e:
            order = BasketItem(product_id=product.id, owner_id=request.user.id)
            order.save()
        return redirect('/basket')
    else:
        return redirect('/auth/login/')



def delete_from_basket_view(request, pk):
    if request.user and request.user.is_authenticated:
        order = BasketItem.objects.get(id=pk)
        order.delete()
        return redirect('/basket')
    else:
        return redirect('/auth/login/')

