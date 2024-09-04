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

    def control(self, current_yaw, desired_yaw, dt):
        error = desired_yaw - current_yaw
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        return self.Kp * error + self.Ki * self.integral + self.Kd * derivative

def control_vehicle(vehicle, world, pid_controller, dt):
    vehicle_transform = vehicle.get_transform()
    waypoint = world.get_map().get_waypoint(vehicle_transform.location, project_to_road=True)
    next_waypoint = waypoint.next(2.0)[0]

    vehicle_location = vehicle_transform.location
    vehicle_yaw = vehicle_transform.rotation.yaw
    next_waypoint_location = next_waypoint.transform.location
    dx = next_waypoint_location.x - vehicle_location.x
    dy = next_waypoint_location.y - vehicle_location.y
    desired_yaw = np.arctan2(dy, dx) * 180 / np.pi
    
    steering_angle = pid_controller.control(vehicle_yaw, desired_yaw, dt)

    control = carla.VehicleControl()
    control.throttle = 0.5
    control.steer = np.clip(steering_angle / 25.0, -1.0, 1.0)
    control.brake = 0.0
    control.reverse = False
    vehicle.apply_control(control)

def update_spectator_view(spectator, vehicle):
    vehicle_transform = vehicle.get_transform()
    spectator.set_transform(carla.Transform(vehicle_transform.location + carla.Location(z=50), carla.Rotation(pitch=-90)))

def main():
    # PID controller parameters
    Kp = 0.5
    Ki = 0.01
    Kd = 0.1
    target_speed = 10  # Adjust as needed

    pid_controller = PIDController(Kp, Ki, Kd, target_speed)

    vehicle = None  # Initialize vehicle to None to ensure it is defined in the scope

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

                # Set the initial spectator view
                spectator = world.get_spectator()
                update_spectator_view(spectator, vehicle)

                # Control the vehicle to follow the lane
                previous_time = time.time()
                while True:
                    current_time = time.time()
                    dt = current_time - previous_time
                    previous_time = current_time

                    control_vehicle(vehicle, world, pid_controller, dt)
                    update_spectator_view(spectator, vehicle)
                    time.sleep(0.1)  # Adjust loop rate as needed

            else:
                print("Failed to spawn vehicle.")

    except Exception as e:
        print("Error:", e)

    finally:
        # Clean up the CARLA actors
        if vehicle is not None:
            vehicle.destroy()
            print("Destroyed vehicle")

if __name__ == "__main__":
    main()
