from setuptools import setup, find_packages

setup(
    name='scientific_calculator',
    version='0.1.0',
    packages=find_packages(),  # Automatically find all packages (calc and tests)
    install_requires=[],  # No external package required
    # Remove tests_require and test_suite
    author='Your Name',  # Add your name
    author_email='sriram9217@example.com',  # Add your email
    description='A simple scientific calculator',  # Add description
    # Add setup for tests
    extras_require={
        "test": ["pytest"]  # We use pytest to test the package
    },
    package_dir={'': '.'},  # Add this line
    #add test option
    test_suite='tests',
)
