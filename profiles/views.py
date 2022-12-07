from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse, reverse_lazy
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdate, ChangePasswordForm
from django.contrib import messages
from shop.models import Product
from .models import Rating, Order, Product, OrderItem, ShippingAddress
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, ceil
import json
import datetime


def RegistrationFormView(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('/')

    else:
        form = UserRegistrationForm()

    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']
    return render(request, 'profiles/register.html', {'form': form, 'cartItems': cartItems})


# searching product
def searchProduct(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        # tuple unpacking
        order, created = Order.objects.get_or_create(
            profile=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    if request.method == 'POST':
        search = request.POST.get('search')
        if search:
            product = Product.objects.filter(product_name__icontains=search)
            data = {'product': product, 'cartItems': cartItems}
            return render(request, 'profiles/search.html', data)
        else:
            data = {'product': None, 'cartItems': cartItems}
            return render(request, 'profiles/search.html', data)

# data for single product/book


def productDetail(request, book_id):
    if request.user.is_authenticated:
        customer = request.user.profile
        # tuple unpacking
        order, created = Order.objects.get_or_create(
            profile=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    book = Product.objects.get(id=book_id)
    ratings = Rating.objects.filter(product=book)
    data = {'book': book, 'ratings': ratings,
            'order': order, 'cartItems': cartItems}
    print(ratings)
    return render(request, 'profiles/product.html', data)


# for updating Cart
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action: ', action)
    print('ProductId:', productId)

    customer = request.user.profile
    product = Product.objects.get(id=productId)

    # tuple unpacking
    order, created = Order.objects.get_or_create(
        profile=customer, completed=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add' and orderItem.quantity < product.quantity:
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


# Editing User profile
@login_required
def ProfileEdit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdate(request.POST, request.FILES,
                               instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profiles:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdate(instance=request.user.profile)

    if request.user.is_authenticated:
        customer = request.user.profile
        # tuple unpacking
        order, created = Order.objects.get_or_create(
            profile=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    return render(request, 'profiles/edit_profile.html', {'cartItems': cartItems, 'u_form': u_form, 'p_form': p_form})


@login_required
def ProfileView(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        # tuple unpacking
        order, created = Order.objects.get_or_create(
            profile=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    return render(request, 'profiles/profile.html', {'cartItems': cartItems})


# Password Change
class PasswordsChangeView(PasswordChangeView):
    success_url = reverse_lazy('home')
    form_class = ChangePasswordForm
    template_name = 'profiles/change_password.html'


# Data for Carts


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        # tuple unpacking
        order, created = Order.objects.get_or_create(
            profile=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    data = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'profiles/cart.html', data)

# Data for checkout


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        # tuple unpacking
        order, created = Order.objects.get_or_create(
            profile=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    data = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'profiles/checkout.html', data)


def recommendationGenerator(request):
    
    books = Product.objects.all()
    ratings = Rating.objects.all()
    
    x = []
    y = []
    A = []
    B = []
    C = []
    D = []
    
    for item in books:
        x = [item.id, item.product_name, item.product_pic.url,
             item.genres, item.digital, item.quantity, item.price]
        y += [x]
    books_df = pd.DataFrame(
        y, columns=['bookId', 'product_name', 'product_pic', 'genres', 'digital', 'quantity', 'price'])
    print("Books data frame")
    print(books_df)
    print(books_df.dtypes)

    
    for item in ratings:
        A = [item.user.id, item.product.id, item.rating]
        B += [A]
    rating_df = pd.DataFrame(B, columns=['userId', 'bookId', 'rating'])
    print("Rating Dataframe")
    rating_df['userId'] = rating_df['userId'].astype(str).astype(np.int64)
    rating_df['bookId'] = rating_df['bookId'].astype(str).astype(np.int64)
    rating_df['rating'] = rating_df['rating'].astype(str).astype(np.float)
    print(rating_df)
    print(rating_df.dtypes)
    if request.user.is_authenticated:
        userid = request.user.id
        
        userInput = Rating.objects.select_related(
            'product').filter(user=userid)
        print(userInput)
        if userInput.count() == 0:
            recommenderQuery = None
            userInput = None
        else:
            for item in userInput:
                C = [item.product.product_name, item.rating]
                D += [C]
            inputBooks = pd.DataFrame(D, columns=['product_name', 'rating'])
            print("Rated books")
            inputBooks['rating'] = inputBooks['rating'].astype(
                str).astype(np.float)
            print(inputBooks.dtypes)

            
            inputId = books_df[books_df['product_name'].isin(
                inputBooks['product_name'].tolist())]
            

            inputBooks = pd.merge(inputId, inputBooks)
            
            print(inputBooks)

           
            userSubset = rating_df[rating_df['bookId'].isin(
                inputBooks['bookId'].tolist())]
            print(userSubset.head())

            
            userSubsetGroup = userSubset.groupby(['userId'])

            
            userSubsetGroup = sorted(
                userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)

            print(userSubsetGroup[0:])

            userSubsetGroup = userSubsetGroup[0:]

            
            pearsonCorrelationDict = {}

        
            for name, group in userSubsetGroup:
                
                group = group.sort_values(by='bookId')
                inputBooks = inputBooks.sort_values(by='bookId')
                
                nRatings = len(group)
                
                temp_df = inputBooks[inputBooks['bookId'].isin(
                    group['bookId'].tolist())]
                
                tempRatingList = temp_df['rating'].tolist()
                
                tempGroupList = group['rating'].tolist()
                
                Sxx = sum([i**2 for i in tempRatingList]) - \
                    pow(sum(tempRatingList), 2)/float(nRatings)
                Syy = sum([i**2 for i in tempGroupList]) - \
                    pow(sum(tempGroupList), 2)/float(nRatings)
                Sxy = sum(i*j for i, j in zip(tempRatingList, tempGroupList)) - \
                    sum(tempRatingList)*sum(tempGroupList)/float(nRatings)

                
                if Sxx != 0 and Syy != 0:
                    pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
                else:
                    pearsonCorrelationDict[name] = 0

            print(pearsonCorrelationDict.items())

            pearsonDF = pd.DataFrame.from_dict(
                pearsonCorrelationDict, orient='index')
            pearsonDF.columns = ['similarityIndex']
            pearsonDF['userId'] = pearsonDF.index
            pearsonDF.index = range(len(pearsonDF))
            print(pearsonDF.head())

            topUsers = pearsonDF.sort_values(
                by='similarityIndex', ascending=False)[0:]
            print(topUsers.head())

            topUsersRating = topUsers.merge(
                rating_df, left_on='userId', right_on='userId', how='inner')
            topUsersRating.head()

            
            topUsersRating['weightedRating'] = topUsersRating['similarityIndex'] * \
                topUsersRating['rating']
            topUsersRating.head()

            
            tempTopUsersRating = topUsersRating.groupby(
                'bookId').sum()[['similarityIndex', 'weightedRating']]
            tempTopUsersRating.columns = [
                'sum_similarityIndex', 'sum_weightedRating']
            tempTopUsersRating.head()

            
            recommendation_df = pd.DataFrame()
            
            recommendation_df['weighted average recommendation score'] = tempTopUsersRating['sum_weightedRating'] / \
                tempTopUsersRating['sum_similarityIndex']
            recommendation_df['bookId'] = tempTopUsersRating.index
            recommendation_df.head()

            recommendation_df = recommendation_df.sort_values(
                by='weighted average recommendation score', ascending=False)
            recommender = books_df.loc[books_df['bookId'].isin(
                recommendation_df.head(10)['bookId'].tolist())]
            print(recommender)
            return recommender.to_dict('records')


def returnRecommendation(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        # tuple unpacking
        order, created = Order.objects.get_or_create(
            profile=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    recommendation = recommendationGenerator(request)
    data = {'recommendation': recommendation, 'cartItems': cartItems}
    return render(request, 'profiles/recommendation.html', data)

#Transaction and shipment


def processOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(
            profile=customer, completed=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_total:
            order.completed = True
        order.save()
        if order.shipping == True:
            ShippingAddress.objects.create(profile=customer, order=order,
                                           address=data['shipping']['address'],
                                           city=data['shipping']['city'],
                                           zipcode=data['shipping']['zipcode'],
                                           )
    else:
        print("User not logged in..")

    print("Data:", data)
    return JsonResponse("Payment Successfull.", safe=False)


def processReview(request):
    data = json.loads(request.body)
    bookId = data['bookDetail']['id']
    bookName = data['bookDetail']['name']
    book = Product.objects.get(id=bookId)
    if request.user.is_authenticated:
        customer = request.user
        review_title = data['formReviewData']['title']
        review_score = data['formReviewData']['review_score']
        review_text = data['formReviewData']['review_text']
        rating, updated = Rating.objects.update_or_create(
            user=customer, product=book)
        rating.title = review_title
        rating.rating = review_score
        rating.review = review_text
        rating.save()
    else:
        print("User not logged in..")
    print(data)
    return JsonResponse("Reviewed Successfully.", safe=False)
