from setuptools import setup, find_packages

# PyPA packaging instructions: https://packaging.python.org/tutorials/distributing-packages
# The setuptools command reference: https://setuptools.readthedocs.io/en/latest/setuptools.html#command-reference
# PyPI classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers 
# create source dist: py -m build --sdist
# create wheel: py -m build --wheel
# upload distribution to testpypi: twine upload --repository-url https://test.pypy.org/legacy/ dist/<pyexample-0.1.0.tar.gz> or *
# upload distribution: twine upload dist/*
# python -m twine upload -u __token__ -p pypi-**(insert password here) dist/*
# username = __token__, password = <token>

# python -m pip install -U pkginfo twine // run this line when throws error that involves versioning


setup(
    name='bdarpack',
    version='0.1.7',    
    description='A Python package for tabular synthetic data',
    url='https://biomeddar.github.io/copula-tabular/',
    author='MZ Tan',
    author_email='tan_ming_zhen@bii.a-star.edu.sg',
    license='MIT',
    # license='BSL-1.1',
    keywords='synthetic data copula',
    packages=find_packages(include=['bdarpack', 'bdarpack.*']),
    install_requires=[ #comment out when uploading in testpypi
        'pandas',
        'numpy',
        'matplotlib',
        'scipy',
        'openpyxl',
        'scikit-learn',
        'xlrd',
        'Unidecode'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        # 'License :: Free for non-commercial use',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
