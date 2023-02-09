from setuptools import setup, find_packages


VERSION = '0.0.01'
DESCRIPTION = 'A general purpose Quality of Life package that includes some advanced modules.'

# Setting up
setup(
    name="pysmags",
    version=VERSION,
    author="FrostySmags",
    author_email="<frostysmags+dev@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'pyautogui', 'pyaudio'],
    keywords=['python', 'qol', 'threading', 'sockets', 'web'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
