from setuptools import setup, find_packages

data_files = [
    ('/etc/econtext/auth', [
        'econtextauth/engine/data/econtextauth.ini'
    ])
]

setup(
    name='econtextauth',
    version="0.0.1",
    author='Jonathan Spalink',
    author_email='jspalink@info.com',
    description='The eContext Auth engine provides authentication (and possibly authorization) services to eContext products',
    packages=find_packages(),
    data_files=data_files,
    install_requires=[
        'requests',
        'falcon',
        'gevent',
        'gunicorn',
        'rethinkdb', 'remodel'
    ],
    
    entry_points={
        'console_scripts': [
            'econtextauth-engine = econtextauth.engine.engine:main'
        ]
    }

)
