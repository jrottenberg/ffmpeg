from __future__ import annotations

from setuptools import setup


setup(
    name='pre_commit_placeholder_package',
    version='0.0.0',
    install_requires=['packaging'],
    entry_points={
        "console_scripts": ["generate_dockerfile = update:main"]
        }
)