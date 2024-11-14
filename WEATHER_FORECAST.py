# Importing the required modules
import requests
from tkinter import *
from tkintermapview import TkinterMapView
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk, ImageSequence
from moviepy.editor import VideoFileClip
from opencage.geocoder import OpenCageGeocode
import pyttsx3

# Create a root window
root  = Tk()

# Function to play video and then show the second page
def playVideo(videoPath):
    # Load the video file
    video_clip = VideoFileClip(videoPath)
    clip1 = video_clip.resize(0.8)
    # Play the video 
    clip1.preview()

    # Close the video clip
    clip1.close()

# Call the function to play the video
playVideo(r"C:\Users\intel\Downloads\Your paragraph text (2).mp4")

# Set the title of the window
root.title("WEATHER APP")

# setting an icon 
root.iconbitmap("Weather-icon.ico")

# Set background image
imagePath = PhotoImage(file=r"C:\Users\intel\Downloads\image.png")
image1 = Label(root, image=imagePath)
image1.place(relheight=1, relwidth=1)

# Add a title label
titleLabel = Label(root, text="LET'S KNOW THE WEATHER", font=("Arial", 50), bg="yellow")
titleLabel.pack(padx=50, pady=270)

# Reverse the date function
def reverseDate(date) :
    date_parts = date.split("-")
    return "-".join(reversed(date_parts))

# Get the current date, time, and day
now = datetime.now()
dt_string = now.strftime("%d - %m - %Y")
time = now.strftime("%H:%M:%S")
day = now.strftime("%A")

# Display date, time, and day
DateLabel = Label(root, text=f"{dt_string}", font=("Helvetica", 20), fg="white", bg="black")
DateLabel.place(x=1300, y=100)

timeLabel = Label(root, text=f"{time}", font=("Helvetica", 20), fg="white", bg="black")
timeLabel.place(x=1300, y=140)

dayLabel = Label(root, text=f"{day}", font=("Helvetica", 20), fg="white", bg="black")
dayLabel.place(x=1300, y=180)


# Function to get data from API
def getWeather(cityName) :
    try :
                
        # url - for getting the current weather forecast 
        baseUrl = "http://api.openweathermap.org/data/2.5/weather?"
        apiKey = "51d3896b7013940aa5bc057df051cd5b"
        api1 = baseUrl + "&units=metric" + "&appid=" + apiKey + "&q=" + cityName
        # print(api1)
                    
        # getting data from the api
        data1= requests.get(api1).json()
            
        cityCode = data1['id']
            
        # getting the longitude and latitude of the city
        latitude = data1['coord']['lat']
        longitude = data1['coord']['lon']
            
        # url - for getting the 3 hour forecast of 5 days  
        api2 = f"http://api.openweathermap.org/data/2.5/forecast?id={cityCode}&appid={apiKey}&units=metric"
                    
        # getting data from the api
        # print(api2)
        response = requests.get(api2)
        data2 = response.json()
            # print(data2)
        dataList = []
        for index in range(0,40) :
            date_time,temp,description =  threeHrWeather(data2,index)
            dataList.append([date_time,temp,description])
            # print(dataList)
            
        # temperature
        temp = data1['main']['temp']
            
        # humidity
        humidity = data1['main']['humidity']
            
        # pressure
        pressure = data1['main']['pressure']
            
        # windspeed
        wind = data1['wind']['speed']
            
        # description
        description  = data1['weather'][0]['description']
            
        return [temp,humidity,pressure,wind,description,dataList,latitude,longitude]
                            
    except requests.exceptions.RequestException :
        # Create a message box with an "OK" button
        messagebox.showerror("ERROR", "Network Error: Please check your internet connection.")

        # Close the root window
        root.destroy()
            
    except KeyError :
        return 
        
# Getting the 3 hr weather forecast for 5 days
def threeHrWeather(data,index) :
    # date and time
    date_time =  data['list'][index]['dt_txt']
            
    # temperature
    temp = data['list'][index]['main']['temp']
    
    # Description
    description = data['list'][index]['weather'][0]['description']
            
    return [date_time,temp,description]

# Function to show the main page content
def showMainPage():
    # Hide second page widgets
    for widget in root.winfo_children():
        widget.pack_forget()
        widget.place_forget()
    
    # Set background image
    image1.place(relheight=1, relwidth=1)

    # Add a title label
    titleLabel.pack(padx=50, pady=270)

    # Display date, time, and day
    DateLabel.place(x=1300, y=100)
    timeLabel.place(x=1300, y=140)
    dayLabel.place(x=1300, y=180)

    # Create the main page buttons
    startButton.place(relx=0.45, rely=0.75, anchor=E)
    closeButton.place(relx=0.5, rely=0.9, anchor=CENTER)
    tourButton.place(relx=0.55, rely=0.75, anchor=W)
    

# Function to show the second page content
def showSecondPage():
    
    # Hide previous page widgets
    for widget in root.winfo_children():
        widget.pack_forget()
        widget.place_forget()
    
    # Load the GIF and start the animation
    gif_path = r"C:\Users\intel\Downloads\MKjwbG.gif"
    
    #  uses the PIL (Pillow) library to open the GIF file.
    gif_image = Image.open(gif_path)
    
    # Prepare Frames for Animation
    frames = [ImageTk.PhotoImage(frame.resize((root.winfo_screenwidth(), root.winfo_screenheight()))) for frame in ImageSequence.Iterator(gif_image)]
    
    # Label to  display the GIF frames.
    label = Label(root)
    label.place(relheight=1, relwidth=1)


    def update_frame(ind):
        if label.winfo_exists():
            frame = frames[ind]
            ind += 1
            if ind == len(frames):
                ind = 0
            label.configure(image=frame)
        root.after(gif_image.info['duration'], update_frame, ind)
        
    update_frame(0)
    
    cityLabel = Label(root, text='Enter your city name', font=('arial', 20, 'bold'), bg="#57adff")
    cityLabel.place(relx = 0.5,rely=0.45,anchor = CENTER)

    # Entry for city name
    questionField = Entry(root, width=45, font=('arial', 14, 'bold'), bd=4, relief=SUNKEN)
    questionField.place(relx = 0.5,rely = 0.55,anchor=CENTER)        

    # Function for search button
    def search():
        cityName = questionField.get()
        data = getWeather(cityName)
                
        if data:
            showThirdPage(data,cityName)
           
        else : 
            # Create a message box with an "OK" button
            messagebox.showerror("ERROR", "City not found.")
            
            # Close the root window
            root.destroy()
            
    # Creating a Search button
    searchButton = Button(root, text="Search",font = ("Arial",15) ,command=lambda: search(),bg = "Lightblue")
    searchButton.place(relx = 0.8,rely = 0.55,anchor = CENTER)
    
    # Creating a Back button to return to main page
    backButton = Button(root, text="Back", font=("Arial", 15), command=showMainPage, bg="lightblue")
    backButton.place(relx=0.1, rely=0.9, anchor=CENTER)
    
    
    # Set the window to fullscreen
    root.attributes('-fullscreen', True)  
    
#  Function to show the thrid page content
def showThirdPage(data,cityName):
    # Hide second page widgets
    for widget in root.winfo_children():
        widget.pack_forget()
        widget.place_forget()
    
    mapWidget = TkinterMapView(root, width=800, height=600, corner_radius=0)
    mapWidget.pack(fill="both", expand=True)

    lat = data[6]
    lng = data[7]
    
    # google maps server
    mapWidget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=10)
    mapWidget.set_position(lat, lng)
    mapWidget.set_marker(lat, lng,text = cityName.upper())
    
    root.after(13000,lambda : displayInfo())
    
    def displayInfo() :
        # Create frame for displaying the current weather forecast
        frame = Frame(root, bd=5, bg='#57adff', highlightbackground='dark gray', highlightthickness=2)
        frame.place(x=850, y=250, width=250, height=250)

        # Temperature
        tempLabel = Label(root, text=f"Temperature : {data[0]} °C", font=("Helvetic", 12), fg="white", bg='black')
        tempLabel.place(x=870, y=280)

        # Humidity
        humidityLabel = Label(root, text=f"Humidity : {data[1]} %", font=("Helvetic", 12), fg="white", bg='black')
        humidityLabel.place(x=870, y=310)
            
        # Pressure
        pressureLabel = Label(root, text=f"Pressure : {data[2]} hPa", font=("Helvetic", 12), fg="white", bg='black')
        pressureLabel.place(x=870, y=340)

        # Wind Speed
        windLabel = Label(root, text=f"Wind speed : {data[3]} m/s", font=("Helvetic", 12), fg="white", bg='black')
        windLabel.place(x=870, y=370)

        # Description
        descriptionLabel = Label(root, text=f"Description : {data[4]}", font=("Helvetic", 12), fg="white", bg='black')
        descriptionLabel.place(x=870, y=400)

        # Back button
        backButton = Button(root, text="Back", font=("Arial", 15), command=showSecondPage, bg="lightblue")
        backButton.place(x=10, y=800)

        # initializing the index number
        index = 0
        y_co = 25
        
        # Creating and displaying the frames for 3 hr forecast of 5 days
        for day in range(1, 6):
            # Day
            frame_day = Frame(root, bd=2, bg="yellow", highlightbackground='dark gray', highlightthickness=2)
            frame_day.place(x=500 + (day - 1) * 140, y=575, width=130, height=200)

            date = reverseDate(data[5][index][0][:10])

            dateLabel = Label(root, text=f"{date}", font=("Helvetica", 11), bg="Yellow")
            dateLabel.place(x=510 + (day - 1) * 140, y=580)

            y_co = 25
            index += 1

            while data[5][index][0][11:] != "00:00:00":
                temperature = Label(root, text=f"{data[5][index][0][11:16]} - {data[5][index][1]} °C", font=("Helvetica", 11), bg="Yellow")
                temperature.place(x=510 + (day - 1) * 140, y=575 + y_co)
                index += 1
                y_co += 20
    
        root.after(1000,lambda : voice())
        def voice() :
            engine = pyttsx3.init()
            temp = data[0]
            humidity = data[1]
            pressure = data[2]
            wind = data[3]
            description = data[4]
            str = f"The weather forecast for {cityName}. The temperature is {temp} degree Celsius. The humidity is {humidity} percent. The pressure is {pressure} hpa. The wind speed is {wind} meters per second. The weather description is {description}."
            engine.say(str)
            engine.runAndWait()    
    
                
OPENCAGE_API_KEY = "cf5a4659f50b4baebe395893af835dcc"
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

def reverse_geocode(lat, lng):
    result = geocoder.reverse_geocode(lat, lng)
    if result and len(result):
        # Extract the formatted address
        address = result[0]['components']['state']
        
        return address
        
    return "Unknown location"

# # Function to remove all spaces from a given string
# def removeSpaces(string):
#     string = string.replace(' ','')
#     return string

# Function for plan a tour
def tourPlanner() :
    # Hide previous page widgets
    for widget in root.winfo_children():
        widget.pack_forget()
        widget.place_forget()
        
    # Set background image
    imagePath3 = PhotoImage(file="C:\\Users\\intel\\Downloads\\background2.png")
    image3 = Label(root, image=imagePath3)
    image3.place(relheight=1, relwidth=1)
    image3.image = imagePath3  # Keep a reference to avoid garbage collection


    # Add labels and entry widgets for source and destination
    sourceLabel = Label(root, text='Enter source city name:', font=('arial', 20, 'bold'), bg="#57adff")
    sourceLabel.place(relx=0.5, rely=0.3, anchor=CENTER)

    source = Entry(root, width=45, font=('arial', 14, 'bold'), bd=4, relief=SUNKEN)
    source.place(relx=0.5, rely=0.4, anchor=CENTER)

    destinationLabel = Label(root, text='Enter destination city name:', font=('arial', 20, 'bold'), bg="#57adff")
    destinationLabel.place(relx=0.5, rely=0.5, anchor=CENTER)

    destination = Entry(root, width=45, font=('arial', 14, 'bold'), bd=4, relief=SUNKEN)
    destination.place(relx=0.5, rely=0.6, anchor=CENTER)
    
    # Function to get data from the getweather function
    def planRoute():
        sourceCity = source.get()
        destinationCity = destination.get()
        
        sourceData = getWeather(sourceCity)
        destinationData = getWeather(destinationCity)
        
        if sourceData and destinationData :
            showRoutePage(sourceCity, sourceData, destinationCity, destinationData)

    # Create the plan button
    planButton = Button(root, text="Plan", font=("Arial", 15), command=planRoute, bg="Lightblue")
    planButton.place(relx=0.5, rely=0.7, anchor=CENTER)

    # Create the back button
    backButton = Button(root, text="Back", font=("Arial", 15), command=showMainPage, bg="lightblue")
    backButton.place(relx=0.1, rely=0.9, anchor=W)

# Function to check route weather and travel suitability
def getRouteWeather(source, states, destination):
    states.append(source)
    states.append(destination)
    unsuitable_conditions = ["thunderstrom","shower rain","thunderstorm with heavy rain","heavy thunderstorm","heavy intensity rain","very heavy rain","heavy intensity shower rain","heavy snow","heavy shower snow","rain and snow","tornado",]
    # unsuitable_conditions = ["thunderstrom","snow","rain","shower rain","thunderstorm with heavy rain","heavy thunderstorm","heavy intensity rain","very heavy rain","heavy intensity shower rain","heavy snow","heavy shower snow","rain and snow","tornado",]
    travelSuitability = True
    for state in states:
        # stateName = removeSpaces(state)
        data = getWeather(state)
        if data :
            for index in range(0, 40):
                description = data[5][index][2]
                # temp = data[5][index][1] 
                if any(condition in description.lower() for condition in unsuitable_conditions):
                    travelSuitability = False
                    reason = description
                    break
                
                # if temp > 50 or temp < -20:
                #     travelSuitability = False
                #     break
        if travelSuitability == False:
            # Show error message and return to main page
            messagebox.showerror("Error", f"It is not suitable to travel through {state} because of {reason}.")
            engine = pyttsx3.init()
            engine.say("Hey there!! we see that u cannot travel.OOps!! sorry for that but your safety is our priority ")
            engine.runAndWait()
            break
            
    
    # If all states have suitable weather conditions, Show success message 
    if travelSuitability == True:     
        messagebox.showinfo("Success", "It is suitable to travel.")
        engine = pyttsx3.init()
        engine.say("Hey there!! we see that u can travel.Have a safe trip!!")
        engine.runAndWait() 

    # showMainPage()
    
# Function to display the route page
def showRoutePage(sourceCity, sourceData, destinationCity, destinationData):
    # Hide previous page widgets
    for widget in root.winfo_children():
        widget.pack_forget()
        widget.place_forget()
    
    mapWidget = TkinterMapView(root, width=800, height=600, corner_radius=0)
    mapWidget.pack(fill="both", expand=True)

    sourceLat = sourceData[6]
    sourceLng = sourceData[7]
    destLat = destinationData[6]
    destLng = destinationData[7]

    # Google maps server
    mapWidget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=25)
    mapWidget.set_position((sourceLat + destLat) / 2, (sourceLng + destLng) / 2)
    mapWidget.set_marker(sourceLat, sourceLng, text=sourceCity.upper())
    mapWidget.set_marker(destLat, destLng, text=destinationCity.upper())
    # mapWidget.set_path([(sourceLat, sourceLng), (destLat, destLng)])
    
    # Back button
    backButton = Button(root, text="Back", font=("Arial", 15), command=tourPlanner, bg="lightblue")
    backButton.place(x=10, y=800)
    
    # Function to calculate intermediate points
    def get_intermediate_points(coord1, coord2, num_points):
        # Calculate intermediate points
        intermediate_points = []
        for i in range(1, num_points + 1):
            lat = coord1[0] + (coord2[0] - coord1[0]) * i / (num_points + 1)
            lng = coord1[1] + (coord2[1] - coord1[1]) * i / (num_points + 1)
            intermediate_points.append((lat, lng))
            
        return intermediate_points

    # Calculate and display intermediate points
    intermediate_points = get_intermediate_points((sourceLat, sourceLng), (destLat, destLng), 5)
    all_points = [(sourceLat, sourceLng)] + intermediate_points + [(destLat, destLng)]
    states = []
    if intermediate_points:
        for point in intermediate_points:
            address = reverse_geocode(point[0], point[1])
            if address not in states:
                mapWidget.set_marker(point[0], point[1],text=address)
                states.append(address)
                
    # Set the path
    mapWidget.set_path(all_points)
    
    # Set the window to fullscreen
    root.attributes('-fullscreen', True)
    
    getRouteWeather(sourceCity,states,destinationCity)

  
# Create the main page buttons
startButton = Button(root, text="FORECAST", font=("Arial", 25), width=15, height=1, fg="green", bg="lightgreen", command=showSecondPage)
startButton.place(relx=0.45, rely=0.75, anchor=E)

closeButton = Button(root, text="CLOSE", font=("Arial", 25), width=15, height=1, fg="red", bg="pink", command=root.destroy)
closeButton.place(relx=0.5, rely=0.9, anchor=CENTER)

tourButton = Button(root,text = "PLAN A TOUR",font = ("Arial",25),width = 15,height = 1,fg = "blue",bg = "#57adff",command = tourPlanner)
tourButton.place(relx =0.55,rely = 0.75,anchor=W )

# Set the window to fullscreen
root.attributes('-fullscreen', True)

# Start the Tkinter event loop
root.mainloop()
