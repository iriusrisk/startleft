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
        'click',
        'pyyaml',
        'jsonschema',
        'deepmerge',
        'jmespath',
        'lxml',
        'python-hcl2',
        'requests',
        'xmltodict',
        'setuptools_scm',
        'fastapi',
        'python-multipart'
    ],
    use_scm_version=True,
    extras_require={
        "setup": [
            "pytest-runner",
        ],
        "test": [
            'tox',
            'pytest'
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
