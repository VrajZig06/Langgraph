from langgraph.graph import StateGraph,START,END
from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
import time
from langchain_core.prompts import PromptTemplate

class WorkFlow_State(TypedDict):
    topic : str
    joke : str
    exp : str

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-Coder-480B-A35B-Instruct",
    task="text-generation",
    max_new_tokens=100
)

def Generate_Joke(state:WorkFlow_State) -> WorkFlow_State:
    print("STEP 1")
    topic = state["topic"]  
    prompt = PromptTemplate(
        template= """
            genereate Joke on given topic : {topic}
        """
    )
    chain = prompt | chat_model 
    response = chain.invoke({
        "topic" : topic
    })

    return {"joke":response.content}

def Explain_Joke(state:WorkFlow_State) -> WorkFlow_State:
    print("STEP 2")
    time.sleep(10)
    joke = state['joke']
    prompt = PromptTemplate(
        template= """
            genereate Joke Explaination for given Joke : {joke}
        """
    )
    
    chain = prompt | chat_model 
    response = chain.invoke({
        "joke" : joke
    })
    return {"exp":response.content}


# Chat Model Initialization
chat_model = ChatHuggingFace(llm=llm)

# Create Graph 
graph = StateGraph(WorkFlow_State)

# add Node to graph
graph.add_node("Generate_Joke",Generate_Joke)
graph.add_node("Explain_Joke",Explain_Joke)

# Add Edges
graph.add_edge(START,"Generate_Joke")
graph.add_edge("Generate_Joke","Explain_Joke")
graph.add_edge("Generate_Joke",END)

# checkpointer initialization
checkpointer = InMemorySaver()

# graph compile
workflow = graph.compile(checkpointer=checkpointer)

thread_id = 1

config = {"configurable":{"thread_id":thread_id}}

initial_state = {"topic" : "AI"}
final_state = workflow.invoke(initial_state,config,checkpointer="1f0840da-4da1-6f1a-8001-5ea8eb684a2d")
print(final_state)

print(workflow.get_state(config))
print(workflow.get_state_history(config))





