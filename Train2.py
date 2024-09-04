#!/usr/bin/env python

# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================
import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
import carla

import argparse
import logging
import random

# ==============================================================================
# -- World ---------------------------------------------------------------------
# ==============================================================================

def main():
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    args = argparser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    client = carla.Client(args.host, args.port)
    client.set_timeout(2.0)

    try:
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()

        # Get a random vehicle blueprint
        vehicle_bp = random.choice(blueprint_library.filter('vehicle'))
        transform = random.choice(world.get_map().get_spawn_points())
        vehicle = world.spawn_actor(vehicle_bp, transform)

        # Set up the camera
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_transform = carla.Transform(carla.Location(x=2.5, z=0.7))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

        control = carla.VehicleControl()

        while True:
            world.wait_for_tick()

            # Get keyboard input
            keys = input("Enter controls (w,a,s,d,r for reset): ")

            if 'w' in keys:
                control.throttle = 1.0
            else:
                control.throttle = 0.0

            if 'a' in keys:
                control.steer = -1.0
            elif 'd' in keys:
                control.steer = 1.0
            else:
                control.steer = 0.0

            if 'r' in keys:
                # Reset vehicle position
                vehicle.set_transform(transform)
                control.throttle = 0.0
                control.steer = 0.0

            vehicle.apply_control(control)

    finally:
        print('destroying actors')
        camera.destroy()
        vehicle.destroy()
        print('done.')

if __name__ == '__main__':
    main()