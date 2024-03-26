# src/utils.py

from datetime import datetime
import asyncio
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

import json
import os


def load_config(config_path):
    """
    Load configuration file from the provided path.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Configuration data.
    """
    with open(os.path.join(os.path.dirname(__file__), config_path)) as json_file:
        config = json.load(json_file)

    return config


async def control_plug(dev, action):
    print(f"{datetime.now()}: {dev.name} is turning {'ON' if action == 'on' else 'OFF'}...")
    if action == 'on':
        await dev.async_turn_on(channel=0)
    else:
        await dev.async_turn_off(channel=0)

async def setup_device(email, password, device_type):
    """
    Setup the Meross device manager and find the first available plug.
    """

    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=email, password=password)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()
    await manager.async_device_discovery()

    # Find the first available plug
    plugs = manager.find_devices(device_type=device_type)
    if len(plugs) < 1:
        print(f"No {device_type} plugs found...")
        return None, None
    dev = plugs[0]
    return dev, manager

async def main():
    # Load configuration
    credentials = load_config("../../credentials.json")

    # Initialize the device
    dev, manager = await setup_device(credentials["email"], credentials["password"], "mss210")
    if dev is None:
        return
    control_plug(dev, 'on')

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())