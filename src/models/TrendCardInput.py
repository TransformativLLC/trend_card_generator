from typing import Optional
from pydantic import BaseModel, Field


class TrendCardInput(BaseModel):
    """
    Input parameters for generating a trend card.
    """

    industry_segment: str = Field(
        ...,
        description="The industry segment to analyze (e.g., 'Payment processing platforms')"
    )

    topic: str = Field(
        ...,
        description="The topic to investigate (e.g., 'Gen Z in the Workforce')"
    )

    component: Optional[str] = Field(
        None,
        description="Optional STEEL framework component (Social, Technical, Economic, Environmental, or Legal). "
                    "If not provided, the most relevant component will be determined by the agent."
    )

    word_limit: Optional[int] = Field(
        40,
        description="Optional limit on the number of words for each text section."
    )