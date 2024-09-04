import carla
import time

# Function to control the vehicle
def control_vehicle(vehicle):
    # Set control values
    control = carla.VehicleControl()
    control.throttle = 0.5  # 0 to 1 for forward throttle
    control.steer = 0.0  # -1 to 1 for left and right steering
    control.brake = 0.0  # 0 to 1 for braking
    control.reverse = False  # True to set reverse gear
    vehicle.apply_control(control)

try:
    # Connect to the CARLA server
    print("Connecting to CARLA server...")
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)  # Increase timeout to 10 seconds
    print("Connected to CARLA server.")

    # Get the world
    print("Retrieving the world...")
    world = client.get_world()
    print("Retrieved the world successfully.")

    # Get the blueprint library
    blueprint_library = world.get_blueprint_library()

    # Get the vehicle blueprint for a specific vehicle (e.g., Tesla Model3)
    vehicle_bp = blueprint_library.find('vehicle.tesla.model3')

    # Specify the spawn point
    spawn_point = carla.Transform(carla.Location(x=230, y=128, z=3))

    # Spawn the vehicle
    vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)

    if vehicle is not None:
        print("Spawned vehicle:", vehicle.id)

        # Set the vehicle as the spectator
        world.get_spectator().set_transform(vehicle.get_transform())

        # Control the vehicle
        control_vehicle(vehicle)

        # Wait for a few seconds
        time.sleep(5)

    else:
        print("Failed to spawn vehicle.")

except Exception as e:
    print("Error:", e)
