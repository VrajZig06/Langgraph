from langgraph.graph import StateGraph,START,END
from typing import TypedDict
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class BLOG_APP_STATE(TypedDict):
    topic : str
    outline : str
    blog : str

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-Coder-480B-A35B-Instruct",
    task="text-generation",
    max_new_tokens=100)

chat_model = ChatHuggingFace(llm=llm)

str_parser = StrOutputParser()

# Nodes Behaviour 
def generate_outline(state:BLOG_APP_STATE) -> BLOG_APP_STATE:
    topic = state['topic']
    prompt = PromptTemplate(template=
    """
        You are Good Assistance and Good Writer.
        Generate Outline for following Topic.
        Topic Name : {topic}
    """)
    chain = prompt | chat_model | str_parser

    response = chain.invoke({
        "topic" : topic 
    })

    state['outline'] = response
    return state

def generate_blog(state:BLOG_APP_STATE) -> BLOG_APP_STATE:
    outline = state['outline']
    prompt = PromptTemplate(
        template=
        """
            You have Good Reasoning Power. So You need to generate Blog using following outlines.
            Outline : {outline}
        """
    )

    chain = prompt | chat_model | str_parser

    response = chain.invoke({
        "outline" : outline
    })

    state["blog"] = response

    return state

def store_to_file(state:BLOG_APP_STATE) -> BLOG_APP_STATE:
    blog = state["blog"]
    topic = state['topic']
    filename = f"Blog_{topic}.txt"

    with open(filename,"w") as f:
        f.write(blog)
    
    return state

# Create Graph
graph = StateGraph(BLOG_APP_STATE)

# Add Nodes 
graph.add_node("generate_outline",generate_outline)
graph.add_node("generate_blog",generate_blog)
graph.add_node("store_to_file",store_to_file)

# Connects Nodes using Edges
graph.add_edge(START,"generate_outline")
graph.add_edge('generate_outline','generate_blog')
graph.add_edge("generate_blog","store_to_file")
graph.add_edge("store_to_file",END)

# Compile Graph
workflow = graph.compile()

# Invoke Graph using Initial State 
initial_state = {
    "topic" : "LangChain as a Future."
}

final_state = workflow.invoke(initial_state)
print(final_state)

