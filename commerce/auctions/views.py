from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from .forms import *
from .models import *
from datetime import datetime

def index(request):
    return render(request, "auctions/index.html",{
        'Listing' : Product.objects.all(),
        'user' : request.user
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        form = NewProductForm(request.POST)
        if form.is_valid():
            newProduct = form.save(commit=False)
            newProduct.selled_by = User.objects.get(id=int(request.user.id))
            newProduct.created_at = datetime.now()
            newProduct.is_closed = False
            if newProduct.image_link == None:
                newProduct.image_link = "No image"
            newProduct.save()
            return HttpResponseRedirect(reverse('index'))
    form = NewProductForm()
    return render(request, 'auctions/create.html', {
        'form' : form,
    })

def detail(request,product_title):
    form = NewBidForm() # 입찰을 위한 폼

    product = Product.objects.get(title=product_title)

    # user 가 익명일떄
    if request.user.id == None:
        # comment 보여주기
        comments = Comment.objects.filter(product_id=product.id)
        # Result 보여주기

        return render(request,'auctions/detail.html',{
            'product' : product,
            'form' : form,
            'comments' : comments,
        })

    user_id = User.objects.get(id=int(request.user.id))
    # 유저의 watchlist를 가져온다
    if Watchlist.objects.filter(user_id=user_id, product_id=product):
        flag = True
    else:
        flag = False

    # comment 보여주기
    comments = Comment.objects.filter(product_id=product.id)
    # Result 보여주기
    results = Result.objects.filter(user_id=user_id, product_id=product)

    return render(request,'auctions/detail.html',{
        'product' : product,
        'flag' : flag,
        'form' : form,
        'comments' : comments,
        'results' : results
    })

def watch_list(request):
    user_id = int(request.user.id)
    watch_list = Watchlist.objects.filter(user_id=user_id)

    return render(request,'auctions/watch_list.html',{
        'watch_list' : watch_list,
    })

@login_required(login_url='/login')
def update_watch_list(request):
    if request.method == "POST":
        product_id = Product.objects.get(id=int(request.POST['product_id']))
        user_id = User.objects.get(id=int(request.user.id))
        product = Watchlist.objects.filter(user_id=user_id,product_id=product_id)

        if product:
            product.delete()
        else:
            Watchlist.objects.create(user_id=user_id,product_id=product_id)

        return HttpResponseRedirect(reverse('watch_list'))
    return render(request,'auctions/watch_list.html',{
    })

@login_required(login_url='/login')
def bid(request):
    product = Product.objects.get(id=int(request.POST['product_id']))
    if request.method == "POST":
        form = NewBidForm(request.POST)
        product = Product.objects.get(id=int(request.POST['product_id']))
        start_bidding = product.price
        my_bidding = int(request.POST['bidding'])
        if form.is_valid():
            if start_bidding <= my_bidding:
                bidding = form.save(commit=False)
                bidding.user_id = User.objects.get(id=int(request.user.id))
                bidding.product_id = Product.objects.get(id=int(request.POST['product_id']))
                bidding.save()

                # HttpResponseRedirect로 해야함
                return render(request, 'auctions/detail.html',{
                    'product' : product,
                    'product_id' : request.POST['product_id'],
                    'message' : "Your bid is current bid"
                })
            return render(request, 'auctions/detail.html',{
                'product' : product,
                'form' : NewBidForm(),
                'product_id' : request.POST['product_id'],
                'message' : "bid is so far"
            })
    return render(request,'auctions/detail.html',{
        'form' : form
    })

def close_auction(request):
    if request.method == 'POST':
        try:
            bidding_list = Bid.objects.filter(product_id=int(request.POST['product_id'])).order_by('-bidding')[:1]

            product = Product.objects.get(id=int(request.POST['product_id']))
            product.is_closed = True
            product.save()

        # 결과 저장
            for bidding in bidding_list:
                user_id = bidding.user_id

        # 로그인 사용자의 id가 아니라 가장 높은 금액을 제시한 사용자의 id를 기록해야
            product_id = Product.objects.get(id=int(request.POST['product_id']))

            for bidding in bidding_list:
                successful_bid = bidding.bidding

            Result.objects.create(user_id=user_id,product_id=product_id,successful_bid=successful_bid)
            return render(request, 'auctions/result.html',{
                'bidding_list' : bidding_list,
                'successful_bid' : successful_bid
            })

        except:
            bidding_list = Bid.objects.filter(product_id=int(request.POST['product_id'])).order_by('-bidding')[:1]

            product = Product.objects.get(id=int(request.POST['product_id']))
            product.is_closed = False
            product.save()
            return render(request,'auctions/error.html',{

            })

def categories(request):
    products = Product.objects.all()
    categories = Product.categories
    lists = []
    for category in categories:
        lists.append(category[0])
    return render(request,'auctions/categories.html', {
        'lists' : lists,
        'products' : products,


    })

@login_required(login_url='/login')
def comment(request):
    if request.method == 'POST':
        user_id = User.objects.get(id=int(request.user.id))
        product = Product.objects.get(id=int(request.POST['product_id']))

        comment = request.POST['comment']
        Comment.objects.create(user_id=user_id,product_id=product,content=comment)
        comments = Comment.objects.filter(product_id=product.id)
        return render(request,'auctions/detail.html', {
            'product_title' : product.title,
            'product' : product,
            'comments' : comments
        })
