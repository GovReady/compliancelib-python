from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='compliancelib',
      version='1.0.0',
      description='A python library for modeling IT Compliance',
      long_description=readme(),
      classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.0',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        # 'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Documentation',
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
          'defusedxml'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)