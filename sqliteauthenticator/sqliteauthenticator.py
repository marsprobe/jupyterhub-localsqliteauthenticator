#coding=utf-8
from jupyterhub.auth import Authenticator
from tornado import gen

import os
import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

import sqlite3

class prpcrypt():
    def __init__(self, key='jupyterhub'):
        self.key = key
        self.mode = AES.MODE_CBC
        self.length = 16

    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        count = len(text)
        #padding to length
        add = self.length - (count % self.length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        #turn to hex string
        return b2a_hex(self.ciphertext)
     

class SQLiteAuthenticator(Authenticator):
    def _verify_password(self,username,password):
        encryptor = prpcrypt()
        try:
            sql_cnn = sqlite3.connect(os.getenv('JUPYTERHUB_SQLITEDB_PATH'))
            # print("connect db sucessfully")
            cursor = sql_cnn.cursor()
            sql = ("SELECT password FROM users WHERE username = '{}'").format(username)  # select from the database
            # print(sql)
            cursor.execute(sql)
            user_password = cursor.fetchone()[0] # first to check the username
            #print(user_password)
            input_password = encryptor.encrypt(password).decode()
            if user_password == input_password:
                cursor.close()
                sql_cnn.close()
                return True
            else:
                cursor.close()
                sql_cnn.close()
                return False
        except:
            try:
                cursor.close()
                sql_cnn.close()
            except:
                pass
            finally:
                print("wrong database/username/password, "
                      "please check your JUPYTERHUB_SQLITEDB_PATH/username/password....")
                return False
    @gen.coroutine
    def authenticate(self, handler, data):
        username = data['username']
        passwd = data['password']
        if self._verify_password(username,passwd):
            return data['username']
        else:
            return None

