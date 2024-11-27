from setuptools import setup, find_packages

setup(
    name='materials',
    version='0.2.07',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'materials': ['data/materials1.db'],
    },
    install_requires=[],
)
