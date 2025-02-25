from dotenv import load_dotenv
from sscws.sscws import SscWs
import requests
import json
import os

# Load environment variables from the .env file
load_dotenv()

# Access environment variables
API_KEY = os.getenv('API_KEY')

# The Base Url for the API enteries 
BASE_URL = "https://api.nasa.gov"

# Gets NASA's Astronomy Picture of the Day
def fetch_apod():
    url = f"{BASE_URL}/planetary/apod?api_key={API_KEY}"
    response = requests.get(url).json()

    print("Astronomy Picture of the Day:")
    print("Title:", response.get("title"))
    print("Explanation:", response.get("explanation"))
    print("URL:", response.get("url"))

# Gets Mars Rover's Photos from a set day
def fetch_mars_rover_photos():
    date = input("Enter Earth date (YYYY-MM-DD) for Mars rover photos: ")
    url = f"{BASE_URL}/mars-photos/api/v1/rovers/curiosity/photos?earth_date={date}&api_key={API_KEY}"
    response = requests.get(url).json()
    photos = response.get("photos", [])
    limit = input("How many photos would you like to view?: ")
    try:
        limit = int(limit)
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        return

    print(f"Found {len(photos)} photos.")
    for photo in photos[:limit]: 
        print(photo["img_src"])

# Gets a image of the earth from a setish day, at a set longitude and latitude.
def fetch_earth_imagery():
    lat = input("Enter latitude: ")
    lon = input("Enter longitude: ")
    dim = input("Enter width and height of image in degrees (between 1 and 0) that you want the image:")
    date = input("Enter date (YYYY-MM-DD): ")

    url = f"https://api.nasa.gov/planetary/earth/imagery?lon={lon}&lat={lat}&date={date}&dim={dim}&api_key={API_KEY}"

    print("Earth Imagery URL:", url)

# Gets near Earth Objects on a set day
def fetch_neo_ws():
    start_date = input("Enter start date (YYYY-MM-DD) for asteroid data: ")
    end_date = input("Enter end date (YYYY-MM-DD) for asteroid data: ")
    url = f"{BASE_URL}/neo/rest/v1/feed?start_date={start_date}&start_date={end_date}&api_key={API_KEY}"
    response = requests.get(url).json()
    neos = response.get("near_earth_objects", {}).get(start_date, [])    
    limit = input("How many NEOs would you like to view?: ")
    try:
        limit = int(limit)
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        return

    print(f"Found {len(neos)} asteroids.")
    for neo in neos[:limit]:
        print("Name:", neo["name"])
        print("Magnitude:", neo["absolute_magnitude_h"])

# Gets a set satelite location data
def fetch_satellite_location():
    # I got my base version of this from: https://sscweb.gsfc.nasa.gov/WS/sscr/2/observatories/iss/clientLibraryExample/

    ssc = SscWs()

    # Gets which satellite the user wants to view
    try:   
        object = input("Which satelite would you like to see:")

        #  Change the following time_interval value to suit your needs.
        time_interval = ssc.get_example_time_interval(object)
        result = ssc.get_locations([object], time_interval)
        data = result['Data'][0]
        coords = data['Coordinates'][0]
        print(coords['X'])

    # Makes sure the satellite is in the nasa db
    except Exception:
        print("Satellite not found in the database!")
        return

    try:
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from packaging import version
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlabel('X (km)')
        ax.set_ylabel('Y (km)')
        ax.set_zlabel('Z (km)')
        title = data['Id'] + ' Orbit (' + coords['CoordinateSystem'].value.upper() + ')'
        ax.plot(coords['X'], coords['Y'], coords['Z'], label=title)
        ax.legend()
        plt.show()
    except ImportError:
        print('To see the plot, do')
        print('pip install packaging matplotlib')
    except Exception as e:
        print(e)

# Gets a set number of The Earth Observatory Natural Event Tracker most recent open events.
def fetch_eonet_events():    
    
    url = f"https://eonet.gsfc.nasa.gov/api/v3/events"
    response = requests.get(url).json()
    limit = input("How many most recent open events would you like to view?: ")
    try:
        limit = int(limit)
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        return

    for event in response.get("events", [])[:limit]:
        print("Event:", event.get("title"), "\nCategorie: ", event.get("categories", [{}])[0].get("title", "No title available"), "\nLink: ", event.get("link"), "\n\n")

# Gets The Space Weather Database Of Notifications, Knowledge, Information
def fetch_donki():
    url = f"{BASE_URL}/DONKI/notifications?api_key={API_KEY}"
    response = requests.get(url).json()

    for notification in response[:5]:
        print("Type:", notification.get("messageType"))
        print("Message:", notification.get("messageBody"))

# The main function
def main():
    while True:
        print("\nNASA API Console Application")
        print("1. Astronomy Picture of the Day")
        print("2. Mars Rover Photos")
        print("3. Earth Imagery")
        print("4. Near-Earth Objects (Asteroids)")
        print("5. Satellite Situation Center")
        print("6. EONET Natural Events")
        print("7. DONKI Space Weather Notifications")
        print("8. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            fetch_apod()
        elif choice == "2":
            fetch_mars_rover_photos()
        elif choice == "3":
            fetch_earth_imagery()
        elif choice == "4":
            fetch_neo_ws()
        elif choice == "5":
            fetch_satellite_location()
        elif choice == "6":
            fetch_eonet_events()
        elif choice == "7":
            fetch_donki()
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
