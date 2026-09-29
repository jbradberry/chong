from setuptools import setup

setup(
    name='Chong',
    version='0.1dev',
    author='Jeff Bradberry',
    author_email='jeff.bradberry@gmail.com',
    packages=['chong'],
    entry_points={
        'jrb_board.games': 'chong = chong.chong:Board',
    },
    license='LICENSE',
    description="An implementation of the board game Chong.",
)
