import os
from setuptools import setup, find_packages, find_namespace_packages


DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
with open(os.path.join(DIR, 'requirements.txt')) as f:
    requirements = f.read()


setup(
    name='conversion_rate_model',
    version='1.0',
    description="Sellics conversion rate models",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author="Dmitry Kisler",
    author_email="admin@dkisler.com",
    license='MIT',
    packages=find_packages(include='conversion_rate_model*'),
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False)
