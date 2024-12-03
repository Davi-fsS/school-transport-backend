from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from firebase_admin import credentials, auth
import firebase_admin
import os

class FirebaseAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        json_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        
        if json_path:
            cred = credentials.Certificate(json_path)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
        else:
            raise ValueError("Caminho para o arquivo de credenciais não fornecido na variável de ambiente GOOGLE_APPLICATION_CREDENTIALS.")
        
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/docs") or request.url.path.startswith("/user"):
            return await call_next(request)
        
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token não fornecido ou inválido.")
        
        id_token = token.split("Bearer ")[1]
        try:
            decoded_token = auth.verify_id_token(id_token)
            request.state.user = decoded_token
        except Exception as e:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado.")
        
        response = await call_next(request)
        return response
