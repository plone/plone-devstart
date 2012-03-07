from setuptools import setup, find_packages

version = '1.0'

long_description = open('README.txt').read()

setup(name='plone-customizations',
      version=version,
      description="Project-specific Plone customizations (not intended for independent release)",
      long_description=long_description,
      license='GPL',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'z3c.jbot',
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      )
