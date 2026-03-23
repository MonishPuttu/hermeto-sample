from verifier import verify_sha256
import tempfile
import hashlib


def test_verify_sha256_success():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"hello world")
        f.flush()

        sha = hashlib.sha256(b"hello world").hexdigest()

        assert verify_sha256(f.name, f"sha256:{sha}")


def test_verify_sha256_failure():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"hello world")
        f.flush()

        wrong_hash = "sha256:0000000000000000000000000000000000000000000000000000000000000000"

        assert not verify_sha256(f.name, wrong_hash)