import carla

# Function to spawn a vehicle
def spawn_vehicle(world):
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter("vehicle.*")[0]
    spawn_point = carla.Transform(carla.Location(x=100, y=100, z=2), carla.Rotation(yaw=0))
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    return vehicle

# Function to apply throttle and steer to the vehicle
def apply_control(vehicle, throttle, steer):
    control = carla.VehicleControl()
    control.throttle = throttle
    control.steer = steer
    vehicle.apply_control(control)

# Main function
def main():
    try:
        # Connect to the CARLA server
        client = carla.Client("localhost", 2000)
        client.set_timeout(5.0)

        # Get the world
        world = client.get_world()

        # Spawn a vehicle
        vehicle = spawn_vehicle(world)

        # Main loop
        while True:
            # Get keyboard input
            throttle = float(input("Enter throttle value (-1.0 to 1.0): "))
            steer = float(input("Enter steer value (-1.0 to 1.0): "))

            # Apply control to the vehicle
            apply_control(vehicle, throttle, steer)

    finally:
        # Destroy actors
        vehicle.destroy()

if __name__ == "__main__":
    main()
