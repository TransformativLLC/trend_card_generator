import nest_asyncio
from dotenv import load_dotenv


__all__ = [
    "set_up_env",
]


def set_up_env(trace: bool = False) -> None:
    load_dotenv()
    nest_asyncio.apply()
    if trace:
        import logfire
        logfire.configure(send_to_logfire='if-token-present')