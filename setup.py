from setuptools import setup, find_packages

setup(
    name="finance",
    version="1.0.0",
    description="Personal finance manager",
    author="Andrey Kiselev",
    author_email="kiselevandrew@yandex.ru",
    url="https://github.com/ezhk/finance/",

    packages=find_packages(exclude=["migrations"]),
)
