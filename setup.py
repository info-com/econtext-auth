from setuptools import setup, find_packages

data_files = [
    ('/etc/econtext/auth', [
        'econtextauth/engine/data/econtextauth.ini'
    ]),
    ('/etc/init.d', [
        'econtextauth/engine/data/econtextauth-engine'
    ])
]

dependency_links = [
    'git+ssh://git@github.com/info-com/econtext.util#egg=econtext.util-1.0.1',
    'git+ssh://git@github.com/jspalink/remodel#egg=remodel'
]

setup(
    name='econtextauth',
    version="0.0.3",
    author='Jonathan Spalink',
    author_email='jspalink@info.com',
    description='The eContext Auth engine provides authentication (and possibly authorization) services to eContext products',
    packages=find_packages(),
    data_files=data_files,
    install_requires=[
        'requests',
        'falcon >= 1.2',
        'gevent',
        'gunicorn',
        'rethinkdb',
        'remodel',
        'validate_email',
        'basicauth',
        'python-dateutil',
        'bcrypt',
        'econtext.util >= 1.0.1',
        'ujson',
        'python-jose'
    ],
    dependency_links=dependency_links,
    
    entry_points={
        'console_scripts': [
            'econtextauth-engine = econtextauth.engine.engine:main',
            'econtextauth-status = econtextauth.engine.bin.apistatus:main'
        ]
    }

)
