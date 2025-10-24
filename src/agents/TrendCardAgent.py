from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from google.genai.types import HarmBlockThreshold, HarmCategory

from src.models import TrendCard, TrendCardInput
from src.utils.configuration import load_config


class TrendCardAgent:
    """
    Handles the configuration, initialization, and operation of an agent used for generating trend cards.

    This class is designed to streamline the process of loading configurations, setting up prompt templates,
    and utilizing a preconfigured model to produce trend card components based on input data. The generated
    trend cards are produced asynchronously using a predefined agent and prompt system.

    Attributes:
        config (dict): The configuration dictionary loaded from the specified file.
        system_prompt (str): Predefined system prompt used by the agent.
        prompt_template (str): Template for generating prompts specific to trend cards.
        agent (Agent): Configured agent instance for generating trend cards.
    """

    def __init__(self, config_path: str = "src/agents/config", config_file_name: str = "trend_card_agent.yaml"):
        """
        Initializes an instance of a class that configures and creates an agent based on the provided
        configuration file. It loads configuration settings, stores prompt templates, and initializes
        an agent with the specified model and parameters.

        Args:
            config_path (str): Path to the configuration file. Defaults to "trend_card_agent.yaml".
        """

        # read config
        self.config = load_config(config_file_name, config_path)

        # save prompt templates
        self.system_prompt = self.config["system_prompt"]
        self.prompt_template = self.config["generator_prompt"]

        # create the agent
        # the Google API is different than those for OpenAI, Anthropic, etc., so need google-specific code
        settings = None
        model = None
        if self.config["model"].startswith("gemini"):
            settings = GoogleModelSettings(
                temperature=self.config.get("temperature", 0.5),
                max_tokens=self.config.get("max_tokens", 2048),
                google_thinking_config={'thinking_budget': self.config.get("thinking_budget", 2048)},
                google_safety_settings=[
                    {
                        'category': self.config.get("safety_settings_cateogry", HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT),
                        'threshold': self.config.get("safety_settings_threshold", HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
                    }
                ]
            )
            model = GoogleModel(self.config["model"])
        else:
            settings=ModelSettings(
                max_tokens=self.config.get("max_tokens", 2048),
                temperature=self.config.get("temperature", 0.5)
            )
            model=self.config["model"]

        self.agent = Agent(
            model=model,
            model_settings=settings,
            output_type=TrendCard,
            system_prompt=self.system_prompt,
            retries=self.config.get("generator_retries", 3)
        )


    async def generate_trend_card(self, inputs: TrendCardInput) -> TrendCard:
        """
        Generates trend card components based on the given inputs.

        This method uses a predefined prompt template and fills it with values from the
        input object to create a query. The query is then passed to an agent which
        executes the operation and provides the result.

        Args:
            inputs (TrendCardInput): Input object containing values for industry
                segment, topic, and component.

        Returns:
            TrendCard: Generated trend card containing the requested components.
        """

        # create the finished prompt
        prompt = self.prompt_template.format(
            industry_segment=inputs.industry_segment,
            topic=inputs.topic,
            component=inputs.component,
        )

        # Run the agent
        result = await self.agent.run(prompt)
        return result.output


    translation_table = str.maketrans('.:-', '___')
    def get_directory_safe_model_name(self) -> str:
         return self.config["model"].translate(self.translation_table)