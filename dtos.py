from dataclasses import dataclass


@dataclass
class CreateUser:
    user_id: int
    username: str
    fullname: str
    photo_url: str
    referred_by_code: str


@dataclass
class PaginationRequest:
    pass
