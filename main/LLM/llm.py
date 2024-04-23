import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),  '.env'))

import importlib.util
import os
import database


def import_module_from_directory(directory, package_name, module_name):
    file_path = os.path.join(directory, package_name, module_name + ".py")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

bing_module = import_module_from_directory(os.path.dirname(os.path.dirname(__file__)), "scrapers", "bing")
google_module = import_module_from_directory(os.path.dirname(os.path.dirname(__file__)), "scrapers", "google")



google_api_key = os.getenv("API_KEY")

genai.configure(api_key = google_api_key)

def getPromptResponse( prompt, top_p = 0.8, top_k = 2, temp = 0.9):
    """ Generate a response based on a user prompt using a generative AI model.

        Returns:
            str: The generated response based on the user prompt.
    """

    generation_config = {
      "temperature": temp,
      "top_p": top_p,
      "top_k": top_k,
      "max_output_tokens": 2048,
    }

    safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    response = model.generate_content(prompt)

    return response.text

def getChatResponse( prompt, top_p = 0.8, top_k = 2, temp = 0.9, history = []):
    """ Generate a response based on a user prompt using a generative AI model
        given the chat history.

        Returns: tuple containing prompt response and updated chat history.
    """

    generation_config = {
      "temperature": temp,
      "top_p": top_p,
      "top_k": top_k,
      "max_output_tokens": 2048,
    }

    safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    convo = model.start_chat(history = history)
    convo.send_message(prompt)

    response = convo.last.text

    return response, convo.history

def chat(user_id, chat_id, prompt):
    if( chat_id == None ):
        response, history = getChatResponse( prompt )
        topic = getChatTopic( prompt )
        database.insert_into_history_table( user_id, topic, history)
    else:
        history = database.getChatHistory( chat_id, user_id)
        response, history = getChatResponse( prompt, history )
        database.update_chat_history( chat_id, user_id, history)
    return response

def extendedChat(user_id, chat_id, prompt):
    if( chat_id == None ):
        extended_prompt = getExtendedPrompt(prompt)
        response, history = getExtendedChatResponse( prompt )
        topic = getChatTopic( prompt )
        database.insert_into_history_table( user_id, topic, history)
    else:
        extended_prompt = getExtendedPrompt(prompt)
        history = database.getChatHistory( chat_id, user_id)
        response, history = getChatResponse( prompt, history )
        database.update_chat_history( chat_id, user_id, history)
    return response

def getChatTopic( first_prompt ):
    prompt = f"""Generate a concise and appropriate topic for this user prompt: "{first_prompt}" within 20 characters.
				Enclose the topic within '$$$$' and '$$$$' as start and end markers.
    			Output format: $$$$ topic string $$$$"""
    response = getPromptResponse(prompt, temp=0.7)

    start_marker = '$$$$'
    end_marker = '$$$$'

    start_index = response.find(start_marker)
    end_index = response.find(end_marker, start_index + len(start_marker))

    topic = response[start_index + len(start_marker):end_index].strip()

    return topic

def getExtendedPrompt( prompt ):
  bing_res = bing_module.bing_search(prompt)
  google_res = google_module.google_search(prompt)

  extended_prompt = f""" prompt: "{prompt}"
                        BING_SEARCH_RESULT: "{bing_res}"
                        GOOGLE_SEARCH_RESULT: "{google_res}"
                        OUTPUT FORMAT: $$$$ response $$$$
                        Given the provided prompt and search results from bing and google search engines
                        respectively, generate the most appropriate response to the prompt considering this
                        added knowledge and existing background knowledge.
                        enclose the response within '$$$$' and '$$$$'.
                    """
  return extended_prompt

def getExtendedPromptResponse( prompt ):
    # extended_prompt = prompt
    extended_prompt = getExtendedPrompt(prompt)

    response = getPromptResponse(extended_prompt, temp=0.4)

    start_marker = '$$$$'
    end_marker = '$$$$'

    start_index = response.find(start_marker)
    end_index = response.find(end_marker, start_index + len(start_marker))

    res = response[start_index + len(start_marker):end_index].strip()

    return res

def getExtendedChatResponse( prompt, history = [] ):
    # extended_prompt = prompt
    extended_prompt = getExtendedPrompt(prompt)

    response, history = getChatResponse(extended_prompt, temp=0.4, history = history)

    start_marker = '$$$$'
    end_marker = '$$$$'

    start_index = response.find(start_marker)
    end_index = response.find(end_marker, start_index + len(start_marker))

    res = response[start_index + len(start_marker):end_index].strip()

    return res, history

response = getExtendedPromptResponse( "Explain theory of relativity in the easiest way..")
print(response)