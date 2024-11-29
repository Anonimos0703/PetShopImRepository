# users/views.py
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from appointment.models import Appointment
from django.shortcuts import render, get_object_or_404
from .models import Product, CartItem, Order,ProductRating
from .forms import CustomerForm
from .models import Customer
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        
    else:
        form = SignUpForm()
            
    return render(request, 'users/signup.html', {'form': form})



from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
            else:
                messages.error(request, "Invalid username or password.")  # Add error message for invalid login
                return redirect('login')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)  
            return redirect('login')
    else:
        form = AuthenticationForm()
    storage = messages.get_messages(request)
    storage.used = True

    return render(request, 'users/login.html', {'form': form})

 

def logout_view(request):
    logout(request)
    return redirect('login')


def aboutus(request):
    return render(request, 'users/aboutus.html')

def uproduct_list(request):
    products = Product.objects.only('name', 'price', 'image')
    
    query = request.GET.get('query')
    category = request.GET.get('category')
    
    if query and category:
        products = products.filter(name__icontains=query, category__icontains=category)
    elif query:
        products = products.filter(name__icontains=query)
    elif category:
        products = products.filter(category__icontains=category)


    return render(request, 'users/uproduct_list.html', {'products': products})



def service(request):
    return render(request, 'users/service.html')

def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'users/product_details.html', {'product': product})

def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()
        else:
            if 'cart' not in request.session:
                request.session['cart'] = {}
            if str(id) in request.session['cart']:
                request.session['cart'][str(id)] += quantity
            else:
                request.session['cart'][str(id)] = quantity
            request.session.modified = True
        
        if request.is_ajax():
            return JsonResponse({'success': True, 'message': 'Product added to cart.'})
        
        return redirect('cart')

# @login_required
# def cart(request):
#     cart_items = []
#     total = 0
#     insufficient_stock = any(item.quantity > item.product.stock for item in cart_items)
#     context = {
#     'cart_items': cart_items,
#     'total': total,
#     'insufficient_stock': insufficient_stock,
# }

#     if request.user.is_authenticated:
#         cart_items = CartItem.objects.filter(user=request.user)
#         total = sum(item.get_total_price() for item in cart_items)
#     else:
#         if 'cart' in request.session:
#             cart = request.session['cart']
#             for product_id, quantity in cart.items():
#                 product = get_object_or_404(Product, id=product_id)
#                 cart_items.append({
#                     'product': product,
#                     'quantity': quantity,
#                     'total_price': quantity * product.price,
#                 })
#                 total += quantity * product.price
        

#     return render(request, 'users/cart.html', context,{'cart_items': cart_items, 'total': total})

@login_required
def cart(request):
    cart_items = []
    total = 0
    insufficient_stock = False  # Initialize to False

     
    # Fetch cart items for authenticated users
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)

    # Check for insufficient stock using the `quantity` field
    insufficient_stock = any(item.quantity > item.product.quantity for item in cart_items)

    # Consolidate context
    context = {
        'cart_items': cart_items,
        'total': total,
        'insufficient_stock': insufficient_stock,
    }

    return render(request, 'users/cart.html', context)


def remove_from_cart(request,id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, user=request.user, product__id=id)
        cart_item.delete()
    else:
        if 'cart' in request.session:
            cart = request.session['cart']
            if str(id) in cart:
                del cart[str(id)]
                request.session.modified = True

    return redirect('cart')



def home(request):
   # Keep your original query exactly as is
    products = Product.objects.only('name', 'price', 'image')
    
    # Only apply filters if search terms are actually entered
    query = request.GET.get('query')
    category = request.GET.get('category')
    
    if query and category:
        products = products.filter(name__icontains=query, category__icontains=category)
    elif query:
        products = products.filter(name__icontains=query)
    elif category:
        products = products.filter(category__icontains=category)
    return render(request, 'users/home.html',{'products': products})  


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        pass
    
    context = {
        'user': user,
    }
    return render(request, 'users/profile.html', context)



def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'users/appointment_schedule.html', {'appointments': appointments})


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)

    for cart_item in cart_items:
        if not cart_item.product.reduce_quantity(cart_item.quantity):
            messages.error(request, f'Insufficient stock for {cart_item.product.name}')
            return redirect('cart')  # Redirect back to cart if stock is insufficient

    if request.method == 'POST':
        cart_items.delete()
        return redirect('order_confirmation')
    

    return render(request, 'users/checkout.html', {'cart_items': cart_items, 'total': total})
    
def order_confirmation(request):
    return render(request, 'users/order_confirmation.html')

@login_required
def payment_method(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':            
        request.session['cart_total'] = str(total)
        return render(request, 'users/payment_method.html', {'cart_items': cart_items, 'total': total})

    return redirect('cart')

@login_required
def process_payment(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(item.get_total_price() for item in cart_items)

        if not cart_items:
            messages.error(request, 'Your cart is empty.')
            return redirect('cart')

        try:
            # Check and reduce product quantities first
            for cart_item in cart_items:
                if not cart_item.product.reduce_quantity(cart_item.quantity):
                    messages.error(request, f'Insufficient stock for {cart_item.product.name}')
                    return redirect('cart')

            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                payment_method=payment_method.capitalize(),
                status='Pending'
            )

            for cart_item in cart_items:
                cart_item.order = order
                cart_item.save()

            cart_items.delete()

            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True

            if payment_method == 'gcash':
                messages.success(request, 'Order placed successfully! Proceeding with GCash payment...', extra_tags='order-confirmation')
               
            elif payment_method == 'paypal':
                messages.success(request, 'Order placed successfully! Redirecting to PayPal...', extra_tags='order-confirmation')

            return redirect('order_confirmation')

        except Exception as e:
            messages.error(request, f'An error occurred while processing your order: {str(e)}')
            return redirect('cart')

    return redirect('payment_method')


def confirm_payment(request):
    return render(request, 'order_confirmation.html')

 

@login_required
def edit_profile(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'users/edit_profile.html', {'form': form})


def product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = ProductRating.objects.filter(product=product)
    return render(request, 'users/product_etails.html', {'product': product, 'reviews': reviews})