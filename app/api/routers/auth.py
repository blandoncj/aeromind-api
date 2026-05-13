from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.api.dependencies import get_login_use_case, get_register_use_case
from app.application.dtos.auth_dtos import LoginUserInput, RegisterUserInput
from app.application.use_cases.auth.login_user import LoginUserUseCase
from app.application.use_cases.auth.register_user import RegisterUserUseCase
from app.domain.enums.document_type import DocumentType
from app.domain.enums.gender import Gender
from app.domain.enums.role import Role

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    first_lastname: str
    second_lastname: str | None = None
    document_type: DocumentType
    document_number: str
    nationality_code: str
    gender: Gender
    phone_number: str
    role: Role = Role.PASSENGER


class RegisterResponse(BaseModel):
    user_id: UUID
    email: str
    first_name: str
    first_lastname: str
    role: Role


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: UUID
    email: str
    role: Role


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    body: RegisterRequest,
    use_case: Annotated[RegisterUserUseCase, Depends(get_register_use_case)],
) -> RegisterResponse:
    result = await use_case.execute(RegisterUserInput(
        email=body.email,
        password=body.password,
        first_name=body.first_name,
        first_lastname=body.first_lastname,
        second_lastname=body.second_lastname,
        document_type=body.document_type,
        document_number=body.document_number,
        nationality_code=body.nationality_code,
        gender=body.gender,
        phone_number=body.phone_number,
        role=body.role,
    ))
    return RegisterResponse(
        user_id=result.user_id,
        email=result.email,
        first_name=result.first_name,
        first_lastname=result.first_lastname,
        role=result.role,
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    use_case: Annotated[LoginUserUseCase, Depends(get_login_use_case)],
) -> LoginResponse:
    result = await use_case.execute(LoginUserInput(
        email=body.email,
        password=body.password,
    ))
    return LoginResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        user_id=result.user_id,
        email=result.email,
        role=result.role,
    )
