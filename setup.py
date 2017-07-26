from setuptools import setup

setup(
    name='course_scheduler',
    version='0.1',
    packages=['course_scheduler',],
    license='MIT License',
    description='Carleton University course scheduling tool',
    long_description=open('README.md').read(),
    install_requires=[ 'requests' ],
    entry_points={
        'gui_scripts': [
            'course_scheduler = course_scheduler.__main__:main'
        ]
    },
)
