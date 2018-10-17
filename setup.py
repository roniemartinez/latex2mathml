from setuptools import setup

VERSION = '2.6.2'

setup(
    name='latex2mathml',
    version=VERSION,
    packages=['latex2mathml'],
    url='https://github.com/Code-ReaQtor/latex2mathml',
    download_url='https://github.com/Code-ReaQtor/latex2mathml/tarball/{}'.format(VERSION),
    license='MIT',
    author='Ronie Martinez',
    author_email='ronmarti18@gmail.com',
    description='Pure Python library for LaTeX to MathML conversion',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=[],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'License :: OSI Approved :: MIT License',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Topic :: Scientific/Engineering :: Mathematics',
                 'Topic :: Text Processing :: Markup :: HTML',
                 'Topic :: Text Processing :: Markup :: LaTeX'],
    package_data={'latex2mathml': ['unimathsymbols.txt']}
)
