import os
import json
from news_api_client import NewsAPIClient

class AssistantManager:
    def __init__(self, client, assistant, thread):
        self.client = client
        self.assistant = assistant
        self.thread = thread
        self.run = None
        self.summary = None

    def add_message_to_thread(self, role, content):
        self.client.beta.threads.messages.create(
            self.thread.id, role=role, content=content
        )

    def run_assistant(self): # 
        self.run = self.client.beta.threads.runs.create(
            self.thread.id, assistant_id=self.assistant.id
        )

    def check_run(self): # metóda, ktorá vráti navráti status behu, nebude tu treba parameter, pretože informáciu o behu máme - self.run
        run_status = self.client.beta.threads.runs.retrieve(
            self.run.id, thread_id=self.thread.id
        )
        return run_status
    
    def wait_for_run_to_complete(self): # táto metoda bued ukončená v prípade, že dosiahne stavu complete
        while True:
            run = self.check_run()
            if run.status == "completed":
                self.get_latest_response()
                break
            elif run.status == "requires_action":
                tools_output = self.prepare_tool_outputs(run.required_action.submit_tool_outputs.model_dump())
                self.client.beta.threads.runs.submit_tool_outputs(self.run.id, thread_id=self.thread.id, tool_outputs=tools_output)
                #get news
        

    def get_news(self, topic):
        news_api_key = os.getenv("NEWS_API_KEY")
        news_client = NewsAPIClient(news_api_key)
        return news_client.fetch_news(topic)
    
    def format_output(self, news_output):
        articles = [f"Title: {article['title']}, Author: {article['author']}, URL: {article['url']}, description: {article['description']}"
            for article in news_output]

        output_str = "\n".join(articles)
        return output_str
    
    def prepare_tool_outputs(self, tool_calls):
        tools_outputs = []

        for call in tool_calls["tool_calls"]:
            if call["function"]["name"] == "get_news":
                topic_load =json.loads(call["function"]["arguments"])
                topic = topic_load["topic"]

                new_output = self.get_news(topic)
                output = self.format_output(new_output)

                tools_outputs.append({"tool_call_id": call["id"], "output": output})
        
        return tools_outputs

    def get_latest_response(self):
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        last_message = messages.data[0].content[0].text.value
        self.summary = last_message

    def get_summary(self):
        return self.summary