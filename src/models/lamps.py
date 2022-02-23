import abc
from dataclasses import dataclass


@dataclass
class LightBulbAbstract:
    ip: str
    port: int
    id: int

    @abc.abstractmethod
    def set_power_on(self):
        raise NotImplementedError

    @abc.abstractmethod
    def set_power_off(self):
        raise NotImplementedError

    @abc.abstractmethod
    def set_color_temperature(self, color_temperature: int, brightness: int):
        """
        :param color_temperature: 1700 - 6500
        :param brightness: 1 - 100
        """
        raise NotImplementedError

    def get_stats(self):
        return {
            "id": self.id,
            "method": "get_prop",
            "params": ["power", "bright", "color_mode", "ct", "rgb", "hue", "sat", "name"]
        }

    def set_name(self, name: str):
        return {
            "id": self.id,
            "method": "set_name",
            "params": [f"{name}"]
        }


@dataclass
class LightStripe(LightBulbAbstract):
    def set_power_on(self):
        return {
            "id": self.id,
            "method": "set_power",
            "params": ["on", "smooth", 2000]
        }

    def set_power_off(self):
        return {
            "id": self.id,
            "method": "set_power",
            "params": ["off", "smooth", 2000]
        }

    def set_color_temperature(self, color_temperature: int, brightness: int):
        return {
            "id": self.id,
            "method": "start_cf",
            "params": [1, 1, f"5000, 2, {color_temperature}, {brightness}"]
        }


@dataclass
class DesktopLamp(LightBulbAbstract):
    def set_power_on(self):
        return {
            "id": self.id,
            "method": "set_power",
            "params": ["on", "smooth", 2000]
        }

    def set_power_off(self):
        return {
            "id": self.id,
            "method": "set_power",
            "params": ["off", "smooth", 2000]
        }

    def set_color_temperature(self, color_temperature: int, brightness: int):
        return {
            "id": self.id,
            "method": "start_cf",
            "params": [1, 1, f"5000, 2, {color_temperature}, {brightness}"]
        }


@dataclass
class CeilingLamp(LightBulbAbstract):
    def set_power_on(self):
        return {
            "id": self.id,
            "method": "set_power",
            "params": ["on", "smooth", 4000]
        }

    def set_power_off(self):
        return {
            "id": self.id,
            "method": "set_power",
            "params": ["off", "smooth", 4000]
        }

    def set_color_temperature(self, color_temperature: int, brightness: int):
        return {
            "id": self.id,
            "method": "start_cf",
            "params": [1, 1, f"5000, 2, {color_temperature}, {brightness}"]
        }
