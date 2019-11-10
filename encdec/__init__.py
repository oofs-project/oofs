import base64

def encodeFile(filepath):
    with open(filepath, "rb") as f:
        encodedFile = base64.b64encode(f.read())
        return encodedFile


def decodeFile(b64, filepath):
    writeTo = open(filepath, 'wb')
    decFile = base64.b64decode(b64)
    writeTo.write(decFile)
    return decFile

def encodeBits(b64):
    encodedBits = base64.b64encode(b64)
    return encodedBits