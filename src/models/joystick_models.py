"""
Joystick model database and identification
Maps detected joystick info to known models and their visual templates
"""
from typing import Dict, Optional


class JoystickModel:
    """Represents a known joystick model with its characteristics"""

    def __init__(self, name: str, manufacturer: str, button_count: int,
                 axis_count: int, template_name: str, keywords: list):
        self.name = name
        self.manufacturer = manufacturer
        self.button_count = button_count
        self.axis_count = axis_count
        self.template_name = template_name
        self.keywords = keywords  # Words to match in device name

    def matches(self, device_name: str, button_count: int, axis_count: int) -> int:
        """
        Calculate match score for this model against detected device

        Args:
            device_name: The detected device name
            button_count: Number of buttons detected
            axis_count: Number of axes detected

        Returns:
            Match score (0-100), higher is better match
        """
        score = 0
        device_lower = device_name.lower()

        # Check for keyword matches (50 points max)
        keyword_matches = sum(1 for keyword in self.keywords if keyword.lower() in device_lower)
        score += (keyword_matches / len(self.keywords)) * 50

        # Check button count match (30 points)
        if button_count == self.button_count:
            score += 30
        elif abs(button_count - self.button_count) <= 2:
            score += 20  # Close enough

        # Check axis count match (20 points)
        if axis_count == self.axis_count:
            score += 20
        elif abs(axis_count - self.axis_count) <= 1:
            score += 10

        return score


# Database of known joystick models
KNOWN_MODELS = [
    # VIRPIL Constellation Alpha Prime
    JoystickModel(
        name="VPC Constellation ALPHA Prime",
        manufacturer="VIRPIL",
        button_count=32,
        axis_count=6,
        template_name="virpil_alpha_prime",
        keywords=["virpil", "vpc", "alpha", "constellation"]
    ),

    # VIRPIL Constellation ALPHA (original)
    JoystickModel(
        name="VPC Constellation ALPHA",
        manufacturer="VIRPIL",
        button_count=29,
        axis_count=6,
        template_name="virpil_alpha",
        keywords=["virpil", "vpc", "alpha", "constellation"]
    ),

    # VIRPIL MongoosT-50CM3
    JoystickModel(
        name="VPC MongoosT-50CM3",
        manufacturer="VIRPIL",
        button_count=31,
        axis_count=5,
        template_name="virpil_mongoost50cm3",
        keywords=["virpil", "vpc", "mongoost", "cm3"]
    ),

    # VIRPIL WarBRD Grip (original)
    JoystickModel(
        name="VPC WarBRD Grip",
        manufacturer="VIRPIL",
        button_count=24,
        axis_count=6,
        template_name="virpil_warbrd_grip",
        keywords=["virpil", "vpc", "warbrd"]
    ),

    # VKB Gladiator NXT
    JoystickModel(
        name="VKB Gladiator NXT",
        manufacturer="VKB",
        button_count=34,
        axis_count=5,
        template_name="vkb_gladiator_nxt",
        keywords=["vkb", "gladiator", "nxt"]
    ),

    # VKB Gladiator NXT EVO
    JoystickModel(
        name="VKB Gladiator NXT EVO",
        manufacturer="VKB",
        button_count=34,
        axis_count=5,
        template_name="vkb_gladiator_nxt_evo",
        keywords=["vkb", "gladiator", "evo"]
    ),

    # Thrustmaster T.16000M
    JoystickModel(
        name="Thrustmaster T.16000M",
        manufacturer="Thrustmaster",
        button_count=16,
        axis_count=4,
        template_name="thrustmaster_t16000m",
        keywords=["thrustmaster", "t16000", "t.16000"]
    ),

    # Thrustmaster HOTAS Warthog Stick
    JoystickModel(
        name="Thrustmaster HOTAS Warthog",
        manufacturer="Thrustmaster",
        button_count=19,
        axis_count=3,
        template_name="thrustmaster_warthog",
        keywords=["thrustmaster", "warthog", "hotas"]
    ),
]


def identify_joystick(device_name: str, button_count: int, axis_count: int) -> Optional[JoystickModel]:
    """
    Identify a joystick model from its detected characteristics

    Args:
        device_name: The device name from pygame
        button_count: Number of buttons detected
        axis_count: Number of axes detected

    Returns:
        Best matching JoystickModel, or None if no good match found
    """
    best_match = None
    best_score = 0

    for model in KNOWN_MODELS:
        score = model.matches(device_name, button_count, axis_count)
        if score > best_score:
            best_score = score
            best_match = model

    # Require at least 40% match to consider it identified
    if best_score >= 40:
        return best_match

    return None


def get_model_by_name(model_name: str) -> Optional[JoystickModel]:
    """
    Get a model by its exact name

    Args:
        model_name: The model name

    Returns:
        JoystickModel if found, None otherwise
    """
    for model in KNOWN_MODELS:
        if model.name.lower() == model_name.lower():
            return model
    return None
