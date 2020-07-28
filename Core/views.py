from django.shortcuts import render
from .forms import HouseForm
import pickle
import pandas as pd
import numpy as np
import joblib
from django.contrib import messages
import json

# Create your views here.

def home(request):
    return render(request,'home.html')

def predict_price(total_sqft,bath,bhk,location):
    with open("C://Users//sumanth//Desktop//MY_DJANGO//Banglore_Home_Prediction//Core//columns.json", "r") as f:
        col = json.load(f)['data_columns']
        locations =col[3:]
    model=joblib.load('C://Users//sumanth//Desktop//MY_DJANGO//Banglore_Home_Prediction//Core//banglore_home_prices_model.pickle')
    try:
        loc_index =col.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(col))
    x[0] = total_sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1
    return int(round(model.predict([x])[0],0))

def details(request):
    if request.method=='POST':
        form=HouseForm(request.POST)
        if form.is_valid():
            total_sqft=form.cleaned_data.get('total_sqft')
            bath=form.cleaned_data.get('bath')
            bhk=form.cleaned_data.get('bhk')
            location=form.cleaned_data.get('location')
            print(total_sqft,bath,bhk,location)
            answer=predict_price(total_sqft,bath,bhk,location)
            if answer>0:
                messages.success(request,'Application Status : {} Lakhs'.format(answer))
            else:
                messages.success(request,"Status : Within {0} Square Feet Its Not Possible In {1} Area".format(total_sqft,location))
        else:
            redirect('home')
    form=HouseForm()
    return render(request,'form.html',{'form':form})
