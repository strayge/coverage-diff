from setuptools import find_packages, setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='coverage-diff',
    version='0.0.5',
    description='Show/check coverage only for changed files (between any git branches)',
    long_description=readme,
    author='strayge',
    author_email='strayge@gmail.com',
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'coverage-diff = coverage_diff.main:main',
        ],
    },
    python_requires='>=3.6',
    install_requires=['coverage>=4'],
    data_files = [('', ['LICENSE'])],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
)
