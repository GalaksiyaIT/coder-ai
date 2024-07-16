from setuptools import setup, find_packages

setup(
    name='coder-ai',
    version='1.0.0',
    author='Galaksiya Information Technologies (Dilşen Yıldar Havaylar, Mehmet Şahin)',
    author_email='info@galaksiya.com',
    description='A Python library for generating Java methods from unit tests using OpenAI\'s GPT model.',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.9',
)
