import importlib.metadata
import sys

packages = [
    "beautifulsoup4",
    "colorlog",
    "comtypes; sys_platform == 'win32'",
    "gradio_client",
    "lxml_html_clean",
    "nltk",
    "numpy",
    "opencv-python",
    "openai",
    "pillow",
    "psutil",
    "pulsectl; sys_platform == 'linux'",
    "pyaudio",
    "pyautogui",
    "pycaw; sys_platform == 'win32'",
    "pygame",
    "pypiwin32; sys_platform == 'win32'",
    "PyQt5",
    "python-dotenv",
    "pyttsx3",
    "pywhatkit",
    "requests",
    "scipy",
    "selenium",
    "sumy",
    "webdriver-manager",
    "webscout",
    "winotify; sys_platform == 'win32'",
    "wmi; sys_platform == 'win32'",
    "yaspin"
]

installed_packages = {}
for dist in importlib.metadata.distributions():
    installed_packages[dist.metadata["Name"].lower()] = dist.version

output_lines = []
for pkg in packages:
    base_pkg = pkg.split(";")[0].strip().lower()
    
    # Handle aliases
    lookup_name = base_pkg
    if base_pkg == "opencv-python":
        lookup_name = "opencv-python" # it registers as opencv-python in dist usually
    
    version = installed_packages.get(lookup_name)
    if version:
        output_lines.append(f"{pkg.split(';')[0].strip()}=={version}" + (f"; {pkg.split(';')[1].strip()}" if ";" in pkg else ""))
    else:
        output_lines.append(pkg)

# Sort alphabetically
output_lines.sort(key=lambda x: x.lower())

with open("requirements.txt", "w") as f:
    for line in output_lines:
        f.write(line + "\n")

print("Generated requirements.txt:")
print("\n".join(output_lines))
