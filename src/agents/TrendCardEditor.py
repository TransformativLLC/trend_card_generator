from typing import List
from pydantic_ai import Agent

from src.agents.AgentFactory import AgentFactory
from src.models import TrendCard, AgentConfiguration
from src.utils.configuration import load_config
from src.utils.fileio import read_file


class TrendCardEditor:
    """
    Handles the editing and batch processing of trend cards, leveraging configuration-based
    settings and asynchronous operations.

    This class is designed to provide utilities for editing "trend cards," which are presumably
    text-based artifacts processed and updated with the assistance of an asynchronous agent.
    It allows integration with configuration files for defining agent behavior and includes
    methods for editing individual and multiple trend cards.

    Attributes:
        model (str): The name of the model used by the agent to process trend cards.
        agent (Agent): The agent instance responsible for handling asynchronous operations
            related to trend card editing.
    """

    def __init__(self, config_path: str = "src/agents/config", config_file_name: str = "trend_card_editor.yaml",
                 settings: AgentConfiguration = None, section_word_limit: int = 40):
        """
        Initializes an instance of the class by loading configuration, applying overrides if
        provided, and creating an agent based on the specified configuration.

        Args:
            config_path: Path to the directory containing the configuration file.
            config_file_name: Name of the configuration file including file extension.
            settings: Configuration settings that can override certain defaults in the
                loaded configuration file.
            section_word_limit: Limit on the word count for a specific section of the
                system prompt.
        """

        # read config
        config = load_config(config_file_name, config_path)

        # overwrite the config file settings if settings are provided
        if settings:
            config["model"] = settings.model
            config["temperature"] = settings.temperature

        # add word limit to system prompt
        config["system_prompt"] = config["system_prompt"].format(word_limit=section_word_limit)

        # remember the model name
        self.model = config["model"]

        # create the agent
        self.agent = AgentFactory.create_agent(config)


    async def edit_trend_card(self, trend_card_text: str) -> TrendCard:
        """
        Edits the trend card using the provided text and runs the required asynchronous
        agent operation.

        Args:
            trend_card_text (str): A string containing the text to update the trend card.

        Returns:
            TrendCard: The updated TrendCard instance obtained from the asynchronous
            agent operation.
        """

        # Run the agent
        result = await self.agent.run(trend_card_text)
        return result.output


    async def edit_batch(self, file_list: List[str], target_dir: str,
                         file_name_suffix: str, verbose: bool = False) -> None:
        """
        Asynchronously edits a batch of text files and saves the modified content to a target directory. Each file's content is
        processed through the `edit_trend_card` method, and the resultant content is saved using the provided file name suffix.

        Args:
            file_list (List[str]): A list of file paths to be read and edited.
            target_dir (str): The directory where the edited files will be saved.
            file_name_suffix (str): A suffix appended to the file names of the edited files.
            verbose (bool, optional): Enables verbose mode to log processing details if set to True. Defaults to False.

        Returns:
            None
        """
        list_len = len(file_list)
        if verbose: print(f'Editing {list_len} file{"s" if list_len > 1 else ""} in "{target_dir}"...')
        i = 1
        for file in file_list:
            text = read_file(file)
            trend_card = await self.edit_trend_card(text)
            saved_file_name = trend_card.save_to_file(file_path=target_dir, file_name_suffix=file_name_suffix)
            if verbose:
                print(f"{i}: {saved_file_name}")
                print("\nWORD LENGTHS")
                print(trend_card.get_length(), end="\n" * 2)
                i += 1