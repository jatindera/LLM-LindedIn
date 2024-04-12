import json
import ast
import requests
from dotenv import load_dotenv
from common.MyLinkedIn import *


def get_linkedin_profile(api_key, linkedin_profile_url) -> json:
    headers = {"Authorization": "Bearer " + api_key}
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    params = {
        "linkedin_profile_url": linkedin_profile_url,
        "extra": "include",
        "github_profile_id": "include",
        "facebook_profile_id": "include",
        "twitter_profile_id": "include",
        "personal_contact_number": "include",
        "personal_email": "include",
        "inferred_salary": "include",
        "skills": "include",
        "use_cache": "if-present",
        "fallback_to_cache": "on-error",
    }
    response = requests.get(api_endpoint,
                            params=params,
                            headers=headers)
    return response.json()


#write a function to read a json file and return a dictionary
def get_linkedin_profile_from_filesystem(file_path):
    with open(file_path, 'r') as file:
        linkedin_profile_dict = file.read()
        return linkedin_profile_dict


def json_corrections(linkedin_response_str):
    linkedin_response_str = linkedin_response_str.replace("'", '"')
    linkedin_response_str = linkedin_response_str.replace('"s ', "'s ")
    linkedin_response_str = linkedin_response_str.replace("None", "\"None\"")
    #convert the string to a dictionary
    linkedin_response_dict = ast.literal_eval(linkedin_response_str)
    # print(linkedin_response_dict)
    return linkedin_response_dict

def linkedin_profile_cleanup(linkedin_profile_dict):
    """scrape information from linkedin profiles,
    Manually scrape the information from the LinkedIn profile
    """
    linkedin_profile_dict = {
    k:v
    for k,v in linkedin_profile_dict.items()
    if v not in [[],"",'', 'None', None] and k not in ["people_also_viewed", "certifications"]
}
    #remove the key "profile_pic_url" from the dictionary
    if linkedin_profile_dict.get("groups"):
        for group_dict in linkedin_profile_dict["groups"]:
            group_dict.pop("profile_pic_url")
    
    return linkedin_profile_dict
   

