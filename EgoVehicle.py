import carla

# Connect to Carla server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)  # Increase timeout if necessary

# Retrieve the world
world = client.get_world()

# Retrieve the current map
current_map = world.get_map()
print("Current Map:", current_map.name)

# Find the ego vehicle
ego_vehicle = None
for actor in world.get_actors():
    if actor.type_id.startswith('vehicle') and actor.attributes.get('role_name') == 'ego_vehicle':
        ego_vehicle = actor
        break

if ego_vehicle:
    print("Ego Vehicle:", ego_vehicle.type_id)
else:
    print("Ego Vehicle not found!")

# Close connection
client.disconnect()
