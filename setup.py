from setuptools import setup

setup(
    name='pytrevl',
    version='0.0.2',    
    description='Python interface to handle and modify TREVL backed visualizations',
    url='https://github.com/trendence/pytrevl',
    author='Trendence Institut GmbH',
    author_email='valentin.lorenzen@trendence.com',
    license='MIT License',
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
        'Programming Language :: Python :: 3.9',
    ],
)