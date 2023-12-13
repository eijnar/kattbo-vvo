from setuptools import setup, find_packages

setup(
    name='kattbo_models',
    version='0.5.1',
    author='Johan Andersson',
    author_email='johan@morbit.se',
    description='Package containing the DB models for Kättbo VVO',
    url='https://github.com/eijnar/kattbo_vvo_web/common/',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'alembic'
    ],
)