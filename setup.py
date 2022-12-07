from setuptools import setup

setup(
    name='pytrevl',
    version='0.0.2',    
    description='Python interface to handle and modify TREVL backed visualizations',
    url='https://github.com/trendence/pytrevl',
    author='Trendence Institut',
    author_email='valentin.lorenzen@trendence.com',
    license='BSD 2-clause',
    packages=['pytrevl', 'pytrevl.api'],
    install_requires=['numpy>=1.23.5'
                      'pandas>=1.5',        
                      'python-highcharts>=0.4.2',    
                      'pyyaml>=6.0'              
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.9',
    ],
)