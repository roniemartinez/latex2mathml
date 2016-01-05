from distutils.core import setup

setup(
        name='latex2mathml',
        version='1.0.3',
        packages=['latex2mathml'],
        url='https://github.com/Code-ReaQtor/latex2mathml',
        download_url='https://github.com/Code-ReaQtor/latex2mathml/tarball/1.0.3',
        license='MIT',
        author='Ronie Martinez',
        author_email='ronmarti18@gmail.com',
        description='Pure Python library for LaTeX to MathML conversion.',
        long_description=open('README').read(),
        keywords=[],
        classifiers=['Development Status :: 3 - Alpha',
                     'License :: OSI Approved :: MIT License',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Programming Language :: Python',
                     'Topic :: Scientific/Engineering :: Mathematics',
                     'Topic :: Text Processing :: Markup :: HTML',
                     'Topic :: Text Processing :: Markup :: LaTeX']
)
