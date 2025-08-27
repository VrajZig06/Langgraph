from langgraph.graph import StateGraph,START,END
from typing import TypedDict

# Create State Class
class Workflow_State(TypedDict):
    a : int
    iterationCount : 0

def square(state:Workflow_State) -> Workflow_State:
    a = state['a']
    iterationCount = state['iterationCount'] + 1
    return {"a" : a**2,"iterationCount" :iterationCount}

def check_iteration(state:Workflow_State) -> Workflow_State:
    iterationCount = state['iterationCount']

    if iterationCount < 2:
        return "square"
    else:
        return END

# Create Graph
graph = StateGraph(Workflow_State)

# Add Nodes 
graph.add_node("square",square)
graph.add_node("check_iteration",check_iteration)

# Add Edges
graph.add_edge(START,"square")
graph.add_conditional_edges("square",check_iteration)

# Compile Graph
workflow = graph.compile()

# Invoke Workflow
initial_state = {"a" : 2,"iterationCount" : 0}
final_state = workflow.invoke(initial_state)
print(final_state)
