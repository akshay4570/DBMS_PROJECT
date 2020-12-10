from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import Customer, Order, Shipping
from company.models import Category, Company, Product
from math import ceil
import webbrowser
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
import crypt
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import CheckSum

MERCHANT_KEY = '61ojC2&HGO2WPRZ8'
# userId = 4


def login(request):
    return render(request, 'ecom/login.html')


def redirect(request):
    user_name = request.POST.get('name')
    gender = request.POST.get('gender')
    email_addr = request.POST.get('email')
    phone_no = request.POST.get('phone')
    addr = request.POST.get('address')
    passw = request.POST.get('password1')

    user = Customer(username = user_name,sex = gender,email = email_addr,phone = phone_no,address = addr,
                password = crypt.crypt(passw))
    user.save()

    return render(request, 'ecom/login.html')


def signup(request):
    params = {'user_name':'', 'email_addr':'', 'phone':'', 
                'addr':'', 'pass1':'', 'passw2':''}
    params['msg'] = ""
    if(request.method == 'POST'):
        user_name = request.POST.get('name')
        gender = request.POST.get('gender')
        email_addr = request.POST.get('email')
        phone_no = request.POST.get('phone')
        addr = request.POST.get('address')
        passw = request.POST.get('password1')
        passw2 = request.POST.get('password2')

        if(passw != passw2):
            params['msg'] = "Password did not match"
            params['user_name'] = user_name
            params['email_addr'] = email_addr
            params['phone'] = phone_no
            params['addr'] = addr
            params['pass1'] = passw
        else:
            user = Customer(username = user_name,sex = gender,email = email_addr,phone = phone_no,address = addr,
                password = crypt.crypt(passw)) 
            user.save()
            return render(request, 'ecom/login.html')

    return render(request, 'ecom/signup.html', params)


def index(request):
    email_addr = request.POST.get('email', 'default')
    password = request.POST.get('pass', 'default')

    try:
        user = Customer.objects.get(email=email_addr)
        actual_pass = user.password

        if crypt.crypt(password, actual_pass) == actual_pass:
            # global userId
            # userId = user.id
            # print(userId)
            return render(request, 'ecom/index.html', {'user': user})
        else:
            messages.success(request, "Wrong Password")
            return render(request, 'ecom/login.html')

    except:
        messages.success(request, "Invalid User")
        return render(request, 'ecom/login.html')


def home(request):
    userId = request.POST.get('id1')
    user = Customer.objects.get(id=userId)
    return render(request, 'ecom/index.html', {'user': user})


def about(request):
    userId = request.POST.get('id1')
    user = Customer.objects.get(id=userId)
    return render(request, 'ecom/about.html', {'user': user})


def contact(request):
    userId = request.POST.get('id1')
    user = Customer.objects.get(id=userId)
    return render(request, 'ecom/contact.html', {'user': user})


def sendMail(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            userId = request.POST.get('id1')
            full_message = "Name: " + name + "\nEmail: " + email + "\nPhone No: " + phone + "\n\n" + message
            send_mail('Review', full_message, settings.EMAIL_HOST_USER,
                      ['coderkb@gmail.com', 'akshay4570@gmail.com', 'jithendrasrj@gmail.com'], fail_silently=False)
    except:
        pass
    finally:
        cust = Customer.objects.get(id=userId)
        return render(request, 'ecom/thanks.html', {"user":cust})

def thanks(request):
    return render(request, 'ecom/thanks.html')


def parameters(userId):
    # global userId
    user = Customer.objects.get(id=userId)
    username = user.email.split('@')[0]
    params = {'user': user, 'username': username}
    return params


def profile(request):
    id1 = request.POST.get("id1")
    params = parameters(id1)
    return render(request,'ecom/account.html',params)


def account(request):
    id1 = request.POST.get("id1")
    params = parameters(id1)
    return render(request, 'ecom/account.html', params)


def setting(request):
    id1 = request.GET.get("id1")
    msg = ""
    if(request.method == 'POST'):
        cur_pass = request.POST.get('cur_pass')
        pass1 = request.POST.get('pass1')

        userId = id1
        cust = Customer.objects.get(id=userId)
        print(cust)
        if(crypt.crypt(cur_pass, cust.password) == cust.password):
            msg = "Password Changed Successfully"
            cust.password = crypt.crypt(pass1)
            cust.save()
        else:
            msg = "Wrong Password"

    params = parameters(id1)
    params['msg'] = msg
    return render(request, 'ecom/settings.html', params)


def edit(request):
    id1 = request.GET.get("id1")
    params = parameters(id1)

    if request.method == 'POST':
        img = request.FILES.get('profile_image')
        fs = FileSystemStorage()
        name = fs.save(img.name,img)
        params['user'].image = fs.url(name)
        params['user'].save()

    return render(request, 'ecom/edit.html', params)


def changes(request):
    if (request.method == 'POST'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        sex = request.POST.get('sex')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')

        userId = request.POST.get('id1')

        user = Customer.objects.get(id=userId)
        user.username = name
        user.sex = sex
        user.email = email
        user.address = address
        user.phone = phone_no

        user.save()

        params = parameters(userId)
        return render(request, 'ecom/account.html', params)



def browse(request):
    products = Product.objects.all()
    categories = set(prod.category_id for prod in products)

    allProds = []
    for category in categories:
        prods = Product.objects.filter(category_id=category)
        n = len(prods)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prods, range(1, nSlides), nSlides])

        for prod in prods:
            prod.name = prod.name[:20]
            prod.name = prod.name.center(20,' ')
            prod.desc = prod.desc[:50]
            prod.desc = prod.desc[:25].center(25, ' ') + '\n' + prod.desc[25:].center(25, ' ')

    userId = request.POST.get('id1')
    user = Customer.objects.get(id=userId)
    return render(request, 'ecom/browse.html', {'allProds': allProds, 'user':user})


def searchMatch(query, item):
    '''return true only if query matches the item'''
    if(query.lower() in item.desc.lower() or query.lower() in item.name.lower() 
        or query.lower() in item.category_id.name.lower()):
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    
    products = Product.objects.all()
    cats = set(prod.category_id for prod in products)

    allProds = []
    for cat in cats:
        prodtemp = Product.objects.filter(category_id=cat)
        prods = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prods)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))

        for prod in prods:
            prod.name = prod.name[:20]
            prod.name = prod.name.center(20,' ')
            prod.desc = prod.desc[:50]
            prod.desc = prod.desc[:25].center(25, ' ') + '\n' + prod.desc[25:].center(25, ' ')

        if(n != 0):
            allProds.append([prods, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<2:
        params = {'msg': "Please make sure to enter relevant search query"}

    userId = request.GET.get('id1')
    user = Customer.objects.get(id=userId)
    params['user'] = user
    return render(request, 'ecom/search.html', params)


def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'ecom/prodView.html', {'product':product[0]})

def checkout(request):
    if request.method=="POST":
        total = request.POST.get('amount')
        prods = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = int(request.POST.get('zip', ''))
        phone = int(request.POST.get('phone', ''))
        userId = request.POST.get("id1")

        if(prods == "{}"):
            empty = True
            return render(request, 'ecom/checkout.html', {'empty':empty})

        d = json.loads(prods)
        for key, value in d.items():
            print(key, value);
            prod_id = key[2:]
            prod = Product.objects.get(id=prod_id)
            prod.quantity -= value[0]
            print(prod.quantity);
            prod.save()

        sids = [addr.sid for addr in Shipping.objects.all() if addr.cid.id == userId]

        cust = Customer.objects.get(id=userId)
        
        if(sids == []):
            addr = Shipping(cid=cust, name=name, email=email
                    ,address=address, city=city, state=state, 
                    zip_code=zip_code, phone=phone)
            addr.save()
            
            ordr = Order(prods=prods, cid=cust, sid=addr)
            ordr.save()
        else:
            for sid in sids:
                addr = Shipping.objects.get(sid=sid)
                if(addr.name == name and addr.email == email and
                    addr.city == city and addr.state == state and
                    addr.address == address and addr.zip_code == 
                    zip_code and addr.phone == phone):

                    ordr = Order(prods=prods, cid=cust, sid=addr)
                    ordr.save()
                    break
            else:
                addr = Shipping(cid=cust, name=name, email=email
                    ,address=address, city=city, state=state, 
                    zip_code=zip_code, phone=phone)
                addr.save()
                
                ordr = Order(prods=prods, cid=cust, sid=addr)
                ordr.save()

        thank = True
        id = ordr.id

        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': "gnlMss48967331097385",
                'ORDER_ID': str(ordr.id),
                'TXN_AMOUNT': str(total),
                'EMAIL': email,
                'CUST_ID': str(userId),
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/ecom/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = CheckSum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'ecom/paytm.html', {'param_dict': param_dict})

        # return render(request, 'ecom/checkout.html', {'thank':thank, 'id': id})

    return render(request, 'ecom/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = CheckSum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'ecom/paymentstatus.html', {'response': response_dict})