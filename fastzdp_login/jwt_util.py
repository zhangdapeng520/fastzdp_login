import jwt


def get_jwt(data, secret="zhangdapeng520", algorithm="HS256"):
    if not isinstance(data, dict):
        return None
    return jwt.encode(data, secret, algorithm=algorithm)


def parse_jwt(data, secret="zhangdapeng520", algorithm="HS256"):
    if not isinstance(data, str):
        return None
    return jwt.decode(data, secret, algorithms=[algorithm])


if __name__ == '__main__':
    data = {"some": "payload"}
    token = get_jwt(data)
    print(token)
    data2 = parse_jwt(token)
    print(data2)
