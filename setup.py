#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for Synology DDNS
"""

from pathlib import Path

from setuptools import setup, find_packages

# Read version from VERSION file
version_file = Path(__file__).parent / "VERSION"
with open(version_file, "r", encoding="utf-8") as f:
    version = f.read().strip()

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
with open(readme_file, "r", encoding="utf-8") as f:
    long_description = f.read()

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
with open(requirements_file, "r", encoding="utf-8") as f:
    requirements = [
        line.strip() for line in f if line.strip() and not line.startswith("#")
    ]

setup(
    name="synology-ddns",
    version=version,
    author="Rex Zhou",
    author_email="879582094@qq.com",
    description="Synology DSM DDNS custom provider for CloudFlare",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChowRex/synology-ddns",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "synology_ddns": ["html/*.html", "static/**/*"],
    },
    entry_points={
        "console_scripts": [
            "synology-ddns=synology_ddns.main:app",
        ],
    },
)
