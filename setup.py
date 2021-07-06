from setuptools import setup, find_packages


with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='jackhammer',
   version='0.1',
   description='A minimal website revision system (CMS, if you must)',
   long_description=long_description,
   author='Odysseas Neslechanidis',
   author_email='odnes@tiptheiceberg.com',
   url='http://github.com/odnes/jackhammer.git',
   include_package_data=True,
   zip_safe=False,
   # This is for .py modules meant to reside in site-packages
   #py_modules=['']
   packages=['jackhammer'],
   install_requires=['Flask', 'Flask-SQLAlchemy', 'Markdown', 'python-dotenv']
)
