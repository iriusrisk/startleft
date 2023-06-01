from setuptools import setup, find_packages

from startleft.startleft._version.local_scheme import guess_startleft_semver_suffix
from startleft.startleft._version.version_scheme import guess_startleft_semver

setup(
    name='startleft',
    description='Parse Infrastructure as Code files to the Open Threat Model format and upload them to IriusRisk',
    license='Apache2',
    author='Fraser Scott',
    author_email='fscott@iriusrisk.com',
    url='https://github.com/iriusrisk/startleft',
    keywords=['threat modeling', 'cyber security', 'appsec'],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'pyyaml==6.0',
        'jsonschema==4.17.3',
        'deepmerge==1.1.0',
        'jmespath==1.0.1',
        'python-hcl2==4.3.2',
        'requests==2.31.0',
        'fastapi==0.95.2',
        'python-multipart==0.0.6',
        'click==8.1.3',
        'uvicorn==0.22.0',
        'shapely==2.0.1',
        'vsdx==0.5.13',
        'python-magic==0.4.27',
        'setuptools==67.8.0',
        'defusedxml==0.7.1',
        'networkx==3.1',
        'pygraphviz==1.10'
    ],
    use_scm_version={
        'write_to': 'startleft/version.py',
        'version_scheme': guess_startleft_semver,
        'local_scheme': guess_startleft_semver_suffix,
        'git_describe_command': 'git describe --tags --long --match *[0-9]*'
    },
    extras_require={
        "setup": [
            "pytest-runner==6.0.0",
        ],
        "test": [
            'tox==4.5.2',
            'pytest==7.3.1',
            'responses==0.23.1',
            'deepdiff==6.3.0',
            'httpx==0.24.1',
            'pytest-mock==3.10.0',
            'coverage==7.2.7'
        ]
    },
    entry_points='''
        [console_scripts]
        startleft=startleft.startleft.cli.cli:cli
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
