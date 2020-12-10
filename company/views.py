from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import Company, Category, Product
import crypt

# company_id = ""


def login(request):
    return render(request, 'company/login.html')

def home(request):
    company_id = request.POST.get('id1')
    user = Company.objects.get(id=company_id)
    return render(request, 'company/index.html', {'company': user})

def index(request):
    email_addr = request.POST.get('email', 'default')
    password = request.POST.get('pass', 'default')

    try:
        # global company_id
        user = Company.objects.get(email=email_addr)
        actual_pass = user.password

        # company_id = user.id

        if(crypt.crypt(password, actual_pass) == actual_pass):
            return render(request, 'company/index.html', {'company': user})
        else:
            messages.success(request, "Wrong Password")
            return render(request, 'company/login.html')

    except:
        messages.success(request, "Invalid User")
        return render(request, 'company/login.html')



def redirect(request):
    user_name = request.POST.get('name')
    email_addr = request.POST.get('email')
    phone_no = request.POST.get('phone')
    addr = request.POST.get('address')
    passw = request.POST.get('password1')
    # print(user_name, gender, email_addr, phone_no, addr, passw

    user = Company(name = user_name,email = email_addr,phone = phone_no,address = addr,
                password = crypt.crypt(passw))  
    user.save()

    return render(request, 'company/login.html')


def signup(request):
    params = {'user_name':'', 'email_addr':'', 'phone':'', 
                'addr':'', 'pass1':'', 'passw2':''}
    params['msg'] = ""
    if(request.method == 'POST'):
        user_name = request.POST.get('name')
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
            user = Company(name = user_name,email = email_addr,phone = phone_no,address = addr,
                password = crypt.crypt(passw))  
            user.save()
            return render(request, 'company/login.html')

    return render(request, 'company/signup.html', params)


def addProduct(request):
    company_id = request.POST.get('id1')
    user = Company.objects.get(id=company_id)
    data = Category.objects.all()
    return render(request, 'company/addProduct.html', {'categories': data, 'company': user})


def addProductTo(request):
    company_id = request.POST.get('id1')
    try:
        if(request.method == 'POST'):
            category = request.POST.get('category')
            pname = request.POST.get('pname')
            pdesc = request.POST.get('Description')
            pprice = request.POST.get('pprice')
            pquantity = request.POST.get('pquantity')
            pimage = request.FILES.get('pimage')
            fs = FileSystemStorage()
            img_name = fs.save(pimage.name, pimage)

            category_obj = Category.objects.get(name=category)
            comp1 = Company.objects.get(id=company_id)

            prod = Product(name=pname, desc=pdesc, price=pprice, quantity=pquantity, image=fs.url(img_name),
                           category_id=category_obj, comp_id = comp1)
            prod.save()

    except:
        pass
    finally:
        return addProduct(request)


def deleteProduct(request):
    company_id = request.POST.get('id1')
    user = Company.objects.get(id=company_id)
    products = Product.objects.filter(comp_id=company_id)
    return render(request, 'company/deleteProduct.html', {'products': products, 'total': len(products), 'company': user})


def deleteProd(request, prod_id):
    company_id = request.POST.get('id1')
    user = Company.objects.get(id=company_id)
    item_to_delete = Product.objects.get(id=prod_id)
    item_to_delete.delete()
    products = Product.objects.filter(comp_id=company_id)
    return render(request, 'company/deleteProduct.html', {'products': products, 'total': len(products), 'company': user})


def updateProduct(request):
    company_id = request.POST.get('id1')
    user = Company.objects.get(id=company_id)
    products = Product.objects.filter(comp_id=company_id)
    return render(request, 'company/updateProduct.html', {'products': products, 'total': len(products), 'company': user})


def updateProd(request, prod_id):
    company_id = request.POST.get('id1')
    user = Company.objects.get(id=company_id)
    item_to_update = Product.objects.get(id=prod_id)
    categories = Category.objects.all()
    return render(request, 'company/saveUpdate.html',
                  {'prod':item_to_update, 'categories':categories, 'company': user})


def saveChanges(request, prod_id):
    company_id = request.POST.get('id1')
    user = Company.objects.get(id=company_id)
    
    prod = Product.objects.get(id=prod_id)
    
    category = request.POST.get('category')
    pname = request.POST.get('pname')
    pdesc = request.POST.get('Description')
    pprice = request.POST.get('pprice')
    pquantity = request.POST.get('pquantity')
    pimage = request.FILES.get('pimage')

    try:
        category_obj = Category.objects.get(name=category)

        prod.category_id = category_obj
        prod.name = pname
        prod.desc = pdesc
        prod.price = pprice
        prod.quantity = pquantity

        fs = FileSystemStorage()
        img_name = fs.save(pimage.name, pimage)
        prod.image = fs.url(img_name)
    except:
        pass
    finally:
        prod.save()

    return updateProduct(request)


def viewProduct(request):
    company_id = request.POST.get('id1')
    user = Company.objects.get(id=company_id)
    products = Product.objects.filter(comp_id=company_id)
    return render(request, 'company/viewProduct.html', {'products': products, 'total': len(products), 'company': user})


def addCategory(request):
    company_id = request.POST.get('id1')
    user = Company.objects.get(id=company_id)
    data = Category.objects.all()
    return render(request, 'company/addCategory.html', {'categories':data, 'total': len(data), 'company': user})


def submitCategory(request):
    try:
        category = request.POST.get('categoryname')

        categ = Category(name=category)
        categ.save()

        return addCategory(request)
    except:
        return addCategory(request)
