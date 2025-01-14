


import os
import jwt
from pydantic import BaseModel
from fastapi import APIRouter,Request,HTTPException,Response,Depends
import requests
from src.project.default.domain.chat.infra.repository.chat import ChatRepository
from src.project.default.domain.chat.usecases.create_chat import CreateChat, InputCreateChatDto
from src.project.default.domain.chat.usecases.delete_chat import DeleteChat, InputDeleteChatDto
from src.project.default.domain.chat.usecases.get_all import GetAllChat, InputGetAllChatDto
from src.project.default.domain.chat.usecases.get_by_id import GetBydIdChat, InputGetBydIdChatDto
from sse_starlette.sse import EventSourceResponse
from src.project.default.domain.chat.usecases.interact_chat import InputInteractChatDto, InteractChat
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from src.infra.patterns.naive.vertexai_naive_pattern import VertexNaiveFactory
from src.infra.patterns.naive.vertexai_naive_config import VERTEXAI_NAIVE_CONFIG

chat_router = APIRouter()


KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL","https://sso.sandbox.enap.gov.br") 
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM","enap") 
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID","chat-secretaria-backend") 
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET","wj0aKlPHR852h9oyy5qt41VrHc70UPK6") 
KEYCLOAK_PUBLIC_KEY_URL = os.getenv("KEYCLOAK_PUBLIC_KEY_URL","https://sso.enap.gov.br/realms/enap/protocol/openid-connect/certs") 
EXPECTED_AUDIENCES = os.getenv("EXPECTED_AUDIENCES",["master-realm", "account"]  ) 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{KEYCLOAK_SERVER_URL}realms/{KEYCLOAK_REALM}/protocol/openid-connect/token")



def get_public_key(token):
    """Obtém a chave pública correta para o token, baseada no 'kid'."""
    try:
        response = requests.get(KEYCLOAK_PUBLIC_KEY_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Não foi possível obter a chave pública do Keycloak.")

        keys = response.json().get('keys', [])
        headers = jwt.get_unverified_header(token)

        for key in keys:
            if key['kid'] == headers['kid']:
                key_data = key['x5c'][0]
                key_pem = f"-----BEGIN CERTIFICATE-----\n{key_data}\n-----END CERTIFICATE-----"
                return key_pem

        raise HTTPException(status_code=401, detail="Chave pública correspondente não encontrada.")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido ou expirado: {str(e)}")

async def verify_token(token: str = Depends(oauth2_scheme)):

    public_key = get_public_key(token)

    try:
        # Decodificar sem verificar o audience
        payload = jwt.decode(token, public_key, algorithms=['RS256'], options={"verify_aud": False})

        # Verificar manualmente se o audience está na lista de audiences esperados
        if isinstance(payload.get("aud"), list):
            if not any(aud in EXPECTED_AUDIENCES for aud in payload["aud"]):
                raise HTTPException(status_code=401, detail="Token inválido: audience não corresponde.")
        else:
            if payload.get("aud") not in EXPECTED_AUDIENCES:
                raise HTTPException(status_code=401, detail="Token inválido: audience não corresponde.")

        return payload

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido ou expirado: {str(e)}")














class InputCreateChatDto(BaseModel):
    user_id: str

# @chat_router.post("/create_chat", status_code=201, dependencies=[Depends(verify_token)])
@chat_router.post("/create_chat", status_code=201)
async def create_chat(requests: Request, input: InputCreateChatDto, response: Response):

    try:
        
        usecase = CreateChat(repository=ChatRepository())
        
        input_usecase = InputCreateChatDto(
            user_id=input.user_id
        )
        response = usecase.execute(input=input_usecase)
        return response
    
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"{error}")



# @chat_router.get("/get_chat_by_id/{chat_id}", status_code=200,dependencies=[Depends(verify_token)])
@chat_router.get("/get_chat_by_id/{chat_id}", status_code=200)
async def get_chat_by_id(requests: Request, chat_id: str):
    try:
        repository = ChatRepository()
        usecase = GetBydIdChat(repository=repository)
        
        input_usecase = InputGetBydIdChatDto(
            chat_id=chat_id
        )
        response = usecase.execute(input=input_usecase)
        return response

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"{error}")



@chat_router.get("/get_all_chat/{user_id}", status_code=200)
async def get_all_chat(requests: Request, user_id: str):
    try:

        repository = ChatRepository()
        usecase = GetAllChat(repository=repository)

        input_usecase = InputGetAllChatDto(
            user_id=user_id 
        )
        response = usecase.execute(input=input_usecase)
        return response

    except HTTPException as e:
        raise e  # Retorna erros HTTP personalizados
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"{error}")



@chat_router.delete("/delete_chat/{chat_id}", status_code=200)
async def delete_chat(requests: Request, chat_id: str):

    try:
        repository = ChatRepository()
        usecase = DeleteChat(repository=repository)
        input_usecase = InputDeleteChatDto(
            chat_id=chat_id
        )
        usecase.execute(input=input_usecase)
    
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"{error}")




@chat_router.get("/stream")
async def stream(request: Request, query: str, chat_id: str):
    file = None
    
    repository = ChatRepository()
    
    pattern = VertexNaiveFactory.create(
        config=VERTEXAI_NAIVE_CONFIG
    )
    
    
    usecase_input = InputInteractChatDto(
        chat_id=chat_id,
        query=query,
        file=None,
    )
    usecase = InteractChat(
        repository=repository,
        pattern_service=pattern

    )


    def event_stream():
        try:
            for response in usecase.execute(input=usecase_input):
                yield response
        except Exception as e:
            yield f"event: error\ndata: {str(e)}\n\n"

    return EventSourceResponse(event_stream())
