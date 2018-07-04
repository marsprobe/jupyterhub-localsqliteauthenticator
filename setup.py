#!/usr/bin/env python

from setuptools import setup

setup(name='sqliteauthenticator',
      version='0.1',
      description='SQLite Authenticator for Jupyterhub',
      author='sparkingarthur',
      license='MIT',
      author_email='sparkingarthur@163.com',
      url='https://github.com/sparkingarthur/jupyterhub-localsqliteauthenticator',
      packages=['sqliteauthenticator'],
      install_requires=[
        'jupyterhub',
		'pycrypto'
      ],
      )
import os
import shutil
oldname = './jupyterhub-users.db'
newname = '/etc/jupyterhub/jupyterhub-users.db'
if not os.path.exists(newname):
    shutil.copyfile(oldname,newname)
	
if not os.path.exists('/home/admin'):
    os.makedirs('/home/admin')