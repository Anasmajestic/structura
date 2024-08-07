from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .import models
import random,string
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
import razorpay

# Create your views here.

def home(request):
    return render(request,"home.html")

@login_required(login_url="login")
def contact(request):
    if request.method=='POST':
        name=request.POST["name"]
        email=request.POST["email"]
        mobile=request.POST["mobile"]
        time=request.POST["time"]

        cons=models.Support.objects.create(name=name,mail=email,mobile=mobile,time=time)
        cons.save()
        messages.success(request,f"Our Support Will Contact You In {time}")
        return redirect("home")
    return render(request,"contact.html")

def uniqueId(fname,lname,length=2):
    if len(fname) % 2 == 0:
        chars=string.digits
    else:
        chars=string.ascii_letters
    name=fname+lname
    while True:
        username=name.join(random.choices(chars,k=length))
        if not models.User.objects.filter(username=username):
            return username

def signin(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method=='POST':
            firstname=request.POST["fname"]
            lastname=request.POST["lname"]
            email=request.POST["email"]
            username=email
            password1=request.POST["pwd1"]
            password2=request.POST["pwd2"]

            if password1==password2:
                if models.User.objects.filter(email=email).exists():
                    messages.warning(request,"Email Already Exists..!")
                    return redirect("signin")
                elif not email.endswith("@gmail.com"):
                    messages.warning(request,"Please use gmail account")
                    return redirect("signin")
                else:
                    user_create=models.User.objects.create_user(username=username,email=email,password=password1,first_name=firstname,last_name=lastname)
                    user_create.save()
                    messages.warning(request,"Email Already Exists..!")
                    return redirect("login")
            else:
                messages.warning(request,"Password does not match..!")
                return redirect("signin")
        else:
            return render(request,"create.html")

def loginPage(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            email=request.POST["email"]
            pwd=request.POST["pwd"]
            user=authenticate(username=email,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,f"Welcome {request.user.first_name}")
                return redirect("home")
            else:
                messages.warning(request,"Something Error, Please check The Password or Email")
                return redirect("login")
        return render(request,"login.html")
    return redirect("home")

def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.warning(request,"Please login to access your account..!")
        return redirect("login")
    else:
        return redirect("home")


def category(request):
    categories=models.Category.objects.filter(status=0)
    return render(request,"category.html",{'category':categories})

def product(request,name):
    if(models.Category.objects.filter(name=name,status=0)):
        products=models.Product.objects.filter(category__name=name)
        return render(request,"product.html",{'product':products,"cat":name})
    else:
        messages.warning(request,"No Such Category Found")
        return redirect("category")

@login_required(login_url='login')
def product_details(request,cname,pname):
    if(models.Category.objects.filter(name=cname,status=0)):
        if(models.Product.objects.filter(id=pname,status=0)):
            details=models.Product.objects.filter(id=pname,status=0)
            return render(request,"pro_details.html",{'details':details})
        else:
            messages.warning(request,"Products not found")
            return redirect("product_details")
    else:
        messages.warning(request,"Category not found")
        return redirect("category")
    
@login_required(login_url='login')
def add_cart(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            id=request.POST["pro_id"]
            quantity=int(request.POST["pro_qty"])

            product=models.Product.objects.get(id=id)

            if product:
                if models.Cart.objects.filter(user=request.user.id,product_id=id):
                    cart=models.Cart.objects.get(user=request.user.id,product_id=id)
                    cart.products_qty +=1
                    cart.save()
                    return redirect("cart")
                else:
                    if product.quantity > quantity:
                        models.Cart.objects.create(user=request.user,product_id=id,products_qty=quantity)
                        messages.success(request,"Product added in cart successfully..")
                        return redirect("cart")
                    else:
                        suc="Not found"
                        return render(request,"home.html",{"suc":suc})
            else:
                suc="Waste"
                return render(request,"home.html",{"suc":suc})
    return render(request,"home.html",{"suc":"Not authenticated"})

@login_required(login_url='login')
def cart(request):
    adds=models.Address.objects.filter(user=request.user)
    data=models.Cart.objects.filter(user=request.user)
    sum=0
    for datas in data:
        sum+=datas.total_price

    return render(request,"cart.html",{'datas':data,'adds':adds,"sum":sum})

def cart_remove(request,id):
    cart=models.Cart.objects.get(id=id)
    cart.delete()
    messages.warning(request,"Item has deleted..!")
    return redirect('cart')

@login_required(login_url='login')
def address(request):
    if request.method=='POST':
        mobile=request.POST["mob"]
        house_no=request.POST["house"]
        street=request.POST["street"]
        area=request.POST["area"]
        city=request.POST["city"]
        pincode=request.POST["pin"]

        if models.Address.objects.filter(user=request.user,house_no=house_no,street=street).exists():
            messages.warning(request,"Address already exists..!")
            return redirect('address')
        else:
            data=models.Address.objects.create(user=request.user,mobile=mobile,house_no=house_no,street=street,area=area,city=city,pincode=pincode)
            data.save()
            messages.success(request,"Address Successfully Added..")
            return redirect("cart")
    else:
        return render(request,"address.html")


def success(request):
    if request.method=='POST':
        value=request.POST["adds"]
        cart_list=[]
        cart=request.POST["cart"]
        print("Cart:",cart)
        
        name=request.POST["name"]
        amt=int(request.POST["amt"])*100

        client=razorpay.Client(auth=("rzp_test_wWHPuNDhC1ivkp","FCNjFqzGy2DG2trsKvuHr8wI"))
        data = { "amount": amt, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        base=Payment(user=request.user,name=name,amount=amt,payment_id=payment['id'])
        base.save()
        
        order=models.Order.objects.create(user=request.user,address_id=value,cart_id=cart)
        order.save()
        return render(request,"payment.html",{'payment':payment})
    
def order(request):
    order=models.Order.objects.filter(user=request.user)
    delevery=models.Delivery.objects.create(
        user=request.user,
        cat_name=order[0].cart.product.category.name,
        products=order[0].cart.product.name,
        pro_qty=order[0].cart.products_qty,
        total_amt=order[0].cart.total_price,
        total_price=order[0].address.mobile,
        hno=order[0].address.house_no,
        street=order[0].address.street,
        area=order[0].address.area,
        city=order[0].address.city,
        pincode=order[0].address.pincode
    )
    delevery.save()
    return redirect("clear")


def pay(request):
    if request.method=='POST':
        name=request.POST["name"]
        amt=int(request.POST["amt"])*100
        client=razorpay.Client(auth=("rzp_test_wWHPuNDhC1ivkp","FCNjFqzGy2DG2trsKvuHr8wI"))
        data = { "amount": amt, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        print(payment)
        base=Payment(user=request.user,name=name,amount=amt,payment_id=payment['id'])
        base.save()
        return render(request,"index.html",{'paytem':payment})
    return render(request,"index.html")

@csrf_exempt
def finals(request):
    messages.success(request,"Order confirmed..")
    return redirect("order")

def clear(request):
    dele=models.Cart.objects.filter(user=request.user)
    dele.delete()
    messages.success(request,"Order Confirmed..!")
    return redirect("home")