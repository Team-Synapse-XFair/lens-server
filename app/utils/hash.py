import hashlib

BUF_SZ = 65536


def generateFileHash(file):
    sha256 = hashlib.sha256()

    with open(file, "rb") as f:
        while True:
            data = f.read(BUF_SZ)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


def verifyFileHash(file, hash):
    fileHash = generateFileHash(file)
    return fileHash == hash


def verifyFiles(file1, file2):
    file1Hash = generateFileHash(file1)
    file2Hash = generateFileHash(file2)
    return file1Hash == file2Hash
