#!/usr/bin/env python
# setup.py
from distutils.core import setup
import py2exe
import glob

opts = {
    "py2exe": {
        "includes": "cairo, pango, pangocairo, atk, gobject",
        }
    }

setup(
    name = "pyPowerOff",
    description = ".Simple python powerroff program",
    version = "1.2.3",
    author="Vitaly Tonkacheyev",
    author_email="thetvg@gmail.com",
    windows = [
        {"script": "pypoff",
        "icon_resources": [(1, "images/poweroff.ico")]
        }
    ],
    packages = ["pypoweroff"],
    options=opts,
    data_files=[("images", ["images/poweroff.png",
                "images/poweroff.ico", "images/tb_icon.png"]),
                "COPYING",
                ("glades", ["glades/powoff.glade"])
    ],
)
