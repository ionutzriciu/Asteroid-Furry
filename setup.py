from setuptools import setup, find_packages

setup(
    name="AsteroidFury",  
    version="1.0.0",
    description="A Python game where the player shoots meteors.",  
    author="Ionut Riciu", 
    author_email="ionut.riciu92@gmail.com", 
    packages=find_packages(),  
    include_package_data=True, 
    install_requires=[
        "pygame>=2.0.0",  
    ],
    entry_points={
        'console_scripts': [
            'asteroidfury=engine.main:main',  
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',  
)
