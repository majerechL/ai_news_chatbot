assistant_tools=[
    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "Get the list of articles/news for the given topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic for the news, e.g., bitcoin",
                    }
                },
                "required": ["topic"],
            },
        },
    }
]