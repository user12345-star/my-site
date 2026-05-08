from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Promotion, Product, Review, Order, UserProfile, Comment
from .forms import CommentForm, UserRegistrationForm, ReviewForm, OrderForm


def main(request):
    promotions = Promotion.objects.all()
    products = Product.objects.all()[:6]
    reviews = Review.objects.select_related('user__userprofile').order_by('-date_created')[:3]

    sent = False
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and comment_form.is_valid():
        comment_form.save()
        sent = True

    context = {
        'promotions': promotions,
        'products': products,
        'reviews': reviews,
        'comment_form': comment_form,
        'sent': sent,
    }
    return render(request, 'portal/main.html', context)


def about(request):
    promotions = Promotion.objects.all()
    sent = False
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and comment_form.is_valid():
        comment_form.save()
        sent = True

    context = {
        'promotions': promotions,
        'comment_form': comment_form,
        'sent': sent,
    }
    return render(request, 'portal/about.html', context)


def products(request):
    products_list = Product.objects.all()
    promotions = Promotion.objects.all()
    sent = False
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and comment_form.is_valid():
        comment_form.save()
        sent = True

    context = {
        'products': products_list,
        'promotions': promotions,
        'comment_form': comment_form,
        'sent': sent,
    }
    return render(request, 'portal/products.html', context)


def sale(request):
    promotions = Promotion.objects.all()
    sent = False
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and comment_form.is_valid():
        comment_form.save()
        sent = True

    context = {
        'promotions': promotions,
        'comment_form': comment_form,
        'sent': sent,
    }
    return render(request, 'portal/sale.html', context)



@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    promotions = Promotion.objects.all()
    sent = False
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.product = product
        comment.save()
        sent = True

    context = {
        'product': product,
        'promotions': promotions,
        'comment_form': comment_form,
        'sent': sent,
    }
    return render(request, 'portal/product_detail.html', context)


CATEGORY_DISPLAY_NAMES = {
    'roses': 'РОЗЫ',
    'tulips': 'ТЮЛЬПАНЫ',
    'peonies': 'ПИОНЫ',
    'lilies': 'ЛИЛИИ',
    'daisies': 'РОМАШКИ',
    'baskets': 'КОРЗИНЫ С ЦВЕТАМИ',

    'classic': 'КЛАССИЧЕСКИЕ',
    'original': 'ОРИГЕНАЛЬНЫЕ',
    'edible': 'СЪЕДОБНЫЕ',
    'wedding': 'СВАДЕБНЫЕ',
}


def category(request, category_name):
    if category_name in dict(Product.FLOWERS_CHOICES):
        products = Product.objects.filter(flowers=category_name)
    elif category_name in dict(Product.BOUQUETS_CHOICES):
        products = Product.objects.filter(bouquets=category_name)
    else:
        products = Product.objects.none()

    display_name = CATEGORY_DISPLAY_NAMES.get(category_name, category_name)

    promotions = Promotion.objects.all()
    sent = False
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and comment_form.is_valid():
        comment_form.save()
        sent = True

    context = {
        'products': products,
        'category_name': display_name,
        'promotions': promotions,
        'comment_form': comment_form,
        'sent': sent,
    }
    return render(request, 'portal/category.html', context)


@login_required
def user_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    user_orders = Order.objects.filter(user_profile=profile)
    has_orders = user_orders.exists()

    sent_comment = False
    sent_review = False

    comment_form = CommentForm(request.POST or None)
    review_form = ReviewForm(request.POST or None)

    if request.method == 'POST':
        if comment_form.is_valid():
            comment_form.save()
            sent_comment = True

        if 'review_text' in request.POST:
            if review_form.is_valid():
                Review.objects.create(
                    user=user,
                    review_text=review_form.cleaned_data['review_text']
                )
                sent_review = True

        if 'update_profile' in request.POST:
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            profile.phone = phone
            if 'profile_photo' in request.FILES:
                profile.profile_photo = request.FILES['profile_photo']
            profile.save()

        return redirect('user_profile')

    context = {
        'user': user,
        'profile': profile,
        'orders': user_orders.order_by('-order_date'),
        'promotions': Promotion.objects.all(),
        'comment_form': comment_form,
        'review_form': review_form,
        'sent_comment': sent_comment,
        'sent_review': sent_review,
        'has_orders': has_orders,
    }

    return render(request, 'portal/user.html', context)


def register(request):
    error_login = None
    form = UserRegistrationForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('user_profile')
        elif 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('user_profile')
            else:
                error_login = 'Неверный логин или пароль'

    context = {
        'form': form,
        'error_login': error_login,
        'promotions': Promotion.objects.all(),
    }
    return render(request, 'portal/register.html', context)


def user_logout(request):
    logout(request)
    return redirect('main')


@login_required
def order(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.product = product
            order.user_profile = request.user.userprofile
            order.name = form.cleaned_data['first_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.quantity = form.cleaned_data['quantity']
            order.address = form.cleaned_data['address']
            order.delivery_date = form.cleaned_data['delivery_date']
            order.wishes = form.cleaned_data['wishes']
            if form.cleaned_data['option'] == 'При получении':
                order.payment_method = 'upon_receipt'
            else:
                order.payment_method = 'immediate'
            order.save()
            return redirect('done')
    else:
        form = OrderForm()

    context = {
        'product': product,
        'promotions': Promotion.objects.all(),
        'order_form': form,
    }
    return render(request, 'portal/order.html', context)

def done(request):
    promotions = Promotion.objects.all()
    sent = False
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and comment_form.is_valid():
        comment_form.save()
        sent = True

    context = {
        'promotions': promotions,
        'comment_form': comment_form,
        'sent': sent,
    }
    return render(request, 'portal/done.html', context)

