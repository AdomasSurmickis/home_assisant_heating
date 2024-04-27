from setuptools import setup

setup(
    name="my_custom_component",
    version="0.1.0",
    description="Custom component for Home Assistant",
    packages=["my_custom_component"],
    install_requires=[
        "homeassistant>=2022.1.0",
        "aiohttp>=3.7.4"
    ],
)
