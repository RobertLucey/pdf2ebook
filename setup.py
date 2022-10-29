from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'pdf2text',
    'ebooklib',
    'bs4'
)

setup(
    name='pdf2ebook',
    version='1.0.0',
    python_requires='>=3.6',
    description='PDF to ebook',
    author='Robert Lucey',
    url='https://github.com/RobertLucey/pdf2ebook',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'convert = pdf2ebook.bin.convert:main'
        ]
    }
)
