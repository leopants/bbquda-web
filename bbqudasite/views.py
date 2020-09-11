from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import pandas as pd
import os

# Create your views here.

#Currently playing with the latitude paramter to make sure i can read a csv file properly
def index(request):
    mission_file = open('20190611_103011_greg_map_loc_surface_modified_IVER2-218.csv')
    df = pd.read_csv(mission_file)
    latitude = df['Latitude']
    print(latitude[0])
    context = {'latitude': latitude}
    #return HttpResponse(latitude)
    return render(request, 'index.html', context)

#function for removing outliers
def clean(csv_file):
    return

def formhtml(request):
    #user just landed for the first time so show them the upload html
    if request.method == "GET":
        return render(request, 'form.html')
    
    #in the html called the uploaded file 'file'
    csv_file = request.FILES['file']

    #if the input is a log file then change it to a csv file extension
    if csv_file.name.endswith('.log'):
        name, csv_data = convert_to_csv(csv_file)
        print("----------------------------------------")
        print(name)
        with open(name + ".csv", "w") as csv_file:
            csv_file.write(csv_data)
        #need to get the name when the file is called
        #have to get a way to convert this csv_file into an actual file
        #it isnt csv file yet just like a giant string 

    #if its not a csv by now then it was neither a csv or log to begin with so error
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Please provide a csv file')
    
    #pandas processing to extract parameters
    df = pd.read_csv(csv_file)
    filtered_list = df[['Latitude', 'Longitude', 'Total Water Column (m)',
            'Temperature (c)', 'pH', 'ODO mg/L', 'Salinity (ppt)',
            'Turbid+ NTU', 'BGA-PC cells/mL']]
    print(filtered_list) #just a check
    latitude = filtered_list['Latitude']
    return HttpResponse(latitude[0])

#work in progress to convert log to csv
def convert_to_csv(log_file):
    fileName = str(log_file.name)
    pre = os.path.splitext(fileName)[0]
    print(pre)
    df = pd.read_csv(log_file ,delimiter=';')
    csv_file_out = df.to_csv()
    return pre, csv_file_out
    
