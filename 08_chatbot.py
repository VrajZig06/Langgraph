from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
import operator
from langgraph.checkpoint.memory import MemorySaver

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-Coder-480B-A35B-Instruct",
    task="text-generation",
    max_new_tokens=100)

chat_model = ChatHuggingFace(llm=llm)

class WorkFlow_State(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]


def chat_node(state:WorkFlow_State) -> WorkFlow_State:
    messages = state['messages']
    response = chat_model.invoke(messages)
    return {"messages" : [response]}

# create CheckPoint
checkpointer = MemorySaver()


# Create Graph 
graph = StateGraph(WorkFlow_State)

# Add Node
graph.add_node("chat_node",chat_node)

# Add Edges 
graph.add_edge(START,'chat_node')
graph.add_edge("chat_node",END)

# Compile Graph
workflow = graph.compile(checkpointer=checkpointer)

thread_id = "1"
while True:
    query = input("\n\n ******** Type Here ********: ")
    if query.lower().strip() == "exit":
        break

    # Invoke workflow
    config = {"configurable" : {"thread_id":thread_id}}
    initial_state = {"messages" : [query]}
    final_state = workflow.invoke(initial_state,config)
    print(f"\n ******** AI Response ******** \n {final_state['messages'][-1].content}")