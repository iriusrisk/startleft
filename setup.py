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
    python_requires='>= 3.9, <= 3.12',
    install_requires=[
        'pyyaml==6.0.1',
        'jsonschema==4.19.0',
        'deepmerge==1.1.0',
        'jmespath==1.0.1',
        'python-hcl2==4.3.2',
        'requests==2.32.3',
        'fastapi>=0.115.2,<0.116.0',
        'python-multipart==0.0.18',
        'click==8.1.7',
        'uvicorn==0.23.2',
        'vsdx==0.5.13',
        'python-magic==0.4.27',
        'setuptools==70.3.0',
        'setuptools-scm==8.1.0',
        'defusedxml==0.7.1',
        'networkx==3.1',
        'dependency-injector==4.41.0',
        'google-re2==1.0',
        'xmlschema==2.5.0',
        'word2number==1.1',
        # Do not upgrade pygraphviz unless security issues because it is heavily dependent on the underlying OS
        'pygraphviz==1.10',
        # Be careful with numpy upgrades as it can break other dependencies
        'numpy==1.26.4',
        # Install shapely the last so it does not try to install an invalid numpy version
        'shapely==2.0.1'
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
            'tox==4.11.1',
            'pytest==7.4.1',
            'responses==0.23.3',
            'deepdiff==6.4.1',
            'httpx==0.24.1',
            'pytest-mock==3.11.1',
            'coverage==7.3.1'
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
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ]
)
