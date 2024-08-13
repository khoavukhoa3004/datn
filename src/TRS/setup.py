from os import name
from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    # include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==3.0.2',
        'Flask-SQLAlchemy==3.1.1',
        # 'kafka-python>=2.0.2',
        'numpy==1.26.4',
        'email-validator',
        'pandas',
        # 'psycopg2',
        'psycopg2-binary',
        'scikit-learn',
        'SQLAlchemy>=1.4.5',
        'SQLAlchemy-Utils>=0.36.8',
        'python-dotenv>=0.15.0',
        'gunicorn>=20.1.0',
        # 'Flask-Migrate>=2.7.0',
        'Flask-Cors',
        'pytest==6.2.5',
        'scikit-learn',
        # 'scikit-surprise==1.1.3',
        'APScheduler', 
        'matplotlib',
        'keras',
        'tensorflow',
        # "blinker==1.7.0"
    ],
)