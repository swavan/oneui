from setuptools import setup

APP = ['main.py']
DATA_FILES = ["assets", "templates", "data"]
OPTIONS = {
    'argv_emulation': False,
    "compressed": True,
    "optimize": 1,
    'iconfile': 'assets/images/logo/swavan_one_ui.icns',
    'plist': 'Info.plist',
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
