from pydantic import BaseModel, Field


class AgentConfiguration(BaseModel):
    """
    Parameters for constructing agents
    """

    model: str = Field(
        ...,
        description="The LLM model to be utilized by the agent"
    )

    temperature: float = Field(
        ...,
        description="The temperature setting for the LLM",
        ge=0.0,
        le=2.0
    )
