from pydantic import BaseModel, Field
from typing import get_type_hints


class TrendCard(BaseModel):
    """
    """

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
        Converts a TrendCard instance into a markdown string.

        This method iterates through the attributes of a TrendCard instance and formats
        each attribute into a markdown-ready string using an output format specified
        in the configuration. The formatted markdown string will contain the
        attributes' values structured as titles and contents.

        Args:
            card (TrendCard): An instance of the TrendCard class whose attributes will
                be converted to a markdown string.

        Returns:
            str: A formatted markdown string representing the TrendCard's attributes.
        """

        card_content_markdown = ""

        # Iterate through TrendCard attributes
        for attr_name, attr_value in get_type_hints(TrendCard).items():
            # Format attribute name as title
            title = attr_name.replace('_', ' ').title()
            content = getattr(self, attr_name)

            # Add formatted section to markdown
            card_content_markdown += output_format.format(
                title=title,
                content=content,
            )

        return card_content_markdown.strip()
