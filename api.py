import dataclasses
import requests
from dtos import CreateUser, PaginationRequest


class Api:
    def __init__(self, server_url: str) -> None:
        self.server_url = server_url

    def register_user(self, create_user: CreateUser):
        res = requests.post(
            f"{self.server_url}/registerUser",
            json=dataclasses.asdict(create_user),
        )

    def send_message(self, user_id: int, message: str, date: int):
        res = requests.post(
            f"{self.server_url}/sendMessage",
            json={
                "user_id": user_id,
                "message": message,
                "date": date,
            },
        )

    def add_friend(self, user_id: int, friend_id: int):
        pass

    def search_user(self, request: PaginationRequest):
        pass
