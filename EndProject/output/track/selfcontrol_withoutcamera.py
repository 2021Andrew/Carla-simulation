
import carla
import time
import numpy as np

# Function to control the vehicle
def control_vehicle(vehicle, world):
    # Get the current vehicle transform
    vehicle_transform = vehicle.get_transform()

    # Get the waypoints of the current lane
    waypoints = world.get_map().get_waypoint(vehicle_transform.location, project_to_road=True)
    next_waypoint = waypoints.next(2.0)[0]  # Get the next waypoint 2 meters ahead

    # Calculate the desired steering angle
    vehicle_location = vehicle_transform.location
    vehicle_yaw = vehicle_transform.rotation.yaw
    next_waypoint_location = next_waypoint.transform.location
    dx = next_waypoint_location.x - vehicle_location.x
    dy = next_waypoint_location.y - vehicle_location.y
    desired_yaw = np.arctan2(dy, dx) * 180 / np.pi
    steering_angle = desired_yaw - vehicle_yaw

    # Set control values
    control = carla.VehicleControl()
    control.throttle = 0.5  # 0 to 1 for forward throttle
    control.steer = np.clip(steering_angle / 25.0, -1.0, 1.0)  # Adjust steering angle
    control.brake = 0.0  # 0 to 1 for braking
    control.reverse = False  # True to set reverse gear
    vehicle.apply_control(control)

try:
    # Connect to the CARLA server
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    # Get the map and spawn points
    map = world.get_map()
    spawn_points = map.get_spawn_points()

    # Use the first available spawn point
    spawn_point = spawn_points[0] if spawn_points else None

    if spawn_point is None:
        print("No spawn points found.")
    else:
        # Get the blueprint library
        blueprint_library = world.get_blueprint_library()

        # Get the vehicle blueprint for a specific vehicle (e.g., Tesla Model3)
        vehicle_bp = blueprint_library.find('vehicle.tesla.model3')

        # Spawn the vehicle
        vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        if vehicle is not None:
            print("Spawned vehicle:", vehicle.id)

            # Set the vehicle as the spectator
            world.get_spectator().set_transform(vehicle.get_transform())

            # Control the vehicle to follow the lane
            while True:
                control_vehicle(vehicle, world)

        else:
            print("Failed to spawn vehicle.")

except Exception as e:
    print("Error:", e)