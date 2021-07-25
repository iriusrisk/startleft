from setuptools import setup, find_packages

setup(
    name='IriusRisk StartLeft',
    description='Parse Infrastructure as Code files to the Open Threat Model format and upload them to IriusRisk',
    license='MIT',
    author='Fraser Scott',
    author_email='fscott@iriusrisk.com',
    url='https://github.com/iriusrisk/startleft',
    keywords=['threat modeling', 'cyber security', 'appsec'],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'click',
        'pyyaml',
        'jsonschema',
        'deepmerge',
        'jmespath',
        'lxml',
        'python-hcl2',
        'requests'
    ],
    use_scm_version=True,
    setup_requires=[
        "pytest-runner"
    ],
    tests_require=[
        'pytest'
    ],
    entry_points='''
        [console_scripts]
        startleft=startleft.cli:cli
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
