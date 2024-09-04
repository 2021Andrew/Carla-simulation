import carla
import random
import time

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

    # Get the map
    carla_map = world.get_map()

    # Get all the spawn points
    spawn_points = carla_map.get_spawn_points()

    # Choose a vehicle blueprint
    vehicle_blueprints = blueprint_library.filter('vehicle.*')
    if not vehicle_blueprints:
        print("Warning: No vehicle blueprints found. Exiting.")
        # Exit or handle the situation as needed

    vehicle_bp = random.choice(vehicle_blueprints)

    # Spawn a vehicle
    print("Spawning a vehicle...")
    spawn_point = random.choice(spawn_points)
    print("Chosen spawn point:", spawn_point)
    vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)

    if vehicle is None:
        print("Warning: Failed to spawn vehicle. Exiting.")
        # Exit or handle the situation as needed
    else:
        print("Spawned vehicle:", vehicle.id)

        # Attach a camera sensor to the vehicle
        print("Attaching a camera sensor to the vehicle...")
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

        # Set the camera sensor to follow the vehicle
        camera.listen(lambda data: data.save_to_disk('output/%06d.png' % data.frame))

        # Main loop
        while True:
            # Apply control inputs to the vehicle
            # ...

            # Wait for a small amount of time
            time.sleep(0.1)

except Exception as e:
    print("Error:", e)

finally:
    print("Disconnecting from CARLA server...")