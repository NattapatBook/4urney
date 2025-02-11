from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

def extract_user_data(text: str, field_names: list, descriptions: list) -> dict:
  """
  From the input text, extract user data to the allowed fields.
  """
  
  field_names_list = []
  for field_name, description in zip(field_names, descriptions): 
    field_names_list.append(f"""{field_name}: {description}""")
    
  field_names_final = '\n'.join(field_names_list)
  print(field_names_list)

  # Instantiate the LLM
  llm = ChatOpenAI(model="gpt-4o-mini")

  # Prompt template for information extraction
  template_extract = PromptTemplate(
    input_variables=["text", "field_names_final"],
    template=
      """
      Given the message {text}, extract relevant user information and structure it as a Python dictionary. 
      Only include the specified fields if they are present in the message. If a field is not mentioned, please response only keys of listed field with empty values. 
      
      Only return json dictionary in pure text form. For example: {{\"name\": \"John Doe\", \"sex\": \"male\"}}\
      
      The possible fields are listed below
      {field_names_final}
      """
    )

  # Define the Output Parser
  json_output_parser = JsonOutputParser()

  # Chain them together
  chain = template_extract | llm | json_output_parser

  # Call the chain with your input
  result = chain.invoke({"text":text, "field_names_final":field_names_final})

  return result
    