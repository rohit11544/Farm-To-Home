from django.http import HttpResponse
from django.shortcuts import render
from .models import farmer
from .models import city
from .models import Item
from django.contrib import messages
from django.db import connection
import pandas as pd 
import numpy as np
from sklearn import linear_model
import math
import joblib
import mysql.connector
import sqlalchemy
import folium 
# initialize Distance API 
from geopy.geocoders import Nominatim 
from geopy import distance 
geolocator = Nominatim(user_agent="geoapiExercises") 

engine = sqlalchemy.create_engine('mysql+pymysql://root:7337007435@localhost:3306/customer_farmer2')
# code for forms
from .forms import SearchFarmer,Registration,GetDetails,ChangePassword,FinalUpdateDetails

def customer(request):
    fm = SearchFarmer()
    return render(request,'customer.html',{'form':fm,'name1':'Search your farmer now!','name2': 'Enter your requirments to find a farmer'})

def Farmer_registration(request):
    fm = Registration()
    return render(request,"farmer.html",{'form':fm,'name1':'Farmers Information','name2': 'Registration'})

def redirect_to_update(request):
    fm = GetDetails()
    return render(request,"update_farmer.html",{'form':fm,'name1':'Updating Farmer','name2': 'Updating'})

def index(request):
    return render(request,"index.html")

# making connection with mysql connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="7337007435",
  database="customer_farmer2",
  auth_plugin = 'mysql_native_password',
)
mycursor = mydb.cursor()


query = str(city.objects.all().query)
cities_df = pd.read_sql_query(query, connection)
query = str(Item.objects.all().query)
items_df = pd.read_sql_query(query, connection)
# Create your views here.
def home(request):
    return render(request,'index.html')

def check(request):
    name = request.POST.get('Name')
    if(name=='farmer'):
        return render(request,'farmer.html',{})
    else:
        return render(request,'customer.html')


def join_farmer(request):
    query = str(farmer.objects.all().query)
    data_main = pd.read_sql_query(query, connection)
    if request.POST.get('Password')==request.POST.get('ConformPassword'):
        if request.method=='POST':
            servercord = farmer()
            servercord.Name = request.POST.get('Name')
            servercord.Phone_Number = request.POST.get('Phone_Number')
            servercord.Item = request.POST.get('Item')
            servercord.Organic_Inorganic = request.POST.get('Organic_Inorganic')
            ErrorCheck = 0
            for i in range(13):
                if (items_df['Item'].loc[[i]].item()==request.POST.get('Item')):
                    servercord.Price_Organic = items_df['OP'].loc[[i]].item()
                    servercord.Price_Inorganic = items_df['IP'].loc[[i]].item()
                    ErrorCheck = 1
                    break
            if ErrorCheck == 0:
                fm = Registration()
                return render(request,"farmer.html",{'form':fm,'name1':'INCORRECT Details please enter correctly','name2': 'Registration'})
            servercord.id = len(data_main.index) + 1
            servercord.City = request.POST.get('City')
            servercord.PinCode = request.POST.get('PinCode')
            servercord.Quantity = request.POST.get('Quantity')
            servercord.Availability = request.POST.get('Availability')
            servercord.Rating = 5
            servercord.Target = 0
            servercord.Price = 0
            servercord.UserName = request.POST.get('UserName')
            servercord.Password = request.POST.get('Password')
            
            servercord.save()
            messages.success(request,'Record saved successfully...!')
            return render(request,'farmer_output.html',{'name1': 'You have joined Successfully With id '+str(len(data_main.index) + 1),'name2':'All the best!'})
    fm = Registration()
    return render(request,"farmer.html",{'form':fm,'name1':'INCORRECT Details please enter correctly','name2': 'Registration'})





    
def update_farmer(request):
    if request.POST.get('FP'):
        fm = ChangePassword()
        return render(request,"forgot_password.html",{'form':fm})

    query = str(farmer.objects.all().query)
    data_main = pd.read_sql_query(query, connection)

    i = int(request.POST.get('GivenUserNum')) - 1
    if data_main['UserName'].loc[[i]].item() == request.POST.get('UserName'): 
        if data_main['Password'].loc[[i]].item() == int(request.POST.get('Password')):
            farmerList = []

            farmerList.append(
                            farmer(
                                data_main['id'].loc[[i]].item(),
                                data_main['Name'].loc[[i]].item(),
                                data_main['Phone_Number'].loc[[i]].item(),
                                data_main['Item'].loc[[i]].item(),
                                data_main['Price_Organic'].loc[[i]].item(),
                                data_main['Price_Inorganic'].loc[[i]].item(),
                                data_main['Price'].loc[[i]].item(),
                                data_main['City'].loc[[i]].item(),
                                data_main['PinCode'].loc[[i]].item(),
                                data_main['Organic_Inorganic'].loc[[i]].item(),
                                data_main['Rating'].loc[[i]].item(),
                                data_main['Quantity'].loc[[i]].item(),
                                data_main['Availability'].loc[[i]].item(),
                                data_main['Target'].loc[[i]].item()
                                )
                        )
            fm2 = FinalUpdateDetails()
            return render(request,"print_details.html",{'form':fm2,'farmers': farmerList,'name1':'Updating Farmer','name2':'Updating...'})
    fm = GetDetails()
    return render(request,"update_farmer.html",{'form':fm,'name1':'UserName or Password INCORRECT!!!','name2': 'Updating'})


def forgot_password(request):
    i = int(request.POST.get('GivenUserNum')) - 1
    query = str(farmer.objects.all().query)
    data_main = pd.read_sql_query(query, connection)
    
    if data_main['Name'].loc[[i]].item() == request.POST.get('Name'): 
        if data_main['City'].loc[[i]].item() == request.POST.get('City'):
            if int(request.POST.get('Password')) == int(request.POST.get('ConformPassword')):
                data_main.at[i, "Password"] = int(request.POST.get('ConformPassword'))
                sql = "DROP TABLE IF EXISTS feature1_farmer"
                mycursor.execute(sql)
                data_main.to_sql(name='feature1_farmer',con=engine,index=False)
                return render(request,"forgot_password_output.html")
    fm = ChangePassword()
    return render(request,"forgot_password.html",{'form':fm})



def update_farmer_info(request):
    query = str(farmer.objects.all().query)
    data_main = pd.read_sql_query(query, connection)
    i = int(request.POST.get('GivenUserNum')) - 1
    data_main.at[i, "Name"] = request.POST.get('Name')
    data_main.at[i, "Phone_Number"] = int(request.POST.get('Phone_Number'))
    data_main.at[i, "City"] = request.POST.get('City')
    data_main.at[i, "PinCode"] = request.POST.get('PinCode')
    data_main.at[i, "Item"] = request.POST.get('Item')
    data_main.at[i, "Quantity"] = request.POST.get('Quantity')
    data_main.at[i, "Organic_Inorganic"] = request.POST.get('Organic_Inorganic')
    data_main.at[i, "Availability"] = request.POST.get('Availability')

    for j in range(13):
        if (items_df['Item'].loc[[j]].item()==request.POST.get('Item')):
            data_main.at[i, "Price_Organic"] = items_df['OP'].loc[[j]].item()
            data_main.at[i, "Price_Inorganic"] = items_df['IP'].loc[[j]].item()
            break
              
    sql = "DROP TABLE IF EXISTS feature1_farmer"
    mycursor.execute(sql)
    data_main.to_sql(name='feature1_farmer',con=engine,index=False)

    farmerList = []

    farmerList.append(
                    farmer(
                        data_main['id'].loc[[i]].item(),
                        data_main['Name'].loc[[i]].item(),
                        data_main['Phone_Number'].loc[[i]].item(),
                        data_main['Item'].loc[[i]].item(),
                        data_main['Price_Organic'].loc[[i]].item(),
                        data_main['Price_Inorganic'].loc[[i]].item(),
                        data_main['Price'].loc[[i]].item(),
                        data_main['City'].loc[[i]].item(),
                        data_main['PinCode'].loc[[i]].item(),
                        data_main['Organic_Inorganic'].loc[[i]].item(),
                        data_main['Rating'].loc[[i]].item(),
                        data_main['Quantity'].loc[[i]].item(),
                        data_main['Availability'].loc[[i]].item(),
                        data_main['Target'].loc[[i]].item()
                        )
                )
    return render(request,"update_output.html",{'farmers': farmerList,'name1': 'DONE UPDATING','name2':'Updated your details successfully!!!'})


#def customer(request):
#    return render(request,"customer.html",{'name1':'Search your farmer now!','name2': 'Enter your requirments to find a farmer'})

def search_farmer(request):
    # importing the tabels 
    query = str(farmer.objects.all().query)
    data_main = pd.read_sql_query(query, connection)
    data = pd.read_sql_query(query, connection)
    data.drop(['id','Name','Phone_Number','Quantity'],axis=1,inplace=True)
    i=0
    for city in data_main["City"]:
        data_main.at[i, "City"] = city.replace(" ", "")
        data.at[i, "City"] = city.replace(" ", "")
        i+=1
    i=0
    for item in data_main["Item"]:
        data_main.at[i, "Item"] = item.replace(" ", "")
        data.at[i, "Item"] = item.replace(" ", "")
        i+=1
    # preprocessing the data
    data[['Item', 'City']] = data[['Item', 'City']].apply(lambda s: s.map({k:i for i,k in enumerate(s.unique())}))
    data['Rating'] = data['Rating']/5
    data_main['Price'] = data['Organic_Inorganic']*data['Price_Organic'] + (1 - 1*data['Organic_Inorganic'] )*data['Price_Inorganic']
    data.drop(['Price_Organic','Price_Inorganic','Price','UserName','Password'],axis=1,inplace=True)
    data['Target'] = round((data['Item']+data['City']+data['Organic_Inorganic']+data['Rating'])*data['Availability'])
    data_main['Target'] = data['Target']
    
    # training of the model
    X = data.drop(['Target','PinCode'], axis=1)
    Y = pd.DataFrame(data['Target'])
    ln = linear_model.LinearRegression()
    model = ln.fit(X,Y)

    # taking input
    user_Town = request.POST.get('Town')
    quantity = int(request.POST.get('Quantity'))
    user_Item = request.POST.get('Item')
    user_PinCode = request.POST.get('PinCode')
    
    # converting to numbers based on there index
    ErrorCheckCity = 0
    ErrorCheckItem = 0
    for i in range(40):
        if (cities_df['City'].loc[[i]].item()==user_Town):
            user_Town_index = cities_df['Index'].loc[[i]].item()
            ErrorCheckCity = 1
            break
    for i in range(13):
        if (items_df['Item'].loc[[i]].item()==user_Item):
            user_Item_index = items_df['Index'].loc[[i]].item()
            ErrorCheckItem = 1
            break
    if ErrorCheckItem!=1 or ErrorCheckCity!=1:
        fm = SearchFarmer()
        return render(request,'customer.html',{'form':fm,'name1':'City or Item INCORRECT!!!','name2': 'Enter your requirments to find a farmer'})


    x = np.array([[user_Item_index,user_Town_index,1,1,1]])
    y = math.floor(model.predict(x))
    
    i=0
    farmerList = []
    farmer_ID_List = []
    
    for target in data_main['Target']:
        town = data_main['City'].loc[[i]].item()
        Item = data_main['Item'].loc[[i]].item()
        if(target in range(y-30,y+30)):
            if(user_Town==town and user_Item==Item and (quantity<=data_main['Quantity'].loc[[i]].item())):
                farmerList.append(data_main['Target'].loc[[i]].item())
                farmer_ID_List.append(data_main['id'].loc[[i]].item())
        i+=1
    farmerList.sort(reverse=True)
    list_farmers_obj  = print_farmer(data_main,farmerList,quantity,farmer_ID_List,user_PinCode)
    return render(request,"customer_output.html",{'farmers': list_farmers_obj,'name1': 'Here are the best farmers for your search!', 'name2': 'Farmers!!' })
    

def print_farmer(data_main,farmerList,quantity,farmer_ID_List,user_PinCode):
    list_farmers_obj = [] 
    InDist=10000
    for select_target in farmerList: 
        i=0
        for target in data_main['Target']:
            if (data_main['id'].iloc[[i]].item() in farmer_ID_List and target==select_target):
                # place input 
                Input_place1 = str(user_PinCode)+" India "+data_main['City'].loc[[i]].item()
                Input_place2 = str(data_main['PinCode'].loc[[i]].item())+" India"

                # Get location of the input strings 
                place1 = geolocator.geocode(Input_place1) 
                place2 = geolocator.geocode(Input_place2)
                
                # Get latitude and longitude 
                Loc1_lat, Loc1_lon = (place1.latitude), (place1.longitude) 
                Loc2_lat, Loc2_lon = (place2.latitude), (place2.longitude) 

                location1 = (Loc1_lat, Loc1_lon) 
                location2 = (Loc2_lat, Loc2_lon) 
                
                # displsy the distance 
                Dist = distance.distance(location1, location2).km
                
                if(Dist<InDist):      
                    my_map2 = folium.Map(location = [Loc2_lat, Loc2_lon],zoom_start = 12) 
                    # CircleMarker with radius 
                    folium.CircleMarker(location = [Loc2_lat, Loc2_lon],radius = 50, popup = ' FRI ').add_to(my_map2) 
                    # save as html 
                    my_map2.save("templates/my_map.html") 
                    InDist = Dist

                list_farmers_obj.append(
                    farmer(
                        data_main['id'].loc[[i]].item(),
                        data_main['Name'].loc[[i]].item(),
                        data_main['Phone_Number'].loc[[i]].item(),
                        data_main['Item'].loc[[i]].item(),
                        data_main['Price_Organic'].loc[[i]].item(),
                        data_main['Price_Inorganic'].loc[[i]].item(),
                        data_main['Price'].loc[[i]].item()*quantity/100,
                        data_main['City'].loc[[i]].item(),
                        data_main['PinCode'].loc[[i]].item(),
                        data_main['Organic_Inorganic'].loc[[i]].item(),
                        data_main['Rating'].loc[[i]].item(),
                        data_main['Quantity'].loc[[i]].item(),
                        data_main['Availability'].loc[[i]].item(),
                        Dist
                        )
                )
                farmer_ID_List.remove(data_main['id'].iloc[[i]].item())
            i+=1
    if len(farmerList)==0 :
        print("currently no farmers available for this product")
    
    return list_farmers_obj

def get_location(request):
    return render(request,"my_map.html")
