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
from src.infra.patterns.naive.vertexai_naive_pattern import VertexNaiveFactory
from src.infra.patterns.naive.vertexai_naive_config import VERTEXAI_NAIVE_CONFIG
from src.core.components.knowledge.agent.pre_chat.pre_chat import PreChat
from src.infra.components.embedding.vertexai.embedding import VertexEmbeddings
knowledge_router = APIRouter()

config = VERTEXAI_NAIVE_CONFIG()

@knowledge_router.post("/pre-chat/",status_code=200)
async def pre_chat(requests: Request):
    try:
        embedding_component = VertexEmbeddings(
            model=config.EMBEDDING_MODEL,
            project=config.PROJECT
        )
        
        
        usecase = PreChat(embedding_component=embedding_component, input_file_component=input_file_component, vector_store_component=vector_store_component)

        input_usecase = InputGetAllChatDto(
            user_id=user_id 
        )
        response = usecase.execute(input=input_usecase)
        return response

    except HTTPException as e:
        raise e  # Retorna erros HTTP personalizados
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"{error}")
