from django.shortcuts import get_object_or_404, render, redirect
from .forms import ProductForm, InventoryForm
from .models import Product, Inventory
from users.models import CartItem
from django.contrib.auth.decorators import login_required, user_passes_test



def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')  
    else:
        form = ProductForm()
    
    return render(request, 'product_form.html', {'form': form})


def inventory_list(request):
    query = request.GET.get('query') 
    category = request.GET.get('category') 

    products = Product.objects.all()  

   
    if query:
        products = products.filter(name__icontains=query)  

   
    if category:
        products = products.filter(category__icontains=category) 

    inventory_items = Inventory.objects.all()  

    
    inventory_products = {}
    for inventory in inventory_items:
        inventory_products[inventory] = products.filter(inventory=inventory)

    return render(request, 'inventory_list.html', {
        'products': products,
        'inventory_items': inventory_items,
        'inventory_products': inventory_products,  
        'query': query,  
        'category': category,  
    })




def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def create_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list') 
    else:
        form = InventoryForm()

    return render(request, 'create_inventory.html', {'form': form})

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()  
        return redirect('product_list')  
    return render(request, 'confirm_delete.html', {'product': product}) 

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)  
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product) 
        if form.is_valid():
            form.save()  
            return redirect('product_list') 
    else:
        form = ProductForm(instance=product)  

    return render(request, 'product_form.html', {'form': form})

def add_product_to_inventory(request, inventory_id):
    inventory = get_object_or_404(Inventory, inventoryId=inventory_id)

    if request.method == 'POST':
        product_id = request.POST.get('product_id') 
        product = get_object_or_404(Product, id=product_id)

        return redirect('inventory_list')  

    products = Product.objects.filter(inventory=inventory)  
    return render(request, 'add_product_to_inventory.html', {
        'inventory': inventory,
        'products': products,
    })


def is_admin(user):
    return user.is_staff

@login_required 
@user_passes_test(is_admin) 
def admin_cart(request):
    # Fetch all cart items, including processed ones
    cart_items = CartItem.objects.select_related('user', 'product')
    
    # Create a dictionary to map cart items to their associated products
    cart_products = {cart_item: cart_item.product for cart_item in cart_items}
    
    # Calculate the total price for all cart items
    total = sum(cart_item.get_total_price() for cart_item in cart_items)
    
    return render(request, 'admin_cart.html', {
        'cart_items': cart_items,
        'cart_products': cart_products,
        'total': total,
    })


