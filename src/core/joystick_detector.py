"""
Joystick detection module
Detects connected joystick devices and retrieves their information
"""
import pygame
from typing import List, Dict


class JoystickDetector:
    """Detects and manages connected joystick devices"""

    # Blacklist of device names that should be filtered out
    DEVICE_BLACKLIST = [
        'keychron',
        'keyboard',
        'mouse',
        'touchpad',
        'trackpad',
        'pen',
        'stylus',
    ]

    def __init__(self):
        """Initialize the joystick detector"""
        # Initialize pygame joystick module
        pygame.init()
        pygame.joystick.init()

    def is_blacklisted(self, device_name: str) -> bool:
        """
        Check if a device is blacklisted (not a real joystick)

        Args:
            device_name: The name of the device

        Returns:
            True if the device is blacklisted
        """
        name_lower = device_name.lower()
        return any(blacklisted in name_lower for blacklisted in self.DEVICE_BLACKLIST)

    def detect(self, filter_blacklisted: bool = True) -> List[Dict]:
        """
        Detect all connected joysticks

        Args:
            filter_blacklisted: If True, filter out blacklisted devices

        Returns:
            List of dictionaries containing joystick information
        """
        joysticks = []

        # Refresh joystick list
        pygame.joystick.quit()
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()

        for i in range(joystick_count):
            try:
                joy = pygame.joystick.Joystick(i)
                joy.init()

                device_name = joy.get_name()

                # Skip blacklisted devices if filtering is enabled
                if filter_blacklisted and self.is_blacklisted(device_name):
                    joy.quit()
                    continue

                joystick_info = {
                    'id': i,
                    'name': device_name,
                    'guid': joy.get_guid(),
                    'buttons': joy.get_numbuttons(),
                    'axes': joy.get_numaxes(),
                    'hats': joy.get_numhats(),
                    'instance_id': joy.get_instance_id()
                }

                joysticks.append(joystick_info)
                joy.quit()

            except pygame.error as e:
                print(f"Error initializing joystick {i}: {e}")

        return joysticks

    def get_joystick_by_name(self, name: str) -> Dict:
        """
        Get a specific joystick by name

        Args:
            name: The name of the joystick to find

        Returns:
            Dictionary containing joystick information, or None if not found
        """
        joysticks = self.detect()
        for joy in joysticks:
            if name.lower() in joy['name'].lower():
                return joy
        return None

    def is_virpil_alpha(self, joystick_name: str) -> bool:
        """
        Check if a joystick is a Virpil Alpha Prime

        Args:
            joystick_name: The name of the joystick

        Returns:
            True if the joystick is a Virpil Alpha Prime
        """
        name_lower = joystick_name.lower()
        return 'virpil' in name_lower and 'alpha' in name_lower

    def cleanup(self):
        """Clean up pygame resources"""
        pygame.joystick.quit()
        pygame.quit()
