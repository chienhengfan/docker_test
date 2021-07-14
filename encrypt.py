#Python 3.6.13 :: Anaconda, Inc.
#AES/CBC/PKCS7

#reference:
#https://www.jianshu.com/p/d18c13681bbc
#https://gist.github.com/olooney/1498025



import base64
from Crypto.Cipher import AES
import json



class AESCipher:

    def __init__(self, key):
        self.key = key #16位
        self.iv = self.key

    def __pad(self, text):
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = ' '
        return (str(text) + pad * amount_to_pad).encode('utf-8')

    def __unpad(self, text):
        padding_number = ord(text[-1])    #return ascii uncode,應該是這邊解碼encode不同
        print(padding_number)
        if padding_number >= AES.block_size:
            return text
        else:
            if all(padding_number == ord(c) for c in text[-padding_number:]):
                return text[0:-padding_number]
            else:
                return text

    def encrypt(self, raw):
        """加密"""
        raw = self.__pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        """解密"""
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv )
        return self.__unpad(cipher.decrypt(enc).decode("utf-8"))




class ReadFile:
    def read_json(location,file):
        with open(location+file,'r') as f:
            text = f.read()
        return text




if __name__ == '__main__':

    #read key & clear_data
    key = ReadFile.read_json('D:/secret/','key.txt')
    clear_data = ReadFile.read_json('D:/secret/','plain.txt')

    #encode & decode test
    e = AESCipher(key.encode('utf-8'))
    enc_str = e.encrypt(clear_data)
    dec_str = e.decrypt(enc_str)
    print('enc_str: ' + enc_str.decode())
    print('dec str: ' + dec_str)

    dec_str2 = e.decrypt('/k3FHYD8RHSnXRShqUncU1E2xzFlsbKuJsVUCrgp0WsL71KjiMcMZbs5Byh2U4NgakUmc280/E1US1TbkTq/Tcrg2rZ1R8y/QGblrH/bcmU=')
    print('decode2 : ' + dec_str2)
