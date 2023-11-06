from setuptools import setup, find_packages

# might be a silly thing todo?
def read_requirements():
    with open('requirements.txt', 'r') as req:
        content = req.read()
        requirements = content.split('\n')

    return requirements

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author="Sebastian Schiller-Stoff",
    author_email="SebastianStoff@gmx.at",
    description="Small cli - tool to support GAMS5 local development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name='gams5-client',
    version='0.1.0',
    packages=find_packages(exclude=("tests")),
    include_package_date=True,
    install_requires=read_requirements(),
    # entry_points="""
    #     [console_scripts]
    #     bock=bock.cli:cli
    # """,
    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.10'
    ],
    python_requires='>=3',
)