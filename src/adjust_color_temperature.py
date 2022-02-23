import asyncio
import json
from datetime import datetime, time
from logging import warning
from typing import Any, Optional

from models.lamps import LightBulbAbstract, DesktopLamp, LightStripe, CeilingLamp
from services.device_locator import get_lamps_from_config

TIMEOUT = 15
PING_INTERVAL = 60


async def adjust():
    desktop_lamp = DesktopLamp(
        ip="192.168.68.104",
        port=55443,
        id=0x00000000177573c0,
    )
    light_stripe = LightStripe(
        ip="192.168.68.102",
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

    current_time = datetime.now().time()
    (temp, brightness) = _get_colour_temp_for_time(current_time)

    print(f"setting color temp to {temp} and {brightness}")

    for light in all_light:
        try:
            stats = await _get_stats(light)
            bright = brightness if brightness is not None else int(stats["bright"])

            if stats["power"] == "on":
                response = await _execute_command(light, light.set_color_temperature(temp, bright))
                print(response)
        except BaseException as e:
            warning(e)


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
    # b'{"id":393573312, "error":{"code":-1, "message":"client quota exceeded"}}\r\n'
    return line


def _get_colour_temp_for_time(time_of_date: time) -> (int, Optional[int]):
    time_of_day_to_colour = [
        {"time": time(hour=0), "temp": 3800, "brightness": None},
        {"time": time(hour=1), "temp": 3800, "brightness": None},
        {"time": time(hour=2), "temp": 3800, "brightness": None},
        {"time": time(hour=3), "temp": 3800, "brightness": None},
        {"time": time(hour=5), "temp": 3800, "brightness": None},
        {"time": time(hour=6), "temp": 3800, "brightness": None},
        {"time": time(hour=7), "temp": 3800, "brightness": None},
        {"time": time(hour=8), "temp": 4500, "brightness": 50},
        {"time": time(hour=9), "temp": 5000, "brightness": 100},
        {"time": time(hour=15), "temp": 4800, "brightness": 100},
        {"time": time(hour=16), "temp": 4500, "brightness": 100},
        {"time": time(hour=17), "temp": 4200, "brightness": None},
        {"time": time(hour=18), "temp": 4000, "brightness": None},
        {"time": time(hour=19), "temp": 3900, "brightness": None},
        {"time": time(hour=20), "temp": 3800, "brightness": None},
        {"time": time(hour=21), "temp": 3800, "brightness": None},
        {"time": time(hour=22), "temp": 3800, "brightness": None},
        {"time": time(hour=23), "temp": 3800, "brightness": None},
    ]
    # time_of_day_to_colour.sort(key=lambda o: o["time"])
    for tod in time_of_day_to_colour:
        if time_of_date < tod["time"]:
            return tod["temp"], tod["brightness"]

    return time_of_day_to_colour[0]["temp"], time_of_day_to_colour[0]["brightness"]


def _get_preconfigured_lamps() -> list[LightBulbAbstract]:
    devices = get_lamps_from_config()
    lamps = []
    for device in devices['lamps']:
        (type, ip, port, name, device_id) = (device['type'], device['ip'], device['port'], device['name'], device['id'])
        if type == 'ceiling_lamp':
            lamp = CeilingLamp(
                ip=ip,
                port=int(port),
                id=int(device_id),
            )
        elif type == 'stripe':
            lamp = LightStripe(
                ip=ip,
                port=int(port),
                id=int(device_id),
            )
        elif type == 'desktop_lamp':
            lamp = DesktopLamp(
                ip=ip,
                port=int(port),
                id=int(device_id),
            )

        if lamp is None:
            raise

        lamps.append(lamp)

    return lamps


if __name__ == '__main__':
    _get_preconfigured_lamps()
    a = 1
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(adjust())
    # loop.close()
