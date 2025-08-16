from django.shortcuts import render
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Requires Pillow library
import pandas as pd
from sklearn.linear_model import LinearRegression
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import VehicleAd
from .forms import VehicleAdForm
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm
from .models import Feedback


def ads_list(request):
    query = request.GET.get('q')
    if query:
        ads = VehicleAd.objects.filter(name__icontains=query)
    else:
        ads = VehicleAd.objects.all()

    return render(request, 'ads/ads_list.html', {'ads': ads, 'query': query})

@login_required
def post_ad(request):
    if request.method == 'POST':
        form = VehicleAdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.posted_by = request.user
            ad.save()
            return redirect('ads_list')
    else:
        form = VehicleAdForm()
    return render(request, 'ads/post_ad.html', {'form': form})


def run_script_view(request):
    car_name = request.POST.get('car_name')
    year = request.POST.get('year')
    present_price = request.POST.get('present_price')
    kms_driven = request.POST.get('kms_driven')
    fuel_type = request.POST.get('fuel_type')
    seller_type = request.POST.get('seller_type')
    transmission = request.POST.get('transmission')
    owner = request.POST.get('owner')
    try:
        # Load the car data from CSV

        cars_df = pd.read_csv('cardata.csv')
        print("Column names in CSV:", cars_df.columns.tolist())

        # Filter out bike names if necessary
        car_names = cars_df[~cars_df['Car_Name'].str.contains('Bike', case=False)]['Car_Name'].unique()

        # Prepare data for prediction
        X = cars_df[['Year', 'Present_Price', 'Kms_Driven', 'Fuel_Type', 'Seller_Type', 'Transmission', 'Owner']]
        X = pd.get_dummies(X, columns=['Fuel_Type', 'Seller_Type', 'Transmission'], drop_first=True)
        y = cars_df['Selling_Price']

        # Train Linear Regression model
        model = LinearRegression()
        model.fit(X, y)

        # Prediction logic
        car_name = car_name
        year = year # Use int type for numeric fields
        present_price = present_price
        kms_driven = kms_driven
        fuel_type = kms_driven
        seller_type = seller_type
        transmission = transmission
        owner = owner

        # Prepare input data for prediction
        input_data = pd.DataFrame([[year, present_price, kms_driven, fuel_type, seller_type, transmission, owner]],
                                  columns=['Year', 'Present_Price', 'Kms_Driven', 'Fuel_Type', 'Seller_Type',
                                           'Transmission', 'Owner'])

        # Convert categorical variables to one-hot encoding
        input_data = pd.get_dummies(input_data, columns=['Fuel_Type', 'Seller_Type', 'Transmission'], drop_first=True)

        # Align input data with training data columns
        input_data = input_data.reindex(columns=X.columns, fill_value=0)

        # Predict using the model
        predicted_price = model.predict(input_data)
        print(predicted_price)

        # Add a success message with the predicted price
        messages.success(request, f"The predicted selling price of the car is: ₹{predicted_price[0]:.2f} lakhs")

    except Exception as e:
        # Handle any errors during the process
       print(e)
    # Redirect back to the "Post an Ad" page after execution
    print(1)

    return redirect('post_ad')


def car_data_view(request):
    return render(request, 'car_form.html')





def submit_feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            # feedback.user = request.user
            feedback.save()
            return redirect('/')  # Redirect to a 'Thank you' page after submitting
    else:
        form = FeedbackForm()

    return render(request, 'submit_feedback.html', {'form': form})

@login_required
def admin_feedback_view(request):
    if request.user.is_staff:
        feedback_list = Feedback.objects.all().order_by('-created_at')
        return render(request, 'admin_feedback.html', {'feedback_list': feedback_list})
    else:
        return redirect('home')  # Redirect non-admin users
