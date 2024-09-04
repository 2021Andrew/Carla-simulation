import carla
import random
import time

def connect_to_carla():
    try:
        print("Connecting to CARLA server...")
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        print("Connected to CARLA server.")
        return client
    except Exception as e:
        print("Error connecting to CARLA server:", e)
        return None

def get_carla_world(client):
    try:
        print("Getting world...")
        world = client.get_world()
        print("Got world successfully.")
        return world
    except Exception as e:
        print("Error getting world:", e)
        return None

# Function to change weather
def change_weather(world):
    try:
        weather = carla.WeatherParameters()
        weather.cloudiness = random.uniform(0, 100)
        weather.precipitation = random.uniform(0, 100)
        weather.precipitation_deposits = random.uniform(0, 100)
        weather.wind_intensity = random.uniform(0, 100)
        weather.sun_azimuth_angle = random.uniform(0, 360)
        weather.sun_altitude_angle = random.uniform(0, 90)
        weather.fog_density = random.uniform(0, 100)
        weather.fog_distance = random.uniform(0, 100)
        weather.wetness = random.uniform(0, 100)
        weather.road_wetness = random.uniform(0, 100)
        weather.dust_density = random.uniform(0, 100)
        
        world.set_weather(weather)
        print("Weather changed successfully.")
    except Exception as e:
        print("Error changing weather:", e)
# Main function
def main():
    # Connect to CARLA server
    client = connect_to_carla()
    if not client:
        return

    # Wait for the world to be ready
    time.sleep(5)  # Wait for 5 seconds

    # Get the world
    world = get_carla_world(client)
    if not world:
        return

    # Main loop
    try:
        while True:
            change_weather(world)
            time.sleep(10)  # Change weather every 10 seconds
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing connection to CARLA server...")
        client.disconnect()

if __name__ == "__main__":
    main()
