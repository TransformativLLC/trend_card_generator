from typing import Dict

from pydantic_ai import Agent

from src.agents.AgentFactory import AgentFactory
from src.models import TrendCard, TrendCardInput, AgentConfiguration
from src.utils.configuration import load_config


class TrendCardAgent:
    """
    Manages trend card generation, utilizing various model configurations and prompts,
    while supporting batch creation and saving of trend cards. This agent is designed
    to work with both simple and complex configurations and supports model-specific logic.

    Attributes:
        config (dict): Contains the configuration settings loaded from the YAML file or
            overridden by external inputs.
        system_prompt (str): Represents the base system prompt used by the generative model.
        prompt_template (str): Template for generating queries dynamically based on input
            parameters.
        agent (Agent): Instance of a configured agent responsible for processing prompts
            and generating outputs.
        translation_table (dict): Translation table for converting model names into a safe
            directory-compatible format, replacing special characters with underscores.
    """

    def __init__(self, config_path: str = "src/agents/config",  config_file_name: str = "trend_card_agent.yaml",
                 settings: AgentConfiguration = None):
        """
        Initializes the configuration and sets up the agent with the provided or default parameters.

        Args:
            config_path (str): Path to the directory containing the configuration files.
            config_file_name (str): Name of the configuration file to be loaded.
            settings (AgentConfiguration): Optional configuration settings to overwrite the
                defaults in the configuration file.

        """

        # read config
        config = load_config(config_file_name, config_path)

        # overwrite the config file settings if settings are provided
        if settings:
            config["model"] = settings.model
            config["temperature"] = settings.temperature

        self.prompt_template = config["prompt_template"]
        self.model = config["model"]

        # create the agent
        self.agent = AgentFactory.create_agent(config)


    async def generate_trend_card(self, inputs: TrendCardInput) -> TrendCard:
        """
        Generates trend card components based on the given inputs.

        This method uses a predefined prompt template and fills it with values from the
        input object to create a query. The query is then passed to an agent which
        executes the operation and provides the result.

        Args:
            inputs (TrendCardInput): Input object containing values for industry
                segment, topic, component, and word limit.

        Returns:
            TrendCard: Generated trend card containing the requested components.
        """

        # create the finished prompt
        prompt = self.prompt_template.format(
            industry_segment=inputs.industry_segment,
            topic=inputs.topic,
            component=inputs.component,
            word_limit=inputs.word_limit
        )

        # Run the agent
        result = await self.agent.run(prompt)
        return result.output


    async def generate_batch(self, industry_segment: str, topic_map: Dict[str, str],
                             target_dir: str, word_limit: int = 40, verbose: bool = False) -> None:
        """
        Generates and processes a batch of trend cards for a given industry segment and saves them to a
        specified directory.

        This method iterates through a dictionary of topic-to-component mappings, creates trend cards for
        each topic, and saves the generated trend card to a specified directory. Optional verbosity provides
        detailed processing outputs for each trend card.

        Args:
            industry_segment: String identifier for the industry segment being processed.
            topic_map: Dictionary mapping topics to their respective components.
            target_dir: Directory to save the resulting trend cards.
            word_limit: Word limit for each section of the trend card.
            verbose: Boolean indicating whether to print detailed progress during processing. Defaults to False.

        Returns:
            None
        """
        list_len = len(topic_map)
        if verbose: print(f'Processing {list_len} topic{"s" if list_len > 1 else ""}...')
        i = 1
        for topic, component in topic_map.items():
            inputs = TrendCardInput(
                industry_segment=industry_segment,
                topic=topic,
                component=component,
                word_limit=word_limit
            )

            trend_card = await self.generate_trend_card(inputs)
            trend_card.save_to_file(file_path=target_dir)

            if verbose:
                print(f"{i}: {trend_card.card_identifier}")
                print("\nSECTION LENGTHS")
                print(trend_card.get_length(), end="\n" * 2)
                i += 1


    translation_table = str.maketrans('.:-', '___')
    def get_directory_safe_model_name(self) -> str:
         return self.model.translate(self.translation_table)