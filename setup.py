from setuptools import setup, find_packages

README = 'Metugenetic'

requires = ['numpy']


def packages(namespace, dir):
    packages = find_packages(dir)
    return [f'{namespace}.{package}' for package in packages]


setup(name='metugenetic',
      version='1.0.0',
      description=README,
      long_description=README,
      package_dir={'': 'source'},
      classifiers=[
          "Programming Language :: Python",
      ],
      author='Yasha Rise',
      packages=packages('metugenetic', 'source/metugenetic'),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      )