from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import requests

KEYCLOAK_URL = "http://localhost:8080/auth"
REALM = "your-realm"
CLIENT_ID = "your-client-id"
PUBLIC_KEY = "your-public-key"  # Lấy từ Keycloak

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token")

def verify_jwt(token: str = Depends(oauth2_scheme)) -> str:
    """
    Verify JWT token with Keycloak.
    """
    try:
        # Xác minh token
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            options={"verify_aud": False}
        )
        username = payload.get("preferred_username")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Kiểm tra quyền
        response = requests.get(
            f"{KEYCLOAK_URL}/admin/realms/{REALM}/users/{payload['sub']}",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=403, detail="Permission denied")

        return token
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))