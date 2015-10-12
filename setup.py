from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='compliancelib',
      version='0.2.1',
      description='A python library of IT Compliance Standards',
      long_description=readme(),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='compliance FISMA DICAP PCI',
      url='http://github.com/govready/compliancelib-python',
      author='Greg Elin',
      author_email='gregelin@govready.com',
      license='Apache License 2.0',
      packages=['compliancelib'],
      package_data={
      'compliancelib': ['data/*.xml', 'data/*.pdf', 'xsl/*.xsl'],
      },
      include_package_data=True,
      install_requires=[
          'markdown',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/compliancelib-joke'],
      zip_safe=False)