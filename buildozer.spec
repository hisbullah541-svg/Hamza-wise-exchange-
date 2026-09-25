[app]

# (str) Title of your application
title = Hamza Wise Exchange

# (str) Package name
package.name = hamzawiseexchange

# (str) Package domain (needed for android packaging)
package.domain = org.hamza

# (str) Source files to include (let it include python files and graphics)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to include (let it point to root)
source.dir = .

# (list) Application requirements
# Keeping requirements clean and compatible with Android builds
requirements = python3,kivy,certifi

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android architectural build types (arm64-v8a is standard for modern devices)
android.archs = arm64-v8a

# (bool) Indicate whether the application is fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
