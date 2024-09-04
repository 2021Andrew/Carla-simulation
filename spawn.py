import carla
import time

# Connect to Carla server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

try:
    # Retrieve the world
    world = client.get_world()

    # Get the blueprint for the vehicle you want to spawn (e.g., Tesla Model 3)
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.find('vehicle.tesla.model3')

    # Set the spawn location
    spawn_location = carla.Transform(carla.Location(x=100, y=100, z=1), carla.Rotation())

    # Spawn the vehicle
    vehicle = world.try_spawn_actor(vehicle_bp, spawn_location)

    if vehicle is not None:
        print("Vehicle spawned successfully!")
        print("Vehicle ID:", vehicle.id)  # Print the ID of the spawned vehicle for reference
    else:
        print("Failed to spawn vehicle")

    try:
        # Get the vehicle's control
        control = carla.VehicleControl()

        while True:
            if vehicle is not None:
                # Control the vehicle (for example, make it accelerate)
                control.throttle = 0.5

                # Apply the control to the vehicle
                vehicle.apply_control(control)

                # Sleep for a short time to allow the vehicle to move
                time.sleep(0.1)
            else:
                print("Vehicle is None. Exiting simulation loop.")
                break

    finally:
        # Destroy the vehicle when done
        if vehicle is not None:
            vehicle.destroy()

finally:
    # Disconnect from the server
    client = None
