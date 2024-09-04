import carla
import pygame
import random

# Function to handle keyboard input and convert it to vehicle controls
def process_input(keys):
    control = carla.VehicleControl()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        control.throttle = 1.0
    else:
        control.throttle = 0.0
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        control.brake = 1.0
    else:
        control.brake = 0.0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        control.steer = -1.0
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        control.steer = 1.0
    else:
        control.steer = 0.0
    return control

# Initialize Pygame
pygame.init()
size = (640, 480)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

try:
    # Connect to CARLA server
    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)  # Set timeout for 5 seconds

    # Load CARLA world and map
    world = client.get_world()
    map = world.get_map()

    # Get spawn points
    spawn_points = map.get_spawn_points()
    if not spawn_points:
        raise RuntimeError("No spawn points found")

    # Choose a random spawn point
    spawn_point = random.choice(spawn_points)

    # Get vehicle blueprint
    vehicle_bp = random.choice(world.get_blueprint_library().filter('vehicle.*'))
    if not vehicle_bp:
        raise RuntimeError("No vehicle blueprint found")

    # Spawn the vehicle
    vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
    if not vehicle:
        raise RuntimeError("Failed to spawn vehicle")

    print("Vehicle spawned successfully")
    print("Vehicle Location:", vehicle.get_location())

    # Add camera attached to the vehicle
    camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
    camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))  # Adjust the position of the camera relative to the vehicle
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

    # Main simulation loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Get keyboard input
        keys = pygame.key.get_pressed()

        # Process input and get vehicle controls
        control = process_input(keys)

        # Apply controls to the vehicle
        vehicle.apply_control(control)

        # Get camera location relative to the vehicle
        camera_location = camera.get_location()
        camera_x, camera_y = int(camera_location.x), int(camera_location.y)

        # Center the Pygame window around the camera location
        pygame.display.set_caption("Camera Location: ({}, {})".format(camera_x, camera_y))
        screen.fill((0, 0, 0))
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

except Exception as e:
    print("An error occurred:", e)

finally:
    pygame.quit()
    if vehicle is not None:
        vehicle.destroy()
    if camera is not None:
        camera.destroy()
