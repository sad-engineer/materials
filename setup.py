from setuptools import setup, find_packages

setup(
    name='materials',
    version='0.2.09',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'materials': ['data/materials1.db'],
    },
    install_requires=[
        'SQLAlchemy>=2.0.0',
        'alembic>=1.12.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
    ],
    python_requires='>=3.8',
    description='Пакет Python для работы с базой данных материалов',
    author='sad-engineer',
    author_email='korenyuk.a.n@mail.ru',
    url='https://github.com/sad-engineer/materials',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Materials Science',
    ],
)