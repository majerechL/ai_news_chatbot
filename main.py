import logging
import openai
from dotenv import load_dotenv
from tools import assistant_tools
from assistant_manager import AssistantManager
import streamlit

def read_instructions(file_path): # funkcia, ktorá načíta text zo súboru a použije sa ako instructions pre asistenta
    try:
        with open(file_path, encoding= "utf-8") as file:
            return file.read()
    except FileNotFoundError: # ošetrenie chyby, chyba sa zapíše do app.log a raise zastaví program, aby nepokračoval, keď sa vyskytne chyba
        logging.error(f"File {file_path}not found. Assistant instructions not available.")
        raise
def main():
    load_dotenv() # načítanie premenné prostredie z .env súboru
    logging.basicConfig(filename='app.log') #nastavuje logging, logging error pôjdú do súboru app.log

    client = openai.OpenAI()
    model = "gpt-4.1-mini" # klient na komunikáciu s OpenAI API (používa API key z prostredia)

    streamlit.title("Spravodaj")

    with streamlit.form(key="user_input_form"):
        topic_name = streamlit.text_input("Vlož tému, na ktorú chcete dostať zhrnutie aktuálnych noviniek: ") # vloženie textu
        submit_button = streamlit.form_submit_button(label="Spustiť")

        if submit_button:

            if "assistant" not in streamlit.session_state: # ak neexistuje asistent, tak ho vytvorí
                assistant = client.beta.assistants.create(name="Spravodaj", # tvorba OpenAI Assistenta s menom, modelom, inštrukciami zo súboru, nástrojmi
                    model=model,
                    instructions=read_instructions("assistant_instructions.txt"),
                    tools=assistant_tools)
                streamlit.session_state["assistant"] = assistant # uloženie asistenta do session state

            if "thread" not in streamlit.session_state:
                thread = client.beta.threads.create() # vlákno alebo konkrétna konverzácia, funguje ako chat okno
                streamlit.session_state["thread"] = thread # uloženie konverzacie do session state

                manager = AssistantManager(client, streamlit.session_state["assistant"], streamlit.session_state["thread"]) # vytvorenie managera s asistentom a konverzaciou 

                manager.add_message_to_thread(role="user",content=f"Sprav zhrnutie noviniek na tému{topic_name}")
                manager.run_assistant()
                manager.wait_for_run_to_complete()

                streamlit.write(manager.get_summary())

if __name__ == "__main__": # spustenie hlavnej funkcie
    main()
# pre spustenie stránky do pythonu napísať streamlit run main.py