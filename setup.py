"""Setup for Gjenta.
"""
from pathlib import Path

from setuptools import setup, find_packages

setup(
    name='img2segy',
    version="1.1.0",
    packages=find_packages('src'),
    author='Sixty North AS',
    author_email='rob@sixty-north.com',
    description='A tool for converting images to SEG-Y',
    license='MIT License',
    keywords='',
    package_dir={'': 'src'},
    url='http://bitbucket.com/sixty-north/gjenta',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
    ],
    platforms=['any'],
    include_package_data=True,
    install_requires=[
        "segpy",
        "click",
        'numpy',
        "pillow",
        "exit_codes",
        "euclidian",
        "toml",
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'test': [
            'hypothesis',
            'pytest',
            'tox',
        ],
        'dev': ['bumpversion', 'flake8', 'autopep8', 'twine'],
        'doc': ['sphinx', 'sphinx-rtd-theme']
    },
    entry_points={
        'console_scripts': [
            'img2segy = img2segy.cli:cli',
        ],
    },
    long_description=Path('README.rst').read_text(encoding='utf-8'),
)
