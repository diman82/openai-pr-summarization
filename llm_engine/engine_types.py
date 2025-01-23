from enum import Enum, unique


@unique
class Engine(Enum):
    GPT = "gpt-4"
    LLAMA = "llama (gpt-3.5)"
