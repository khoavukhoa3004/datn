from dataclasses import dataclass

@dataclass
class AccountResponse:
  name: str
  email: str
  type: str
  create_at: str