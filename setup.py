from setuptools import setup, find_packages

setup(
    name='climate_analysis',
    version='0.1.0',
    packages=find_packages(),
    description='A package for data loading, plotting, statistical tests, and forecasting climate data.',
    author='Evan Bouillet',
    author_email='evanbouillet@gmail.com',
    url='https://github.com/yourusername/climate_analysis',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)