import re
from pathlib import Path
from pydantic import BaseModel, Field
from typing import get_type_hints, Dict

from src.utils.fileio import append_to_filename


# Word counting regex pattern that better matches MS Word's counting logic
WORD_PATTERN = re.compile(r'\b[\w\']+\b')


class TrendCard(BaseModel):

    card_identifier: str = Field(
        ...,
        description="Identifier comprised of topic / component (e.g., 'Gen Z in the Workforce / Social')"
    )

    title: str = Field(
        ...,
        description="Short title that conveys the emerging trend, weak signal, or prospective event"
    )

    description: str = Field(
        ...,
        description="1-3 sentence description of the finding"
    )

    implications: str = Field(
        ...,
        description="2-3 sentences describing the implication of the finding on businesses in the industry"
    )

    opportunities: str = Field(
        ...,
        description="2-4 sentences highlighting opportunities the finding might present to businesses"
    )

    challenges: str = Field(
        ...,
        alias="challenges_threats",
        description="2-4 sentences describing potential challenges/threats posed by the finding"
    )

    class Config:
        populate_by_name = True  # Allows using both 'challenges' and 'challenges_threats'


    def to_markdown(self, output_format: str = "**{title}:** {content}\n\n") -> str:
        """
        Converts the attributes of a TrendCard instance to a Markdown formatted string.

        This method iterates through the attributes of the TrendCard instance, formatting
        each attribute as a Markdown section with a title and content. The output format is
        customizable by providing a specific format string.

        Args:
            output_format (str): A format string specifying how each attribute's title and
                content should be placed in the output Markdown. Defaults to
                "**{title}:** {content}\n\n".

        Returns:
            str: A Markdown formatted string containing all attributes of the TrendCard
                instance.
        """

        card_content_markdown = ""

        # Iterate through TrendCard attributes
        for attr_name, attr_value in get_type_hints(TrendCard).items():
            # Format attribute name as title
            title = attr_name.replace('_', ' ').title()
            content = getattr(self, attr_name)

            # Add a formatted section
            card_content_markdown += output_format.format(
                title=title,
                content=content,
            )

        return card_content_markdown.strip()

    def save_to_file(self, file_name_suffix: str = None,
                     extension: str = ".md", file_path: str = "../outputs") -> str:
        """
        Saves the content of the object to a file with a specified naming convention and file extension.
        This method creates a new directory if it does not exist and writes the content in a format
        determined by the extension. Only Markdown (.md) format is currently supported.

        Args:
            file_name_suffix (str, optional): The suffix to append to the file name. Defaults to None.
            extension (str, optional): The desired file extension for the saved file. Defaults to ".md".
            file_path (str, optional): The path where the file should be saved. Defaults to "../outputs".

        Returns:
            str: The name of the saved file.
        """
        # ensure the extension starts with a period
        if not extension.startswith('.'):
            extension = f'.{extension}'

        file_name = self.card_identifier.lower()
        file_name = re.sub(r'[^\w\s]', ' ', file_name)
        file_name = re.sub(r'\s+', '_', file_name.strip()) + extension

        if file_name_suffix:
            file_name = append_to_filename(file_name, suffix=file_name_suffix)

        path = Path(file_path)
        path.mkdir(parents=True, exist_ok=True)

        output_path = path / file_name

        match extension:
            case ".md": output_path.write_text(self.to_markdown(), encoding='utf-8')
            case _: raise NotImplementedError(f"Extension '{extension}' not implemented.")

        return file_name

    def get_length(self) -> Dict[str, int]:
        """
        Calculates the number of words in the TrendCard attribute values.

        Iterates through the attributes of the TrendCard class, computes the total word count
        for the value of each attribute, and returns this information as a dictionary.

        Returns:
            Dict[str, int]: A dictionary where keys are TrendCard attribute names and values
            are the word counts of their respective content.

        Raises:
            AttributeError: If any attribute access operation fails.
        """
        section_lengths = dict()
        # Iterate through TrendCard attributes
        for attr_name in get_type_hints(TrendCard).keys():
            content = getattr(self, attr_name)
            section_lengths[attr_name] = len(WORD_PATTERN.findall(content))

        return section_lengths