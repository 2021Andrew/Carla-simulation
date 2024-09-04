import carla
import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()
size = (800, 600)
pygame.display.set_caption("CARLA Manual Control")
screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

# Connect to CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Load the world and get the map
world = client.get_world()
map = world.get_map()

# Set weather parameters
weather = carla.WeatherParameters(
    cloudiness=0.0,
    precipitation=0.0,
    sun_altitude_angle=10.0,
    sun_azimuth_angle=70.0,
    precipitation_deposits=0.0,
    wind_intensity=0.0,
    fog_density=0.0,
    wetness=0.0,
)
world.set_weather(weather)

# Get blueprint library and spawn points
bp_lib = world.get_blueprint_library()
spawn_points = map.get_spawn_points()

# Spawn a vehicle
vehicle_bp = bp_lib.filter('vehicle.audi.etron')[0]
spawn_point = random.choice(spawn_points)
vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)

# Set up the camera
camera_bp = bp_lib.find('sensor.camera.rgb')
camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
camera.listen(lambda data: process_image(data))  # Register the callback function

# Function to handle keyboard input and convert it to vehicle controls
def process_input(keys):
    control = carla.VehicleControl()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        control.throttle = 1.0
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        control.brake = 1.0
    else:
        control.throttle = 0.0
        control.brake = 0.0

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        control.steer = -1.0
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        control.steer = 1.0
    else:
        control.steer = 0.0

    return control

# Function to process the image data from the camera
image_data = None
def process_image(image):
    global image_data
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]  # Remove the alpha channel
    image_data = array

# Main simulation loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            vehicle.destroy()
            camera.destroy()
            exit()

    # Get keyboard input
    keys = pygame.key.get_pressed()

    # Process input and get vehicle controls
    control = process_input(keys)

    # Apply controls to the vehicle
    vehicle.apply_control(control)

    # Tick the CARLA world
    world.tick()

    # Render the camera view
    if image_data is not None:
        image_surface = pygame.surfarray.make_surface(image_data.swapaxes(0, 1))
        screen.blit(image_surface, (0, 0))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)