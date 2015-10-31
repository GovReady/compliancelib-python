from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='compliancelib',
      version='0.7.2',
      description='A python library of IT Compliance Standards',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.0',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='compliance FISMA DICAP PCI',
      url='http://github.com/govready/compliancelib-python',
      author='Greg Elin',
      author_email='gregelin@govready.com',
      license='Apache License 2.0',
      packages=['compliancelib'],
      package_data={
      'compliancelib': ['data/*.xml', 'data/*.pdf', 'data/dependencies/*.txt'],
      },
      include_package_data=True,
      install_requires=[
          'markdown',
          'pyyaml',
          'graphviz',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)