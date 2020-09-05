import setuptools

setuptools.setup(
    name='kivyhelper',
    url='https://github.com/Larquebus/kivyhelper',
    author='Chris Larabee',
    author_email='quill9@gmail.com',
    packages=[
        'kivyhelper',
        'kivyhelper.scripts',
        'kivyhelper.widgets',
        'kivyhelper.scripts.build_assets',
        'kivyhelper.scripts.new_app',
    ],
    install_requires=[
        'docutils',
        'pygments',
        'pypiwin32',
        'kivy_deps.sdl2==0.1.*',
        'kivy_deps.glew==0.1.*',
        'kivy_deps.gstreamer==0.1.*',
        'kivy==1.11.1',
        'jsonlines',
        'amanuensis @ git+https://github.com/Larquebus/'
        'Amanuensis#egg=amanuensis'
    ],
    version='0.2.4',
    license='Creative Commons',
    description=('A suite of pre-built widgets and helper scripts to '
                 'facilitate building a Kivy-based app. '),
    long_description=open('README.md').read()
)
