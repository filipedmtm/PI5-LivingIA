from setuptools import setup, find_packages

setup(
    name="pi5-livingia",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'dash',
        'pandas',
        'numpy',
        'scikit-learn',
        'plotly'
    ]
) 