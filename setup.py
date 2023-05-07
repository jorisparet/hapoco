import os
import glob
from setuptools import setup
from hapoco._version import __version__

with open('README.md', 'r') as fh:
    readme = fh.read()
    
args = dict(name='hapoco',
            version=__version__,
            description='Trackpoint-like mouse control via webcam-recorded hand gestures',
            long_description=readme,
            long_description_content_type='text/markdown',
            author='Joris Paret',
            author_email='joris.paret@gmail.com',
            maintainer='Joris Paret',
            url='https://github.com/jorisparet/',
            keywords=['mouse', 'controller', 'webcam', 'camera',
                      'hand', 'pointer', 'cursor', 'accessibility',
                      'trackpoint', 'pointing stick'],
            packages=['hapoco',
                      'hapoco/bin',
                      'hapoco/controllers'],
            include_package_data=True,
            entry_points={'console_scripts':
                          ['hapoco = hapoco.bin.hapoco:main']},
            install_requires=['pyautogui', 'numpy', 'opencv-python', 'mediapipe'],
            license='GPLv3',
            classifiers=[
                'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                'Development Status :: 2 - Pre-Alpha',
                'Topic :: Scientific/Engineering :: Human Machine Interfaces',
                'Topic :: Scientific/Engineering :: Image Recognition',
                'Programming Language :: Python :: 3',
                'Operating System :: POSIX :: Linux',
                'Operating System :: Microsoft :: Windows',
                'Intended Audience :: End Users/Desktop',
                'Natural Language :: English']
)

setup(**args)