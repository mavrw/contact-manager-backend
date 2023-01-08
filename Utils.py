import hashlib


def hash_contact_photo(s: str):
    photo_hash = hashlib.md5(s.encode())
    return photo_hash.hexdigest()