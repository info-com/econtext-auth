from setuptools import setup, find_packages

data_files = [
    ('/etc/econtextauth', [
        'src/econtextauth/data/econtextauth.ini'
    ]),
    #('/etc/init.d', [
    #    'econtextauth/engine/data/econtextauth-engine'
    #])
]

dependency_links = [
    'git+ssh://git@github.com/info-com/econtext.util#egg=econtext.util-1.0.11'
]

setup(
    name='econtextauth',
    version="2.0.0",
    author='Jonathan Spalink',
    author_email='jspalink@econtext.ai',
    description='A user management and authentication service written in Python with a default included database mapper to Neo4j',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    data_files=data_files,
    install_requires=[
        'requests',
        'falcon >= 1.4.0,< 2',
        'gevent',
        'gunicorn',
        'basicauth',
        'bcrypt',
        'econtext.util == 1.0.11',
        'ujson',
        'neomodel',
        'python-jose'  #jwt
    ],
    dependency_links=dependency_links,
    
    entry_points={
        'console_scripts': [
            'econtextauth-engine = econtextauth.bin.engine:main',
            'econtextauth-status = econtextauth.bin.apistatus:main'
        ]
    }

)
