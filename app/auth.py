from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError
from settings import settings

ACCESS_TOKEN_EXPIRE = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
REFRESH_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + ACCESS_TOKEN_EXPIRE
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "sub": str(data.get("user_id"))
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        return "expired"
    except JWTError:
        return None
    

def create_refresh_token(data: dict):
    """
    Refresh token yaratadi.
    data: dict (masalan {"user_id": 1, "role": 2})
    return: JWT token (str)
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token