import platform
import subprocess
import os
import logging

# Constants for theme types
DARK_THEME = "dark"
LIGHT_THEME = "light"

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def detect_windows_theme():
    try:
        import winreg

        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(
            registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return LIGHT_THEME if value == 1 else DARK_THEME
    except Exception as e:
        logger.error(f"Error detecting Windows theme: {e}")
        return None


def detect_macos_theme():
    try:
        result = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode == 0:
            return DARK_THEME
        else:
            return LIGHT_THEME
    except Exception as e:
        logger.error(f"Error detecting macOS theme: {e}")
        return None


def detect_gnome_theme():
    try:
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
            stdout=subprocess.PIPE,
        )
        theme = result.stdout.decode().strip().strip("'")
        return DARK_THEME if "dark" in theme else LIGHT_THEME
    except Exception as e:
        logger.error(f"Error detecting GNOME theme: {e}")
        return None


def detect_kde_theme():
    try:
        result = subprocess.run(
            ["qdbus", "org.kde.KWin", "/KWin", "org.kde.KWin.readConfig", "Theme"],
            stdout=subprocess.PIPE,
        )
        theme = result.stdout.decode().strip()
        return DARK_THEME if "dark" in theme.lower() else LIGHT_THEME
    except Exception as e:
        logger.error(f"Error detecting KDE theme: {e}")
        return None


def detect_linux_theme():
    desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    if "gnome" in desktop_env:
        return detect_gnome_theme()
    elif "kde" in desktop_env:
        return detect_kde_theme()
    else:
        logger.warning(f"Unsupported Linux desktop environment: {desktop_env}")
        return None


def detect_system_theme(default_theme=LIGHT_THEME):
    os_name = platform.system()

    if os_name == "Windows":
        system_theme = detect_windows_theme()
    elif os_name == "Darwin":
        system_theme = detect_macos_theme()
    elif os_name == "Linux":
        system_theme = detect_linux_theme()
    else:
        logger.warning(f"Unsupported operating system: {os_name}")
        system_theme = default_theme

    return system_theme


if __name__ == "__main__":
    theme = detect_system_theme()
    if theme:
        logger.info(f"The system theme is {theme}.")
    else:
        logger.warning("Could not detect the system theme.")
