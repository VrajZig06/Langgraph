from langgraph.graph import StateGraph,START,END
from typing import TypedDict

class WorkFlow_State(TypedDict):
    a : int
    b : int
    Addition : int
    Multiplication : int

def Addition(state: WorkFlow_State) -> WorkFlow_State:
    a = state['a']
    b = state['b']

    sum = a + b
    return {"Addition": sum}

def Multiplication(state:WorkFlow_State) -> WorkFlow_State:
    a = state['a']
    b = state['b']

    multiplication = a * b

    return {"Multiplication" : multiplication}

# Create Graph 
graph = StateGraph(WorkFlow_State)

# Create nodes
graph.add_node('Addition',Addition)
graph.add_node("Multiplication",Multiplication)

# add edges
graph.add_edge(START,'Addition')
graph.add_edge(START,'Multiplication')
graph.add_edge("Addition",END)
graph.add_edge("Multiplication",END)

# Compile Graph
workflow = graph.compile()

# Invoke Graph
initial_state = {"a" : 2 ,"b" : 5}
final_state = workflow.invoke(initial_state)
print(final_state)

