from setuptools import setup, find_packages

setup(
    name="network",
    version="0.1.0",
    # packages=["project4", "network", "accounts"],
    packages=find_packages(),
    install_requires=[
        "django",
        "django-widget-tweaks",
        "django-extensions"
    ],
)