from setuptools import setup, find_packages

setup(
    name='IriusRisk StartLeft',
    description='Parse Infrastructure as Code files to the Open Threat Model format and upload them to IriusRisk',
    license='Apache2',
    author='Fraser Scott',
    author_email='fscott@iriusrisk.com',
    url='https://github.com/iriusrisk/startleft',
    keywords=['threat modeling', 'cyber security', 'appsec'],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'pyyaml==6.0',
        'jsonschema==4.14.0',
        'deepmerge==1.0.1',
        'jmespath==1.0.1',
        'lxml==4.9.1',
        'python-hcl2==3.0.5',
        'requests==2.28.1',
        'xmltodict==0.13.0',
        'fastapi==0.78.0',
        'python-multipart==0.0.5',
        'click==8.1.3',
        'uvicorn==0.18.3',
        'shapely==1.8.4',
        'vsdx==0.5.10',
        'python-magic==0.4.27'
    ],
    use_scm_version=True,
    extras_require={
        "setup": [
            "pytest-runner==6.0.0",
        ],
        "test": [
            'tox==3.25.1',
            'pytest==7.1.2',
            'responses==0.21.0',
            'deepdiff==5.8.1'
        ]
    },
    entry_points='''
        [console_scripts]
        startleft=startleft.cli:cli
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
