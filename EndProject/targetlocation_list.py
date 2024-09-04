import carla
import time
import numpy as np

class PIDController:
    def __init__(self, Kp, Ki, Kd, target_speed):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.target_speed = target_speed
        self.prev_error = 0
        self.integral = 0

    def control(self, current_value, target_value, dt):
        error = target_value - current_value
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        return self.Kp * error + self.Ki * self.integral + self.Kd * derivative

def control_vehicle(vehicle, world, pid_steering, pid_throttle, target_location, dt):
    vehicle_transform = vehicle.get_transform()
    vehicle_location = vehicle_transform.location
    vehicle_yaw = vehicle_transform.rotation.yaw

    waypoint = world.get_map().get_waypoint(vehicle_location, project_to_road=True)
    next_waypoint = waypoint.next(2.0)[0]

    next_waypoint_location = next_waypoint.transform.location
    dx = next_waypoint_location.x - vehicle_location.x
    dy = next_waypoint_location.y - vehicle_location.y
    desired_yaw = np.arctan2(dy, dx) * 180 / np.pi

    steering_angle = pid_steering.control(vehicle_yaw, desired_yaw, dt)

    distance_to_target = np.sqrt((target_location.x - vehicle_location.x)**2 +
                                 (target_location.y - vehicle_location.y)**2)

    if distance_to_target < 5.0:
        throttle = 0.0
        brake = 1.0
    else:
        current_speed = np.sqrt(vehicle.get_velocity().x**2 + vehicle.get_velocity().y**2 + vehicle.get_velocity().z**2)
        throttle = pid_throttle.control(current_speed, pid_throttle.target_speed, dt)
        brake = 0.0

    control = carla.VehicleControl()
    control.throttle = np.clip(throttle, 0.0, 1.0)
    control.steer = np.clip(steering_angle / 25.0, -1.0, 1.0)
    control.brake = brake
    control.reverse = False
    vehicle.apply_control(control)

def update_spectator_view(spectator, vehicle):
    vehicle_transform = vehicle.get_transform()
    spectator_transform = carla.Transform(vehicle_transform.location + carla.Location(z=50), carla.Rotation(pitch=-90))
    spectator.set_transform(spectator_transform)

def input_target_locations():
    target_locations = []
    while True:
        user_input = input("Enter target location (x,y,z) or 'done' to finish: ").strip()
        if user_input.lower() == 'done':
            break
        try:
            # Remove parentheses if they exist
            user_input = user_input.replace('(', '').replace(')', '')
            # Split the input by commas and convert to floats
            x, y, z = map(float, user_input.split(','))
            target_locations.append(carla.Location(x=x, y=y, z=z))
        except ValueError:
            print("Invalid input. Please enter coordinates as x,y,z.")
    return target_locations

# PID controller parameters
Kp_steering = 0.5
Ki_steering = 0.01
Kd_steering = 0.1
Kp_throttle = 1.0
Ki_throttle = 0.1
Kd_throttle = 0.01
target_speed = 10

pid_steering = PIDController(Kp_steering, Ki_steering, Kd_steering, target_speed)
pid_throttle = PIDController(Kp_throttle, Ki_throttle, Kd_throttle, target_speed)

vehicle = None

try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    carla_map = world.get_map()
    spawn_points = carla_map.get_spawn_points()

    target_locations = input_target_locations()
    if not target_locations:
        print("No target locations provided.")
        exit()

    spawn_point = spawn_points[0] if spawn_points else None

    if spawn_point is None:
        print("No spawn points found.")
    else:
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.find('vehicle.tesla.model3')

        vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        if vehicle is not None:
            print("Spawned vehicle:", vehicle.id)

            spectator = world.get_spectator()
            update_spectator_view(spectator, vehicle)

            print("Target Locations:", target_locations)

            for target_location in target_locations:
                print(f"Heading towards target: x={target_location.x}, y={target_location.y}, z={target_location.z}")
                reached_target = False
                previous_time = time.time()
                while not reached_target:
                    current_time = time.time()
                    dt = current_time - previous_time
                    previous_time = current_time

                    control_vehicle(vehicle, world, pid_steering, pid_throttle, target_location, dt)
                    update_spectator_view(spectator, vehicle)
                    time.sleep(0.1)

                    vehicle_location = vehicle.get_transform().location
                    distance_to_target = np.sqrt((target_location.x - vehicle_location.x)**2 +
                                                 (target_location.y - vehicle_location.y)**2)

                    if distance_to_target < 5.0:
                        reached_target = True
                        print(f"Reached target: x={target_location.x}, y={target_location.y}, z={target_location.z}")

                print("Moving to the next target location")

        else:
            print("Failed to spawn vehicle.")

except Exception as e:
    print("Error:", e)

finally:
    if vehicle is not None:
        vehicle.destroy()
        print("Destroyed vehicle")
