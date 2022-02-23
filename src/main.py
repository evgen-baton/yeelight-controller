# from typing import Optional
# from fastapi import FastAPI
# from .services.chuk_norris import get_random_joke
#
# app = FastAPI()
#
#
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
#
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}
#
#
# @app.get("/get-chuk-norris-joke/")
# def get_chuk_norris_joke():
#     joke = get_random_joke()
#     return {
#         "joke": joke
#     }
import asyncio
import json
from logging import warning
from typing import Any

from models.lamps import DesktopLamp, LightStripe, CeilingLamp, LightBulbAbstract
from services.device_locator import locate_devices

TIMEOUT = 15
PING_INTERVAL = 60
_DEVICES = {}


async def main():
    desktop_lamp = DesktopLamp(
        ip="192.168.68.104",
        port=55443,
        id=0x00000000177573c0,
    )
    light_stripe = LightStripe(
        ip="192.168.68.101",
        port=55443,
        id=0x0000000012c71a7e,
    )
    ceiling_lamp = CeilingLamp(
        ip="192.168.68.103",
        port=55443,
        id=0x00000000179e06d8,
    )

    all_light = [
        desktop_lamp,
        light_stripe,
        ceiling_lamp,
    ]

    # result = await _execute_command(ceiling_lamp, ceiling_lamp.set_name("ceiling_light"))
    # print(result)
    # stats = await _get_stats(ceiling_lamp)
    # print(stats)

    # for light in all_light:
    #     try:
    #         stats = await _get_stats(light)
    #         if stats["power"] == "on":
    #             response = await _execute_command(light, light.set_color_temperature(4200, 100))
    #             print(response)
    #     except BaseException as e:
    #         warning(e)

    # response = await _execute_command(desktop_lamp, desktop_lamp.get_stats())
    # print(response)
    # stats = await _get_stats(desktop_lamp)

    # devices = []
    # while True:
    #     devices_to_add = [other_device for other_device in _DEVICES.items() if other_device not in devices]
    #     if len(devices_to_add) > 0:
    #         for device in devices_to_add:
    #             devices.append(device)
    #             print(f'Found device: {device[1]["id"]} // {device[1]["model"]} // {device[1]["name"]}')
    #     await asyncio.sleep(1)


async def _get_stats(bulb: LightBulbAbstract) -> dict[str, str]:
    params = bulb.get_stats()["params"]
    response = await _execute_command(bulb, bulb.get_stats())
    response_json = json.loads(response)
    result = {}
    for index in range(len(params)):
        result[params[index]] = response_json["result"][index]

    return result


async def _execute_command(bulb: LightBulbAbstract, command: Any):
    reader, writer = await asyncio.wait_for(
        asyncio.open_connection(bulb.ip, bulb.port), TIMEOUT
    )
    json_message = command
    msg = (json.dumps(json_message, separators=(",", ":")) + "\r\n").encode("utf8")

    writer.write(msg)

    line = await asyncio.wait_for(
        reader.readline(), PING_INTERVAL + TIMEOUT
    )
    return line


async def _update_devices():
    while True:
        device = await locate_devices()
        _DEVICES[device[0]] = device[1]
        print(device)
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # update_devices_task = loop.create_task(_update_devices())
    # loop.run_until_complete(main())
    loop.run_until_complete(_update_devices())
    loop.close()
