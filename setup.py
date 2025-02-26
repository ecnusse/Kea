# This file is a script to build and distribute Python packages
# set up basic requirements for Kea
from setuptools import setup, find_packages, findall
import os
import sys


install_requires = ["networkx",
        "Pillow",
        "uiautomator2==3.2.2",
        "androguard==4.0.0",
        "attrs",
        "opencv-python",
        "coloredlogs",
        "hypothesis",
        "hmdriver2",
        "pyyaml",
        "openai",
        "rtree"
    ]

if sys.version_info >= (3, 12):
    install_requires.append("setuptools")


setup(
    name="kea",
    packages=find_packages(include=["kea"]),
    # this must be the same as the name above
    version="2.0.3",
    description="A property-based testing tool for mobile apps.",
    author="Yiheng Xiong, XiangChen Shen, Xixiang Liang, Ting Su",
    license="MIT",
    author_email="yihengx98@gmail.com",
    url="https://github.com/ecnusse/Kea",  # use the URL to the github repo
    # download_url='https://github.com/honeynet/droidbot/tarball/1.0.2b4',
    keywords=["GUI testing", "Property-based Testing", "Functional Bugs"],  # arbitrary keywords
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python",
    ],
    entry_points={
        "console_scripts": [
            # the entry point of Kea
            "kea=kea.start:main",
        ],
    },
    package_data={
        "kea": [os.path.relpath(x, "kea") for x in findall("kea/resources/")]
    },
    # androidviewclient does not support pip install, thus you should install it with easy_install
    install_requires=install_requires
)
