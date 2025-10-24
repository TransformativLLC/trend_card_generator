from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from google.genai.types import HarmBlockThreshold, HarmCategory, SafetySettingDict

from src.models import TrendCard


class AgentFactory:
    """
    A factory for creating and configuring pydantic-ai Agent instances.
    """

    @staticmethod
    def create_agent(config: dict) -> Agent:
        """
        Creates an instance of an Agent based on the provided configuration.

        The method parses the configuration to set up the appropriate model and
        settings, specifically tailored for Google models or other models. It
        returns an Agent object configured as per the input parameters.

        Args:
            config (dict): A dictionary containing configuration parameters
                for creating the agent. It includes details like the model to
                be used, temperature, max tokens, system prompts, generator
                retries, and other relevant settings for specific models.

        Returns:
            Agent: An initialized Agent object configured as per the
            provided input configuration.
        """
        # the Google API is different from those for OpenAI, Anthropic, etc., so need google-specific code
        if config["model"].startswith("gemini"):
            safety_settings = SafetySettingDict(
                category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
            )
            settings = GoogleModelSettings(
                temperature=config.get("temperature", 0.5),
                max_tokens=config.get("max_tokens", 2048),
                google_thinking_config={'thinking_budget': config.get("thinking_budget", 2048)},
                google_safety_settings=[safety_settings]
            )
            model = GoogleModel(config["model"])
        else:
            settings=ModelSettings(
                max_tokens=config.get("max_tokens", 2048),
                temperature=config.get("temperature", 0.5)
            )
            model=config["model"]

        return Agent(
            model=model,
            model_settings=settings,
            output_type=TrendCard,
            system_prompt=config["system_prompt"],
            retries=config.get("generator_retries", 3)
        )