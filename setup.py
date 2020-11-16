from setuptools import setup, find_packages


def get_long_description():
    readme_file = 'README.md'
    with open(readme_file, encoding='utf-8') as handle:
        contents = handle.read()

    return contents


setup(
    name='RHaP',
    version='0.1',
    author='Mia Maric, Rhys Thomas, Michael D. Atkinson',
    author_email='mia.maric@manchester.ac.uk',
    description='A python library to analyse hydride morphology present in light optical and scanning electron micrographs.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    keywords='micrograph, zirconium, hydride',
    project_urls={
        'GitHub': 'https://github.com/miamaric12/Radial_Hydride_Code'
    },
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: IPython',
        'Framework :: Jupyter',
        'Framework :: Matplotlib'
    ],
    packages=find_packages(),
    package_data={'RHaP': ['data/example.bmp']},
    python_requires='>=3.5',
    install_requires=[
        'scipy',
        'numpy',
        'matplotlib>=3.0.0',
        'scikit-image',
        'numba',
        'skan',
        'toolz',
        'matplotlib_scalebar',
        'networkx',
        'jupyter'
        'pandas'
         

    ],
)
