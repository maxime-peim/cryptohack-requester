from setuptools import setup
setup(
    name='CHRequester',
    version='0.1',
    description='Cryptohack URL/NetCat request maker.',
    url='#',
    author='Maxime Peim',
    author_email='maxime.peim@gmail.com',
    license='MIT',
    packages=['ch_requester'],
    zip_safe=False,
    install_requires=[
       "requests >= 2.26"
   ],
)