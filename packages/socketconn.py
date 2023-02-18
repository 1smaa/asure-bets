import rsa
import os

CWD = os.getcwd()
PUB_PATH = os.path.join(CWD, "rsa", "public.pem")


def encode(obj: bytes) -> bytes:
    with open(PUB_PATH, mode="rb") as p:
        pk = p.read()
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(pk)
    return rsa.encrypt(message=obj, pub_key=public_key)
