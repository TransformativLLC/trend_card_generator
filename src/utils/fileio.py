import re
from pathlib import Path
from src.models import TrendCard


def save_as_md_file(card: TrendCard, file_path: str = "../outputs") -> None:
    """
    Saves the provided TrendCard object as a Markdown (.md) file at the specified file path.

    This function generates a Markdown file name based on the card identifier by replacing
    any slashes ('/') with spaces, converting to lowercase, and substituting spaces with
    underscores. The resulting file is saved at the provided file path, using UTF-8 encoding.

    Args:
        card: TrendCard instance containing the content to save in Markdown format.
        file_name: Name of the file (ignored as the name is auto-generated based on the card).
        file_path: Directory path where the file will be saved. Defaults to "../outputs".

    Returns:
        None
    """

    file_name = card.card_identifier.lower()
    file_name = re.sub(r'[^\w\s]', ' ', file_name)
    file_name = re.sub(r'\s+', '_', file_name.strip()) + ".md"

    path = Path(file_path) / file_name
    path.write_text(card.to_markdown(), encoding='utf-8')
