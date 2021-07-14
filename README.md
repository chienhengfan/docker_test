encrypt
這是關於AES/CBC/PKCS7協定的加密解密程式

目的:串外部web api時因為怕資料洩漏，因此需要對資料加密

流程

加密 : string -> <> -> byte -> <> -> string(encrypt) 解密 : string(encrypt) -> <> -> byte -> <> -> string

報錯: 1.TypeError: Object type <type 'unicode'> cannot be passed to C code solution : str.encode()

2.padding is incorrect solution: making padding vector can be divided by AES.blocksize(因為AES是採取一個區塊一個區塊加密的形式

主要參考網站:

https://www.jianshu.com/p/d18c13681bbc

https://gist.github.com/olooney/1498025