import json
import socket
from pathlib import Path
from typing import Union

_SEARCH_MESSAGE = """M-SEARCH * HTTP/1.1\r\n
HOST: 239.255.255.250:1982\r\n
MAN: "ssdp:discover"\r\n
ST: wifi_bulb"""

_BYTES_TO_SEND = str.encode(_SEARCH_MESSAGE)
_SERVER_ADDRESS_PORT = ("239.255.255.250", 1982)
_BUFFER_SIZE = 1024


async def locate_devices() -> tuple[int, dict[str, str]]:
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    udp_client_socket.sendto(_BYTES_TO_SEND, _SERVER_ADDRESS_PORT)
    msg_from_server = udp_client_socket.recvfrom(_BUFFER_SIZE)
    # msg = "Message from Server {}".format(msg_from_server[0])
    # print(msg_from_server)
    device_id, data = _parse_device(str(msg_from_server[0]))

    return device_id, data


def get_lamps_from_config() -> dict[str, dict[str, Union[str, int]]]:
    """Возвращает массив ламп из файла с конфигами"""
    with open(Path('configs') / 'lamps_conf.json') as file:
        contents = file.read()
        return json.loads(contents)


def _parse_device(response: str) -> tuple[int, dict[str, str]]:
    lines = response.split("\\r\\n")[1:]  # first line is always HTTP/1.1 200 OK

    device_id = -1
    data = {}
    for line in lines:
        key_index = line.find(":")
        if key_index > 0:
            key = line[:key_index]
            value = line[key_index + 2:]
            data[key] = value

            if key == "id":
                device_id = int(value, 0)

    return device_id, data
