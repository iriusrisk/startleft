from setuptools import setup, find_packages
from startleft.version import version

setup(
    name='IriusRisk StartLeft',
    description='Parse Infrastructure as Code files to the Open Threat Model format and upload them to IriusRisk',
    license='Apache2',
    version=version,
    author='Fraser Scott',
    author_email='fscott@iriusrisk.com',
    url='https://github.com/iriusrisk/startleft',
    keywords=['threat modeling', 'cyber security', 'appsec'],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'pyyaml',
        'jsonschema',
        'deepmerge',
        'jmespath',
        'lxml',
        'python-hcl2',
        'requests',
        'xmltodict',
        'fastapi',
        'python-multipart',
        'click',
        'uvicorn'
    ],
    extras_require={
        "setup": [
            "pytest-runner",
        ],
        "test": [
            'tox',
            'pytest',
            'responses'
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
