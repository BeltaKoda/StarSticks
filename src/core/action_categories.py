"""
Star Citizen action categorization
Categorizes SC actions into modes: Flight, Ground, EVA, Mining, etc.
"""
from enum import Enum
from typing import Set


class ActionMode(Enum):
    """SC gameplay modes/contexts"""
    ALL = "All"
    FLIGHT = "Flight"
    GROUND = "Ground / FPS"
    EVA = "EVA"
    MINING = "Mining"
    TURRET = "Turret"
    VEHICLE = "Vehicle"
    UI = "UI / General"


# Keywords that indicate which mode an action belongs to
MODE_KEYWORDS = {
    ActionMode.FLIGHT: [
        'spaceship', 'v_', 'flight', 'ship_', 'vtol', 'throttle',
        'pitch', 'yaw', 'roll', 'strafe', 'ifcs', 'cruise', 'boost',
        'quantum', 'landing', 'doors', 'ramp', 'power_', 'shield_',
        'weapon_', 'missile', 'countermeasure', 'targeting', 'gimbal',
        'scanner', 'radar', 'hud_', 'cockpit'
    ],

    ActionMode.GROUND: [
        'player_', 'fps_', 'walk', 'sprint', 'crouch', 'prone', 'jump',
        'lean', 'melee', 'reload', 'zoom', 'aim', 'grenade', 'inspect',
        'holster', 'throw', 'interaction', 'use', 'pickup'
    ],

    ActionMode.EVA: [
        'eva_', 'space_walk', 'jetpack', 'mag_boot', 'magnetize'
    ],

    ActionMode.MINING: [
        'mining_', 'laser_power', 'extraction', 'fracture', 'scanning_turret'
    ],

    ActionMode.TURRET: [
        'turret_', 'turret_movement', 'turret_fire'
    ],

    ActionMode.VEHICLE: [
        'vehicle_', 'rover_', 'ground_vehicle', 'wheeled_'
    ],

    ActionMode.UI: [
        'ui_', 'mobiglas', 'starmap', 'inventory', 'chat', 'quickchat',
        'respawn', 'menu', 'visor', 'inner_thought', 'focus', 'emote',
        'friends', 'party', 'contract'
    ]
}


def categorize_action(action_name: str) -> ActionMode:
    """
    Categorize a Star Citizen action into a mode

    Args:
        action_name: The action name from SC binding XML

    Returns:
        The ActionMode this action belongs to
    """
    action_lower = action_name.lower()

    # Check each mode's keywords
    for mode, keywords in MODE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in action_lower:
                return mode

    # Default to UI/General if no specific category found
    return ActionMode.UI


def get_mode_description(mode: ActionMode) -> str:
    """
    Get a user-friendly description of a mode

    Args:
        mode: The ActionMode

    Returns:
        Description string
    """
    descriptions = {
        ActionMode.ALL: "Show all bindings",
        ActionMode.FLIGHT: "Spaceship flight controls",
        ActionMode.GROUND: "On-foot / FPS controls",
        ActionMode.EVA: "Zero-gravity EVA controls",
        ActionMode.MINING: "Mining laser controls",
        ActionMode.TURRET: "Turret operation controls",
        ActionMode.VEHICLE: "Ground vehicle controls",
        ActionMode.UI: "User interface & menus"
    }
    return descriptions.get(mode, "")


def get_mode_icon(mode: ActionMode) -> str:
    """
    Get an icon/emoji for a mode

    Args:
        mode: The ActionMode

    Returns:
        Icon string
    """
    icons = {
        ActionMode.ALL: "📋",
        ActionMode.FLIGHT: "🚀",
        ActionMode.GROUND: "🏃",
        ActionMode.EVA: "👨‍🚀",
        ActionMode.MINING: "⛏️",
        ActionMode.TURRET: "🎯",
        ActionMode.VEHICLE: "🚗",
        ActionMode.UI: "💻"
    }
    return icons.get(mode, "")
