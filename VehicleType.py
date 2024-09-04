import carla

# Connect to Carla server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)  # Increase timeout if necessary

# Retrieve the world
world = client.get_world()

# Retrieve the current map
current_map = world.get_map()
print("Current Map:", current_map.name)

# Print all vehicle types and their role names
print("Available Vehicles:")
for actor in world.get_actors():
    if actor.type_id.startswith('vehicle'):
        print("- Type:", actor.type_id)
        print("  Role Name:", actor.attributes.get('role_name'))

# Disconnect from the server
client.disconnect()
