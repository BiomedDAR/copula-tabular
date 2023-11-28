from setuptools import setup, find_packages

# PyPA packaging instructions: https://packaging.python.org/tutorials/distributing-packages
# The setuptools command reference: https://setuptools.readthedocs.io/en/latest/setuptools.html#command-reference
# PyPI classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers 

setup(
    name='bdarpack',
    version='0.1.0',    
    description='A Python package for tabular synthetic data',
    url='https://biomeddar.github.io/copula-tabular/',
    author='MZ',
    author_email='tan_ming_zhen@bii.a-star.edu.sg',
    license='MIT',
    packages=find_packages(include=['bdarpack', 'bdarpack.*']),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'scipy',
        'openpyxl',
        'scikit-learn',
        'xlrd',
        'Unidecode'
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
