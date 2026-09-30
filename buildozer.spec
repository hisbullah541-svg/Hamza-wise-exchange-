[app]

# (str) Title of your application
title = Hamza Wise Exchange

# (str) Package name
package.name = hamzawiseexchange

# (str) Package domain (needed for android packaging)
package.domain = org.hamza

# (str) Source files to include (let it include python files)
source.include_exts = py,png,jpg,json

# (str) Where source is stored (REQUIRED)
source.dir = .

# (str) Version of the application (REQUIRED)
version = 0.1

# (list) Application requirements
# Since your script only uses Python standard libraries (urllib, json, decimal), python3 is enough
requirements = python3

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android architectural build types
android.archs = arm64-v8a

# (bool) Indicate whether the application is fullscreen or not
fullscreen = 0
