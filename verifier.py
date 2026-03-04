import hashlib

def verify(file_path, expected_hash):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)

    digest = sha256.hexdigest()

    expected_hash = expected_hash.replace("sha256:", "")

    return digest == expected_hash
