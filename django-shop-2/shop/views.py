from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import Category, Product, Contact, Review, Size, Variants
from cart.forms import CartAddProductForm
from .forms import ContactForm, ReviewForm
from django.views.generic import View
from django.http.response import HttpResponse, HttpResponseRedirect


def index(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    trending_products = Product.objects.filter(trending=1)
    return render(request, 'shop/index.html', context={
        'category': category,
        'categories': categories,
        'products': products,
        'trending_products': trending_products})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render (request, 'shop/product/list.html', context={
        'category': category,
        'categories': categories,
        'products': products,
    })

def product_detail(request, id, slug):
    trending_products = Product.objects.filter(trending=1)
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    context = {'product':product,
               'cart_product_form':cart_product_form,
               'trending_products':trending_products}

    if product.variant != "None":
        if request.method == 'POST':
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)
            sizes = Variants.objects.raw('SELECT * FROM  shop_variants  WHERE product_id=%s GROUP BY size_id', [id])
        else:
            variants = Variants.objects.filter(product_id=id)
            sizes = Variants.objects.raw('SELECT * FROM  shop_variants  WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)

        context.update({'sizes': sizes,
                        'variant': variant,
                        })

    return render(request, 'shop/product/detail.html', context)







def about_us(request):
    return render(request, "shop/information/about_us.html")

def questions_answer(request):
    return render(request, "shop/information/questions_answer.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST or None)
        errors = None
        if form.is_valid():
            Contact.objects.create(
                first_name = form.cleaned_data.get('first_name'),
                last_name = form.cleaned_data.get('last_name'),
                email = form.cleaned_data.get('email'),
                message = form.cleaned_data.get('message')
                )
            messages.warning(request,"Запит на зворотний зв'язок надіслано. Очікуйте...")
            return render(request,"shop/information/contacts.html")
        if form.errors:
            errors = form.errors

        context = {'form':form, 'errors':errors}
        return render(request,"shop/information/contacts.html", context )
    else:
        form = ContactForm()

    return render(request, "shop/information/contacts.html", {'form':form})


def review(request):
    reviews = Review.objects.all()
    review_form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST or None)
        errors = None
        if form.is_valid():
            Review.objects.create(
                first_name = form.cleaned_data.get('first_name'),
                last_name = form.cleaned_data.get('last_name'),
                email = form.cleaned_data.get('email'),
                review_text = form.cleaned_data.get('review_text')
                )
            messages.warning(request,"Відгук додано успішно!")
            return render(request,"shop/information/review.html", context={'reviews':reviews})
        if form.errors:
            errors = form.errors

        context = {'form':form, 'errors':errors, 'reviews':reviews}
        return render(request,"shop/information/review.html", context )
    else:
        form = ReviewForm()

    return render(request, "shop/information/review.html", {'form':form, 'reviews':reviews})
