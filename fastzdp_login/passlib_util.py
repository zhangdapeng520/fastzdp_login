from passlib.hash import pbkdf2_sha256


def hash_256(secret_str):
    """生成密码"""
    return pbkdf2_sha256.hash(secret_str)


def verify_256(secret_str, hash_str):
    """校验密码"""
    return pbkdf2_sha256.verify(secret_str, hash_str)


if __name__ == '__main__':
    secret_str = "toomanysecrets"
    hash_str = hash_256(secret_str)
    print(hash_str)
    print(verify_256(secret_str, hash_str))
    print(verify_256(secret_str * 2, hash_str))
