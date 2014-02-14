from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

try:
    import py2exe
except ImportError:
    pass

from dose import metadata

setup(name = metadata.pypi_name,
      version = metadata.version,
      download_url = metadata.download_url,
      packages = ['dose', 
                  'dose.copads'],
      description = metadata.description,
      long_description = metadata.long_description,
      author = metadata.maintainer,
      author_email = metadata.email,
      url = metadata.project_website,
      license = metadata.short_license,
      platforms = metadata.platforms,
      classifiers = metadata.trove_classifiers,
      console = ['dosecmd.py']
     )
