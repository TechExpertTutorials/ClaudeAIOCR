import anthropic
import os

client = anthropic.Anthropic(
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    # api_key="my_api_key",
)
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude. Tell me how big is the earth?"}
    ]
)
print(message.content)