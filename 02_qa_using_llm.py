from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langgraph.graph import StateGraph,START,END
from langchain.prompts import PromptTemplate
from typing import TypedDict
from langchain_core.output_parsers import StrOutputParser

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-Coder-480B-A35B-Instruct",
    task="text-generation",
    max_new_tokens=100)

chat_model = ChatHuggingFace(llm=llm)

str_parser = StrOutputParser()


# state for graph
class QA_STATE(TypedDict):
    question : str
    answer : str

# function to answer user's input
def get_answer(state : QA_STATE) -> QA_STATE:
    question = state['question']

    # Creating Prompt 
    prompt = PromptTemplate(
        template=
        """
            Give me Answer of Following Question.
            Question : {question}
        """
    )

    # create chain 
    chain = prompt | chat_model | str_parser
    response = chain.invoke({"question" : question})
    
    state['answer'] = response

    return state

# create graph
graph = StateGraph(QA_STATE)

# Add Node 
graph.add_node("get_answer",get_answer)

# Connect Edges between Node 
graph.add_edge(START,"get_answer")
graph.add_edge("get_answer",END)

# Compile Graph
workflow = graph.compile()

# Invoking Graph
initial_state = {
    "question" : "What is LangGraph?"
}
final_state = workflow.invoke(initial_state)
print(final_state)


