from dotenv import load_dotenv
import os
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler


load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']
ASSISTANT_ID = os.environ['ASSISTANT_ID']
THREAD_ID = os.environ['THREAD_ID']

# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)

client = OpenAI(api_key=API_KEY)

# assistant = client.beta.assistants.create(
#   name="Math Tutor",
#   instructions="You are a personal math tutor. Write and run code to answer math questions.",
#   tools=[{"type": "code_interpreter"}],
#   model="gpt-4-turbo",
# )

# thread = client.beta.threads.create()

# assistant와 thread는 별개 thread 먼저 만들고 assistant에 넣을 수 있음
# 한 thread를 a assistant에 넣고 b assistant에 넣을 수 있다

# MESSAGE_ID = "msg_Ds8zvlSC7684YmTS3mRDYFbg"
# message = client.beta.threads.messages.create(
#   thread_id="thread_Z6dSTTs4sJSe2EkDbfIGgS2t",
#   role="user",
#   content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
# )

 
# Then, we use the `stream` SDK helper 
# with the `EventHandler` class to create the Run 
# and stream the response.
with client.beta.threads.runs.stream(
  thread_id=THREAD_ID,
  assistant_id=ASSISTANT_ID,
  instructions="Please address the user as Jane Doe. The user has a premium account.",
  event_handler=EventHandler(),
) as stream:
  stream.until_done()