from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib import messages
from shop.models import Product
from .models import Rating, Order, Product, OrderItem, ShippingAddress
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, ceil


def index(request):
    return render(request, 'profiles/base.html')


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

    return render(request, 'profiles/register.html', {'form': form})

# data for single product/book


def productDetail(request, book_name):
    book = Product.objects.filter(product_name=book_name)
    data = {'book': book}
    return render(request, 'profiles/product.html', data)


# for updating Cart
def updateItem(request):
    return JsonResponse("Item was added", safe=False)


@login_required
def ProfileView(request):
    return render(request, 'profiles/profile.html')


# Data for Carts
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        # tuple unpacking
        order, created = Order.objects.get_or_create(
            profile=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    data = {'items': items, 'order': order}
    return render(request, 'profiles/cart.html', data)

# Data for checkout


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        # tuple unpacking
        order, created = Order.objects.get_or_create(
            profile=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    data = {'items': items, 'order': order}
    return render(request, 'profiles/checkout.html', data)


def recommendationGenerator(request):
    # fetching books and rating from database
    books = Product.objects.all()
    ratings = Rating.objects.all()
    # data storage for calculation
    x = []
    y = []
    A = []
    B = []
    C = []
    D = []
    # Books dataframe
    for item in books:
        x = [item.id, item.product_name, item.product_pic.url,
             item.genres, item.digital, item.quantity, item.price]
        y += [x]
    books_df = pd.DataFrame(
        y, columns=['bookId', 'product_name', 'product_pic', 'genres', 'digital', 'quantity', 'price'])
    print("Books data frame")
    print(books_df)
    print(books_df.dtypes)

    # Rating dataframe
    for item in ratings:
        A = [item.user.id, item.product, item.rating]
        B += [A]
    rating_df = pd.DataFrame(B, columns=['userId', 'bookId', 'rating'])
    print("Rating Dataframe")
    rating_df['userId'] = rating_df['userId'].astype(str).astype(np.int64)
    rating_df['bookId'] = rating_df['bookId'].astype(str).astype(np.int64)
    rating_df['rating'] = rating_df['rating'].astype(str).astype(np.int64)
    print(rating_df)
    print(rating_df.dtypes)
    if request.user.is_authenticated:
        userid = request.user.id
        # select related is join statement in django.It looks for foreign key and join the table
        userInput = Rating.objects.select_related('books').filter(user=userid)
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

            # filtering out books by title/product_name
            inputId = books_df[books_df['product_name'].isin(
                inputBooks['product_name'].tolist())]
            # Then merging it so we can get the bookId. It's implicitly merging it by title/product_name.

            inputBooks = pd.merge(inputId, inputBooks)
            # #Dropping information we won't use from the input dataframe
            # inputBooks = inputBooks.drop('year', 1)
            # Final input dataframe
            # If a book you added in above isn't here, then it might not be in the original
            # dataframe or it might spelled differently, please check capitalisation.
            print(inputBooks)

            # Filtering out users that have watched books that the input has watched and storing it
            userSubset = rating_df[rating_df['bookId'].isin(
                inputBooks['bookId'].tolist())]
            print(userSubset.head())

            # Groupby creates several sub dataframes where they all have the same value in the column specified as the parameter
            userSubsetGroup = userSubset.groupby(['userId'])

            # print(userSubsetGroup.get_group(7))

            # Sorting it so users with book most in common with the input will have priority
            userSubsetGroup = sorted(
                userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)

            print(userSubsetGroup[0:])

            userSubsetGroup = userSubsetGroup[0:]

            # Store the Pearson Correlation in a dictionary, where the key is the user Id and the value is the coefficient
            pearsonCorrelationDict = {}

        # For every user group in our subset
            for name, group in userSubsetGroup:
                # Let's start by sorting the input and current user group so the values aren't mixed up later on
                group = group.sort_values(by='bookId')
                inputBooks = inputBooks.sort_values(by='bookId')
                # Get the N for the formula
                nRatings = len(group)
                # Get the review scores for the books that they both have in common
                temp_df = inputBooks[inputBooks['bookId'].isin(
                    group['bookId'].tolist())]
                # And then store them in a temporary buffer variable in a list format to facilitate future calculations
                tempRatingList = temp_df['rating'].tolist()
                # Let's also put the current user group reviews in a list format
                tempGroupList = group['rating'].tolist()
                # Now let's calculate the pearson correlation between two users, so called, x and y
                Sxx = sum([i**2 for i in tempRatingList]) - \
                    pow(sum(tempRatingList), 2)/float(nRatings)
                Syy = sum([i**2 for i in tempGroupList]) - \
                    pow(sum(tempGroupList), 2)/float(nRatings)
                Sxy = sum(i*j for i, j in zip(tempRatingList, tempGroupList)) - \
                    sum(tempRatingList)*sum(tempGroupList)/float(nRatings)

                # If the denominator is different than zero, then divide, else, 0 correlation.
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

            # Multiplies the similarity by the user's ratings
            topUsersRating['weightedRating'] = topUsersRating['similarityIndex'] * \
                topUsersRating['rating']
            topUsersRating.head()

            # Applies a sum to the topUsers after grouping it up by userId
            tempTopUsersRating = topUsersRating.groupby(
                'bookId').sum()[['similarityIndex', 'weightedRating']]
            tempTopUsersRating.columns = [
                'sum_similarityIndex', 'sum_weightedRating']
            tempTopUsersRating.head()

            # Creates an empty dataframe
            recommendation_df = pd.DataFrame()
            # Now we take the weighted average
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
    recommendation = recommendationGenerator(request)
    return render(request, 'profiles/recommendation.html', recommendation)
