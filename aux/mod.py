from dataclasses import dataclass, field

token_limit_default = 999999

@dataclass
class User:
    name: str
    email: str
    telefone: str
    token_limit: int = field(default=token_limit_default)
    token_used: int = field(default=0)

@dataclass
class Question:
    user_id: int
    session_id: int
    question: str
    answer: str
    feedback: bool = field(default=0)
    used_tokens: int = field(default=0)