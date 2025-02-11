from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

def extract_user_data(text: str, field_names: list) -> dict:
  """
  From the input text, extract user data to the allowed fields.
  """

  # Instantiate the LLM
  llm = ChatOpenAI(model="gpt-4o-mini")

  # Prompt template for information extraction
  template_extract = PromptTemplate(
    input_variables=["text", "field_names"],
    template="From the message {text}, create a Python dictionary containing keys and values of extracted user data and their order's data. \
    Only return json dictionary in pure text form. For example: {{\"name\": \"John Doe\", \"sex\": \"male\"}}\
    the possible fields are {field_names}"
    )

  # Define the Output Parser
  json_output_parser = JsonOutputParser()

  # Chain them together
  chain = template_extract | llm | json_output_parser

  # Call the chain with your input
  result = chain.invoke({"text":text, "field_names":field_names})

  return result
    