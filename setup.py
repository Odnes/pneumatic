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
   url='http://www.tiptheiceberg.com/',
   include_package_data=True,
   zip_safe=False,
   py_modules=['config', 'models', 'instantiate_db', 'wsgi_frontend', 'wsgi_admin'],
   packages=find_packages(),
   install_requires=['Flask', 'Flask-SQLAlchemy', 'Markdown', 'python-dotenv']
)
