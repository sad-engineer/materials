from setuptools import setup, find_packages

setup(
    name='materials',
    version='0.2.03',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'materials': ['data/materials.db'],
    },
    install_requires=[],
)
