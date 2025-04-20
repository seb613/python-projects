import os
import subprocess
import sys

def launch_designer():
    # Determine the path to Qt Designer
    if sys.platform == "win32":
        designer_path = os.path.join(
            sys.prefix, "Lib", "site-packages", "qt6_applications", "Qt", "bin", "designer.exe"
        )
    else:  # macOS/Linux
        designer_path = os.path.join(
            sys.prefix, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}",
            "site-packages", "qt6_applications", "Qt", "bin", "designer"
        )
    
    # Check if the path exists
    if not os.path.exists(designer_path):
        print("Qt Designer not found. Make sure pyqt6-tools is installed.")
        return
    
    # Launch Qt Designer
    try:
        subprocess.run([designer_path])
    except Exception as e:
        print(f"Failed to launch Qt Designer: {e}")

if __name__ == "__main__":
    launch_designer()
