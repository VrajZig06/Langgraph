from langgraph.graph import StateGraph,START,END
from typing import TypedDict

class State_Workflow(TypedDict):
    a : int
    b : int
    result : int

def sum_number(state :State_Workflow) -> State_Workflow:
    a = state['a']
    b = state['b']

    sum = a + b
    return {"result" : sum}

def print_result(state : State_Workflow) -> State_Workflow:
    result = state['result']
    print("Result : ",result )
    return {}


# create graph
graph = StateGraph(State_Workflow)

# Add Nodes 
graph.add_node("sum_number",sum_number)
graph.add_node("print_result",print_result)

# Add Edges
graph.add_edge(START,'sum_number')
graph.add_edge("sum_number","print_result")
graph.add_edge("print_result",END)

# compile Graph
workflow = graph.compile()

# Invoke
initial_state = {"a" : 10, "b" : 2}

final_state = workflow.invoke(initial_state)
print(final_state)

