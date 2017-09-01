from distutils.core import setup

VERSION = open('VERSION').read()

setup(
    name='latex2mathml',
    version=VERSION,
    packages=['latex2mathml'],
    url='https://github.com/Code-ReaQtor/latex2mathml',
    download_url='https://github.com/Code-ReaQtor/latex2mathml/tarball/{}'.format(VERSION),
    license='MIT',
    author='Ronie Martinez',
    author_email='ronmarti18@gmail.com',
    description='Pure Python library for LaTeX to MathML conversion.',
    long_description=open('README.rst').read(),
    keywords=[],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: OSI Approved :: MIT License',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3',
                 'Topic :: Scientific/Engineering :: Mathematics',
                 'Topic :: Text Processing :: Markup :: HTML',
                 'Topic :: Text Processing :: Markup :: LaTeX'],
    package_data={'latex2mathml': ['unimathsymbols.txt']}
)
