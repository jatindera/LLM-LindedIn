import os
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from common.MyLinkedIn import *


load_dotenv()

if __name__ == "__main__":
    print(__name__)
    print("Hello Langchain")
  
    summary_template = """
        Given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        3. Suggest two funny names for the person     
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)
    
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    #get key from .env
    NUBELA_API_KEY = os.getenv("NUBELA_API_KEY")
    
    linkedin_response_dict = get_linkedin_profile(NUBELA_API_KEY, "https://www.linkedin.com/in/arorajatinder/")
    print(linkedin_response_dict)
    #read key "description" from the dictionary
    profile_name = "jatinderarora.json"
    try:        
        if linkedin_response_dict["description"] == "Not enough credits, please top up.":
            linkedin_response_str = get_linkedin_profile_from_filesystem(f"linkedin_profiles/{profile_name}")
            linkedin_response_dict = json_corrections(linkedin_response_str)
            linkedin_profile_dict = linkedin_profile_cleanup(linkedin_response_dict)            
    except TypeError:
        linkedin_response_str = get_linkedin_profile_from_filesystem(f"linkedin_profiles/{profile_name}")
    
    

    print(chain.run(information=linkedin_profile_dict))

    
    


