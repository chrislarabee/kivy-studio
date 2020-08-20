from setuptools import setup

setup(
    name='kivyhelper',
    url='https://github.com/Larquebus/kivyhelper',
    author='Chris Larabee',
    author_email='quill9@gmail.com',
    packages=['kivyhelper', 'scripts', 'widgets'],
    install_requires=[],
    version='0.1.0',
    license='Creative Commons',
    description=('A suite of pre-built widgets and helper scripts to '
                 'facilitate building a Kivy-based app. '),
    long_description=open('README.md').read()
)
