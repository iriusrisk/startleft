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
        'python-hcl2==4.3.0',
        'requests==2.28.2',
        'fastapi==0.93.0',
        'python-multipart==0.0.5',
        'click==8.1.3',
        'uvicorn==0.20.0',
        'shapely==2.0.1',
        'vsdx==0.5.13',
        'python-magic==0.4.27',
        'setuptools==65.5.1',
        'defusedxml==0.7.1',
        'networkx==3.0',
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
            'tox==4.4.6',
            'pytest==7.2.2',
            'coverage==7.2.3',
            'responses==0.22.0',
            'deepdiff==6.2.3',
            'httpx==0.23.3'
        ],
        "doc": [
            'mkdocs-material==9.1.1',
            'pymdown-extensions==9.10',
            'mkdocs-glightbox==0.3.1'
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
