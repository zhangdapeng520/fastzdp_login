import jwt
import time


def get_jwt(data, secret="zhangdapeng520", algorithm="HS256"):
    """
    获取JWT Token
    """
    if not isinstance(data, dict):
        return None
    return jwt.encode(data, secret, algorithm=algorithm)


def parse_jwt(data, secret="zhangdapeng520", algorithm="HS256"):
    """
    解析JWT Token
    """
    if not isinstance(data, str):
        return None
    return jwt.decode(data, secret, algorithms=[algorithm])


def get_user_token(
        jwt_key,
        jwt_algorithm,
        userid,
        username=None,
        phone=None,
        jwt_token_expired=60 * 60 * 3,
):
    """
    生成用户的Token
    """
    # 生成Token
    now_time = time.time()
    data = {
        "username": username,
        "phone": phone,
        "id": userid,
        "time": now_time,
        "expired": now_time + jwt_token_expired,
    }
    access_token = get_jwt(data, jwt_key, jwt_algorithm)
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == '__main__':
    data = {"some": "payload"}
    token = get_jwt(data)
    print(token)
    data2 = parse_jwt(token)
    print(data2)
