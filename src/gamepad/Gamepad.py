import json
from typing import Dict, Any

class Button:
    def __init__(self, pressed: bool, value: int):
        self.pressed = pressed
        self.value = value

    def __repr__(self):
        return f"Button(pressed={self.pressed}, value={self.value})"

class Axis:
    def __init__(self, axis: list, button: Button):
        self.axis = axis
        self.button = button

    def __repr__(self):
        return f"Axis(axis={self.axis}, button={self.button})"

class Gamepad:
    def __init__(self, data: Dict[str, Any]):
        self.A_BUTTON = Button(**data.get("A_BUTTON", {}))
        self.B_BUTTON = Button(**data.get("B_BUTTON", {}))
        self.X_BUTTON = Button(**data.get("X_BUTTON", {}))
        self.Y_BUTTON = Button(**data.get("Y_BUTTON", {}))
        self.LEFT_TRIGGER = Button(**data.get("LEFT_TRIGGER", {}))
        self.RIGHT_TRIGGER = Button(**data.get("RIGHT_TRIGGER", {}))
        self.LEFT_BUMPER = Button(**data.get("LEFT_BUMPER", {}))
        self.RIGHT_BUMPER = Button(**data.get("RIGHT_BUMPER", {}))
        self.LEFT_STICK = Axis(data["LEFT_STICK"]["axis"], Button(**data["LEFT_STICK"]["button"]))
        self.RIGHT_STICK = Axis(data["RIGHT_STICK"]["axis"], Button(**data["RIGHT_STICK"]["button"]))

    def __repr__(self):
        return (f"Gamepad(A_BUTTON={self.A_BUTTON}, B_BUTTON={self.B_BUTTON}, "
                f"X_BUTTON={self.X_BUTTON}, Y_BUTTON={self.Y_BUTTON}, "
                f"LEFT_TRIGGER={self.LEFT_TRIGGER}, RIGHT_TRIGGER={self.RIGHT_TRIGGER}, "
                f"LEFT_BUMPER={self.LEFT_BUMPER}, RIGHT_BUMPER={self.RIGHT_BUMPER}, "
                f"LEFT_STICK={self.LEFT_STICK}, RIGHT_STICK={self.RIGHT_STICK})")
        
    @staticmethod
    def map_json_to_gamepad(json_data: str):
        data = json.loads(json_data)
        return Gamepad(data)