from setuptools import setup

setup(
    name='bellmanford',
    version='0.1',
    description='''
        Convenience wrappers for the Bellman-Ford routines in NetworkX
        (https://networkx.github.io).
    ''',
    url='https://github.com/nelsonuhan/bellmanford',
    author='Nelson Uhan',
    author_email='nelson@uhan.me',
    license='BSD',
    packages=['bellmanford'],
    install_requires=['networkx'],
)
