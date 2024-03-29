from datetime import datetime
import asyncio
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from config.config import EMAIL_IOT_LIGHT, PASSWORD_IOT_LIGHT


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
    http_api_client = await MerossHttpClient.async_from_user_password(email=email, password=password, api_base_url ="https://iotx-eu.meross.com")

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

async def async_control_light(state: str):
    """
    Control the light by turning it on or off based on the specified state.

    Args:
        state (str): The desired state of the light, 'on' or 'off'.
    """
    # Use the existing setup_device function to get the device and manager
    dev, manager = await setup_device(EMAIL_IOT_LIGHT, PASSWORD_IOT_LIGHT, "mss210")
    if dev is None:
        print("Device not found.")
        return

    # Use the existing control_plug function to change the state of the device
    await control_plug(dev, state)
    print(f"Light has been turned {state}.")


def control_light_robot(status: str):
    asyncio.run(async_control_light(status))

control_light_robot("off")
