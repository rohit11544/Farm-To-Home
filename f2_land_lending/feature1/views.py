from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.db import connection
import pandas as pd 
import numpy as np
from .models import land
from .models import city
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
engine = sqlalchemy.create_engine('mysql+pymysql://root:7337007435@localhost:3306/land2')

# code for forms
from .forms import SearchLand,Registration,GetDetails,ChangePassword,FinalUpdateDetails


def customer(request):
    fm = SearchLand()
    return render(request,'customer.html',{'form':fm,'name1': 'Search Your Land','name2':'Details'})

def owner_registration(request):
    fm = Registration
    return render(request,"owner.html",{'form':fm,'name1':'Owner Information','name2': 'Registration'})

def redirect_to_update(request):
    fm = GetDetails()
    return render(request,"update_owner.html",{'form':fm,'name1':'Updating Owner','name2': 'Updating'})

def index(request):
    return render(request,"index.html")

def home(request):
    return render(request,'index.html')

# making connection with mysql connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="7337007435",
  database="land2",
  auth_plugin = 'mysql_native_password',
)
mycursor = mydb.cursor()

query = str(city.objects.all().query)
cities_df = pd.read_sql_query(query, connection)



def join_owner(request):
    query = str(land.objects.all().query)
    data_main = pd.read_sql_query(query, connection)
    if request.POST.get('Password')==request.POST.get('ConformPassword'):
        if request.method=='POST':
            servercord = land()
            servercord.id = len(data_main.index) + 1
            servercord.Name = request.POST.get('Name')
            servercord.Phone_Number = request.POST.get('Phone_Number')
            ErrorCheck = 0
            for i in range(40):
                if (cities_df['City'].loc[[i]].item()==request.POST.get('City')):
                    servercord.City = request.POST.get('City')
                    ErrorCheck = 1
                    break
            if ErrorCheck == 0:
                fm1 = Registration()
                return render(request,"owner.html",{'form':fm1,'name1':'INCORRECT Details please enter correctly','name2': 'Registration'})
            
            servercord.Pin_Code = request.POST.get('Pin_Code')
            servercord.Acres = request.POST.get('Acres')
            servercord.Rent = request.POST.get('Rent')
            servercord.Share = request.POST.get('Share')
            servercord.R_or_S = request.POST.get('R_or_S')
            servercord.Availability = request.POST.get('Availability')
            servercord.Target = 0
            servercord.UserName = request.POST.get('UserName')
            servercord.Password = request.POST.get('Password')
            servercord.Pin_Code = request.POST.get('PinCode')
            servercord.save()
            messages.success(request,'Record saved successfully...!')
            return render(request,'owner_output.html',{'name1': 'You have joined Successfully','name2':'All the best!'})
    fm2 = Registration
    return render(request,"owner.html",{'form':fm2,'name1':'Owner Information','name2': 'Registration'})

def update_owner(request):
    if request.POST.get('FP'):
        fm = ChangePassword()
        return render(request,"forgot_password.html",{'form':fm})

    query = str(land.objects.all().query)
    data_main = pd.read_sql_query(query, connection)

    i = int(request.POST.get('GivenUserNum')) - 1
    landList = []
    if((int(request.POST.get('Password'))==data_main['Password'].loc[[i]].item() and request.POST.get('UserName'))==data_main['UserName'].loc[[i]].item()):
        landList.append(
                        land(
                            data_main['id'].loc[[i]].item(),
                            data_main['Name'].loc[[i]].item(),
                            data_main['Phone_Number'].loc[[i]].item(),
                            data_main['City'].loc[[i]].item(),
                            data_main['Pin_Code'].loc[[i]].item(),
                            data_main['Acres'].loc[[i]].item(),
                            data_main['Rent'].loc[[i]].item(),
                            data_main['Share'].loc[[i]].item(),
                            data_main['R_or_S'].loc[[i]].item(),
                            data_main['Availability'].loc[[i]].item(),
                            data_main['Target'].loc[[i]].item(),
                            data_main['UserName'].loc[[i]].item(),
                            data_main['Password'].loc[[i]].item()
                            )
                    )
        fm3 = FinalUpdateDetails()
        return render(request,"print_details.html",{'form':fm3,'lands': landList,'name1':'Updating Owner','name2':'Updating...'})
    fm2 = GetDetails()
    return render(request,"update_owner.html",{'form':fm2,'name1':'UserName or Password INCORRECT','name2': 'Updating'})

def forgot_password(request):
    i = int(request.POST.get('GivenUserNum')) - 1
    query = str(land.objects.all().query)
    data_main = pd.read_sql_query(query, connection)
    
    if data_main['Name'].loc[[i]].item() == request.POST.get('Name'): 
        if data_main['City'].loc[[i]].item() == request.POST.get('City'):
            if int(request.POST.get('Password')) == int(request.POST.get('ConformPassword')):
                data_main.at[i, "Password"] = int(request.POST.get('ConformPassword'))
                sql = "DROP TABLE IF EXISTS feature1_land"
                mycursor.execute(sql)
                data_main.to_sql(name='feature1_land',con=engine,index=False)
                return render(request,"forgot_password_output.html",{'name1':'Password Changed!'})
    fm = ChangePassword()
    return render(request,"forgot_password.html",{'form':fm,'name1':'INCORRECT details','name2':'enter details'})

def update_owner_info(request):
    query = str(land.objects.all().query)
    data_main = pd.read_sql_query(query, connection)
    i = int(request.POST.get('GivenUserNum')) - 1
    data_main.at[i, "Name"] = request.POST.get('Name')
    data_main.at[i, "Phone_Number"] = int(request.POST.get('Phone_Number'))
    data_main.at[i, "City"] = request.POST.get('City')
    data_main.at[i, "Pin_Code"] = int(request.POST.get('PinCode'))
    data_main.at[i, "Acres"] = int(request.POST.get('Acres'))
    data_main.at[i, "Rent"] = int(request.POST.get('Rent'))
    data_main.at[i, "Share"] = int(request.POST.get('Share'))
    data_main.at[i, "R_or_S"] = int(request.POST.get('R_or_S'))
    data_main.at[i, "Availability"] = int(request.POST.get('Availability'))

    sql = "DROP TABLE IF EXISTS feature1_land"
    mycursor.execute(sql)
    data_main.to_sql(name='feature1_land',con=engine,index=False)

    landList = []
    landList.append(
                    land(
                        data_main['id'].loc[[i]].item(),
                        data_main['Name'].loc[[i]].item(),
                        data_main['Phone_Number'].loc[[i]].item(),
                        data_main['City'].loc[[i]].item(),
                        data_main['Pin_Code'].loc[[i]].item(),
                        data_main['Acres'].loc[[i]].item(),
                        data_main['Rent'].loc[[i]].item(),
                        data_main['Share'].loc[[i]].item(),
                        data_main['R_or_S'].loc[[i]].item(),
                        data_main['Availability'].loc[[i]].item(),
                        data_main['Target'].loc[[i]].item()
                        )
                )
    return render(request,"update_output.html",{'lands': landList,'name1': 'DONE UPDATING','name2':'Updated your details successfully!!!'})




def search_land(request):
    # importing the tabels 
    query = str(land.objects.all().query)
    data_main = pd.read_sql_query(query, connection)
    data = pd.read_sql_query(query, connection)

    data.drop(['id','Name','Phone_Number','UserName','Password'],axis=1,inplace=True)
    
    # preprocessing the data
    data[['City']] = data[['City']].apply(lambda s: s.map({k:i for i,k in enumerate(s.unique())}))
    data_main['Target'] = data['R_or_S']*data['Rent'] + (1 - 1*data['R_or_S'] )*data['Share']
    data.drop(['Rent','Share','R_or_S'],axis=1,inplace=True)
    data['Target'] = round((data['Target']+data['City']+data['Pin_Code'])*data['Availability'])
    data_main['Target'] = data['Target']
    
    # remove extra spaces in city column
    i=0
    for city in data_main["City"]:
        data_main.at[i, "City"] = city.replace(" ", "")
        i+=1
    # training of the model
    X = data.drop(['Target'], axis=1)
    Y = pd.DataFrame(data['Target'])
    ln = linear_model.LinearRegression()
    model = ln.fit(X,Y)
    
    # taking input
    user_Town = request.POST.get('Town')
    user_Acres = int(request.POST.get('Acres'))
    user_Pin_Code = int(request.POST.get('PinCode'))
    
    # converting to numbers based on there index
    for i in range(40):
        if (cities_df['City'].loc[[i]].item()==user_Town):
            user_Town_index = cities_df['Index'].loc[[i]].item()
            break
    
    x = np.array([[user_Town_index,user_Pin_Code,user_Acres,1]])
    y = math.floor(model.predict(x))
    
    i=0
    ownerList = []
    owner_ID_List = []
    
    for target in data_main['Target']:
        town = data_main['City'].loc[[i]].item()
        if(target in range(y-300000,y+300000)):
            if(user_Town==town):
                ownerList.append(data_main['Target'].loc[[i]].item())
                owner_ID_List.append(data_main['id'].loc[[i]].item())
        i+=1
    ownerList.sort(reverse=True)
    list_land_obj = print_land(data_main,ownerList,owner_ID_List,user_Pin_Code)
    return render(request,"customer_output.html",{'lands': list_land_obj,'name1': 'Here are the best lands for your search!', 'name2': 'Lands!!' })

def print_land(data_main,ownerList,owner_ID_List,user_Pin_Code):
    list_land_obj = [] 
    InDist = 100000
    for select_target in ownerList: 
        i=0
        for target in data_main['Target']:
            if (data_main['id'].iloc[[i]].item() in owner_ID_List and target==select_target):
                
                # place input 
                Input_place1 = str(user_Pin_Code)+" India "+data_main['City'].loc[[i]].item()
                Input_place2 = str(data_main['Pin_Code'].loc[[i]].item())+" India"

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

                list_land_obj.append(
                    land(
                        data_main['id'].loc[[i]].item(),
                        data_main['Name'].loc[[i]].item(),
                        data_main['Phone_Number'].loc[[i]].item(),
                        data_main['City'].loc[[i]].item(),
                        data_main['Pin_Code'].loc[[i]].item(),
                        data_main['Acres'].loc[[i]].item(),
                        data_main['Rent'].loc[[i]].item(),
                        data_main['Share'].loc[[i]].item(),
                        data_main['R_or_S'].loc[[i]].item(),
                        data_main['Availability'].loc[[i]].item(),
                        Dist
                        )
                )
                owner_ID_List.remove(data_main['id'].iloc[[i]].item())
            i+=1
    if len(ownerList)==0 :
        print("currently no owners available for this search")
    
    return list_land_obj

def get_location(request):
    return render(request,"my_map.html")
