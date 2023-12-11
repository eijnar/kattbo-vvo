from setuptools import setup, find_packages

setup(
    name='kattbo_db_models',
    version='0.1',
    author='Johan Andersson',
    author_email='johan@morbit.se',
    description='Package containing the DB models for Kättbo VVO',
    url='https://github.com/eijnar/kattbo_vvo_web',
    packages=find_packages(),
    install_requires=[
        'Flask==3.0.0',
        'Flask-WTF==1.2.1',
        'Flask-SQLAlchemy==3.1.1'
    ],
)