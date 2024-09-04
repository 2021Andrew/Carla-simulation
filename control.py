import carla
import pygame
import numpy as np

# Function to control the steering based on user input
def control_steering(event):
    global steering
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            steering = max(-1.0, steering - 0.1)
        elif event.key == pygame.K_RIGHT:
            steering = min(1.0, steering + 0.1)
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            steering = 0.0

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Manual Steering Control")

# Connect to Carla server
client = carla.Client('localhost', 2000)
client.set_timeout(4.0)

# Retrieve the world
world = client.get_world()

# Retrieve the ego vehicle
ego_vehicle = None
for actor in world.get_actors():
    if actor.type_id == 'vehicle.tesla.model3':
        ego_vehicle = actor
        break

if ego_vehicle is None:
    print("Ego vehicle not found!")
    pygame.quit()
    quit()

# Initial steering angle
steering = 0.0

# Main loop
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            control_steering(event)
        
        # Apply steering control to the vehicle
        control = carla.VehicleControl()
        control.steer = steering
        ego_vehicle.apply_control(control)

        # Display steering angle
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        text = font.render("Steering: {:.2f}".format(steering), True, (0, 0, 0))
        screen.blit(text, (50, 50))
        pygame.display.flip()
        
        # Cap the frame rate
        pygame.time.Clock().tick(60)

finally:
    pygame.quit()
