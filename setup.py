import os

from setuptools import setup, find_packages

requires = [
    'python-poppler',
]

tests_require = [
    'pytest',  # includes virtualenv
    'pytest-cov',
]

setup(name='pdfextract',
      version='0.1.0',
      description='pdfextract',
      long_description='',
      classifiers=[
          "Programming Language :: Python",
      ],
      author='',
      author_email='',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [console_scripts]
      text2md = pdfextract.scripts.text2md:main
      md2xml = pdfextract.scripts.md2xml:main
      """,
)
