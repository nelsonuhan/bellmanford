import setuptools

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = ''

setuptools.setup(
    name='bellmanford',
    version='0.2.1',
    description='''
        Small extensions of the Bellman-Ford routines in NetworkX, primarily
        for convenience (https://networkx.github.io).
    ''',
    long_description=long_description,
    url='https://github.com/nelsonuhan/bellmanford',
    author='Nelson Uhan',
    author_email='nelson@uhan.me',
    license='BSD',
    packages=['bellmanford'],
    install_requires=['networkx'],
)
