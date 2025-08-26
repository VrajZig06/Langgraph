from langgraph.graph import StateGraph,START,END
from typing import TypedDict

# State Structue
class BMIState(TypedDict):
    weight_kg : float
    height_m : float
    bmi : float

def bmi_calculation(state:BMIState):
    weight = state['weight_kg']
    hight = state['height_m']

    # calculate bmi here
    bmi = weight / (hight ** 2)

    # set bmi value to State
    state['bmi'] = bmi

    return state

# Create StateGraph 
graph = StateGraph(BMIState)

# Add Node to graph
graph.add_node("bmi_calculation",bmi_calculation)

# add edges to graph
graph.add_edge(START,'bmi_calculation')
graph.add_edge('bmi_calculation',END)

# compile graph
workflow = graph.compile()

# invoke the graph
initial_state = {
    'weight_kg':64,
    'height_m': 2.3
}
final_state = workflow.invoke(initial_state)

"""

# Show Graph 
from IPython.display import Image   
graph = Image(workflow.get_graph().draw_mermaid_png())

"""

