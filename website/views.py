
from django.shortcuts import render, redirect
from django.contrib import messages
from website import models
from django.http import HttpResponse
from decimal import Decimal
from django.db.models import Q
from collections import defaultdict
from datetime import datetime
import razorpay
from django.conf import settings
from django.http import JsonResponse
from .models import PaymentOrder 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))


import json
import os

FIXED_USERNAME = "admin"
PASSWORD_FILE = "password_store.json"

def load_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            return json.load(file)
    return {"password": "password123"}  

def save_password(password_store):
    with open(PASSWORD_FILE, "w") as file:
        json.dump(password_store, file)

password_store = load_password()

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if username == FIXED_USERNAME and password == password_store["password"]:
            messages.success(request, "Login successful!")
            return redirect("/dashbord")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")

def forgot_password_view(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        
        if old_password == password_store["password"]:
            if new_password == confirm_password:
                password_store["password"] = new_password
                save_password(password_store)
                messages.success(request, "Password updated successfully!")
                return redirect("/forgot_password")
            else:
                messages.error(request, "New passwords do not match.")
        else:
            messages.error(request, "Old password is incorrect.")
    
    return render(request, "forgot_password.html")



def dashbord(req):
    bills = models.Bill.objects.all()

    total_sum = sum(bill.total for bill in bills)

    brand = models.Stack.objects.all()
    custmore = models.Customer.objects.all()

    obj = {
        "brand": brand,
        "custmore": custmore,
        "bills": bills,
        "total_sum": total_sum
    }
    return render(req, "dashbord.html", obj)



def total_sum(req):
    bills = models.Bill.objects.all()

    # Handle date filtering
    start_date = req.GET.get("start_date")
    end_date = req.GET.get("end_date")
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            bills = bills.filter(date__range=(start_date, end_date))
        except ValueError:
            messages.error(req, "Invalid date format. Please use YYYY-MM-DD.")

    bill_list = [
        {
            "id": bill.id,
            "customer": bill.customer.Customer_name,
            "total": bill.total,
            "date": bill.date,
        }
        for bill in bills
    ]
    total_sum = sum(bill["total"] for bill in bill_list)

    context = {
        "bill_list": bill_list,
        "total_sum": total_sum,
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(req, "total_sum.html", context)


def available_stock(req):
    brand=models.Stack.objects.all()
    obj={"brand":brand}
    return render(req,"available_stock.html",obj)

def customer_visits(req):
    custmore=models.Customer.objects.all()
    obj={"custmore":custmore}
    return render(req,"customer_visits.html",obj)

from django.utils import timezone
from datetime import timedelta


def Notifaction(req):
    bills = models.Bill.objects.all()    
    seven_days_ago = timezone.now() - timedelta(days=7)
    new_bills = bills.filter(date__gte=seven_days_ago).order_by('-date')  
    old_bills = bills.filter(date__lt=seven_days_ago).order_by('-date')  
    total_sum = sum(bill.total for bill in bills)
    return render(req, "Notifaction.html", {
        "new_bills": new_bills, 
        "old_bills": old_bills, 
        "total_sum": total_sum
    })

def home(req):
	return render(req,"home.html")

def Profile(req):
    shop = models.Shop_info.objects.all() 
    obj={"shop":shop}
    return render(req,"Profile.html",obj)
    


#  -----------------------------------------------------------------------------------------------------------
def custmore_model(req):
    return render(req,"custmore_model.html")
   
def save_Customer(req):
    custmore=models.Customer(
        Customer_name=req.POST['Customer_name'],
        Customer_email=req.POST['Customer_email'],
        Customer_phone=req.POST['Customer_phone'],
        Customer_addres=req.POST['Customer_addres']
    )
    custmore.save()
    return redirect("/custmore_model")

def custmore_list(req):
     custmore=models.Customer.objects.all()
     obj={"custmore":custmore}
     return render(req,"custmore_list.html",obj)

def delete_custmore(req):
    order_id=req.GET['id']
    models.Customer.objects.get(id = order_id).delete()
    return redirect("/custmore_list")

def edit_custmore(req):
    edit=models.Customer.objects.get(id=req.GET['id'])
    obj={"edit":edit}
    return render(req,"edit_custmore.html",obj)

def update_file(req):
    update=models.Customer.objects.get(id=req.POST['id'])
    update.Customer_name=req.POST['Customer_name']
    update.Customer_email=req.POST['Customer_email']
    update.Customer_phone=req.POST['Customer_phone']
    update.Customer_addres=req.POST['Customer_addres']
    update.save()
    return redirect("/custmore_list")

def add_brand(req):
     return render(req,"add_brand.html")

def add_brand_list(req):
     brand=models.Stack.objects.all()
     obj={"brand":brand}
     return render(req,"add_brand_list.html",obj)


def save_brand(req):
    brand=models.Stack(
            brandr_name=req.POST['brandr_name'],
            brandr_Value=req.POST['brandr_Value'],
            add_product_value=req.POST['add_product_value']
    )
    brand.save()
    return redirect("/add_brand")

def delete_brand(req):
    order_id=req.GET['id']
    models.Stack.objects.get(id = order_id).delete()
    return redirect("/add_brand_list")


def edit_brand(req):
    edit=models.Stack.objects.get(id=req.GET['id'])
    obj={"edit":edit}
    return render(req,"edit_brand.html",obj)

def update_brand(req):
    update=models.Stack.objects.get(id=req.POST['id'])
    update.brandr_name=req.POST['brandr_name']
    update.brandr_Value=req.POST['brandr_Value']
    update.add_product_value=req.POST['add_product_value']
    update.save()
    return redirect("/add_brand_list")


def add_bill(req):
    customer=models.Customer.objects.all()
    stack = models.Stack.objects.all()
    bill=models.Bill.objects.all()
    obj={"customer":customer,"stack":stack,"bill":bill}
    return render(req,"add_bill.html",obj)


def save_bill(req):
    if req.method == "POST":
        customer_name = req.POST.get("customer_name", "").strip()
        customer_phone = req.POST.get("customer_phone", "").strip()

        if not customer_name:
            messages.error(req, "Customer name is required.")
            return redirect("/add_bill")

        if not customer_phone.isdigit() or len(customer_phone) != 10:
            messages.error(req, "Valid phone number is required.")
            return redirect("/add_bill")

        customer, created = models.Customer.objects.get_or_create(
            Customer_name=customer_name,
            defaults={"phone": customer_phone}
        )
        if not created and customer.phone != customer_phone:
            customer.phone = customer_phone
            customer.save()

        stack_ids = req.POST.getlist("stack[]")
        quantities = req.POST.getlist("quantity[]")
        paid_price = Decimal(req.POST.get("paid_price", "0"))
        total_subtotal = Decimal(0)
        aggregated_data = defaultdict(lambda: {"quantity": 0, "subtotal": Decimal(0)})

        for stack_id, quantity_str in zip(stack_ids, quantities):
            try:
                quantity = int(quantity_str)
                stack_item = models.Stack.objects.get(id=stack_id)

                if stack_item.add_product_value < quantity:
                    messages.error(req, f"Insufficient stock for {stack_item.brandr_name}.")
                    return redirect("/add_bill")

                stack_item.add_product_value -= quantity
                stack_item.save()
                subtotal = Decimal(stack_item.brandr_Value) * quantity
                total_subtotal += subtotal

                aggregated_data[stack_id]["quantity"] += quantity
                aggregated_data[stack_id]["subtotal"] += subtotal
            except models.Stack.DoesNotExist:
                messages.error(req, f"Stack item with ID {stack_id} not found.")
                return redirect("/add_bill")
            except ValueError:
                messages.error(req, "Invalid quantity provided.")
                return redirect("/add_bill")

        gov_tax = total_subtotal * Decimal("0.1")
        total = total_subtotal + gov_tax

        for stack_id, data in aggregated_data.items():
            stack_item = models.Stack.objects.get(id=stack_id)
            models.Bill.objects.create(
                customer=customer,
                stack=stack_item,
                quantity=data["quantity"],
                subtotal=data["subtotal"],
                gov_tax=gov_tax,
                total=total,
                paid_price=paid_price,
            )

        messages.success(req, "Bill saved successfully!")
        return redirect(f"/bill_print/{customer.id}")

    return redirect("/add_bill")




#----------------------------------------------------------------------------------------------
def bill_print(req, customer_id):
    shop = models.Shop_info.objects.all() 
    customer = models.Customer.objects.get(id=customer_id)  
    bills = models.Bill.objects.filter(customer=customer) 
    total_sum = sum(bill.total for bill in bills) 
    paid_price_sum = sum(bill.paid_price for bill in bills)

    for bill in bills:
        bill.baki = bill.total - bill.paid_price  
    context = {
        "shop": shop,
        "customer": customer,
        "bills": bills,
        "total_sum": total_sum,
        "paid_price": paid_price_sum  
    }
    
    return render(req, "bill_print.html", context)

from . import models

def Profile_info(req):
    shop = models.Shop_info.objects.all()

    if shop:
        edit_info = shop[0]
        return render(req, "Profile_info.html", {"edit_info": edit_info, "shop": shop})
    
    return render(req, "Profile_info.html", {"shop": shop})

def save_bill_info(req):
    if req.method == 'POST':
        shop_id = req.POST.get('id')

        if shop_id: 
            shop = models.Shop_info.objects.get(id=shop_id)
            shop.shop_name = req.POST['shop_name']
            shop.shop_owner_name = req.POST['shop_owner_name']
            shop.shop_number = req.POST['shop_number']
            shop.shop_email = req.POST['shop_email']
            shop.shop_address = req.POST['shop_address']
            shop.save()
        else: 
            shop = models.Shop_info(
                shop_name=req.POST['shop_name'],
                shop_owner_name=req.POST['shop_owner_name'],
                shop_number=req.POST['shop_number'],
                shop_email=req.POST['shop_email'],
                shop_address=req.POST['shop_address']
            )
            shop.save()
        return redirect("/Profile_info")

def edit_Info(req):
    shop_id = req.GET.get('id')
    if shop_id:
        edit_info = models.Shop_info.objects.get(id=shop_id)
        return render(req, "Profile_info.html", {"edit_info": edit_info})
    return redirect("/Profile_info")




def Purchase_list(request):
    search_query = request.GET.get('search_name', '') 
    shop = models.Shop_info.objects.all()

    if search_query.isdigit():
        bills = models.Bill.objects.filter(id=search_query)
    else:
        bills = models.Bill.objects.filter(customer__Customer_name__icontains=search_query)

    bills = bills.order_by('-id')  

    total_sum = sum(bill.total for bill in bills)
    paid_price_sum = sum(bill.paid_price for bill in bills)

    for bill in bills:
        bill.baki = bill.total - bill.paid_price

    return render(request, "Purchase_list.html", {
        "bills": bills,
        "total_sum": total_sum,
        "search_query": search_query,
        "shop": shop,
        "paid_price": paid_price_sum,
    })




def delete_Purchase(req):
    order_id=req.GET['id']
    models.Bill.objects.get(id = order_id).delete()
    return redirect("/Purchase_list")
# ----------------------------------------------------------------------------------------------

def Return(req):
    bills = models.Bill.objects.all()
    context = {"bills": bills}
    return render(req, "Return.html", context)


def process_return(req):
    if req.method == "POST":
        bill_id = req.POST.get("bill_id") 
        return_quantity = int(req.POST.get("quantity"))  
        try:
            bill = models.Bill.objects.get(id=bill_id)
            stack_item = bill.stack  

            stack_item.add_product_value += return_quantity
            stack_item.save()

            bill.quantity -= return_quantity
            bill.subtotal -= Decimal(stack_item.brandr_Value) * return_quantity
            gov_tax = bill.subtotal * Decimal("0.1")
            bill.total = bill.subtotal + gov_tax

            if bill.quantity <= 0:
                bill.delete()
            else:
                bill.save()
            messages.success(req, "Return processed successfully!")
        except models.Bill.DoesNotExist:
            messages.error(req, "Invalid Bill ID. Please try again.")
        except Exception as e:
            messages.error(req, f"An error occurred: {str(e)}")
    
    return redirect("/Return")




def Calendar(req):
    return render(req,"Calendar.html")

def Pyment(req):
    customers = models.Customer.objects.all()

    selected_customer = None
    customer_total_spent = None

    if req.method == 'POST' and 'customer' in req.POST:
        selected_customer = models.Customer.objects.get(id=req.POST['customer'])
        
        customer_total_spent = sum(bill.total for bill in models.Bill.objects.filter(customer=selected_customer))
        
        order_amount = float(customer_total_spent) if customer_total_spent else 1000.0  # Fallback to 1000 if no spending
    else:
        order_amount = 1000.0

    order_currency = 'INR'

    payment_order = client.order.create(dict(amount=int(order_amount * 100), currency=order_currency, payment_capture=1))  # Razorpay expects amount in paise
    order_id = payment_order['id']

    PaymentOrder.objects.create(order_id=order_id, amount=order_amount, status='locked')

    context = {
        'amount': order_amount,  
        'api_key': settings.RAZORPAY_API_KEY,
        'order_id': order_id,
        'customers': customers, 
        'selected_customer': selected_customer,
        'customer_total_spent': customer_total_spent
    }

    return render(req, "pyment.html", context)



def verify_payment(req):
    payment_data = json.loads(req.body.decode('utf-8'))  
    payment_id = payment_data['payment_id']
    order_id = payment_data['order_id']
    signature = payment_data['signature']

    payment_order = PaymentOrder.objects.get(order_id=order_id)

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        payment_order.status = 'unlocked'
        payment_order.save()

        customer = models.Customer.objects.get(id=payment_data['customer_id'])
        customer.total_spent += payment_order.amount  
        customer.save()

        return JsonResponse({'status': 'success'})

    except razorpay.errors.SignatureVerificationError:
        payment_order.status = 'failed'
        payment_order.save()

        return JsonResponse({'status': 'failure'})


