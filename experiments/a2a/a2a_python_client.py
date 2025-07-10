from python_a2a import A2AClient, Message, TextContent, MessageRole

# Create a client to talk to our agent
client = A2AClient("http://localhost:5000/a2a")
# Send a message
message = Message(
    content=TextContent(text="Hello, is this thing on?"),
    role=MessageRole.USER
)
response = client.send_message(message)
# Print the response
print(f"Agent says: {response.content.text}")