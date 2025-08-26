from langgraph.graph import StateGraph,START,END
from typing import TypedDict

# State Structue
class BMIState(TypedDict):
    weight_kg : float
    height_m : float
    bmi : float
    category : str

def bmi_calculation(state:BMIState) -> BMIState:
    weight = state['weight_kg']
    hight = state['height_m']

    # calculate bmi here
    bmi = weight / (hight ** 2)

    # set bmi value to State
    state['bmi'] = bmi

    return state

def labeled_bmi(state:BMIState) -> BMIState:
    bmi = state['bmi']

    if bmi < 18.5:
        state['category'] = "Underweight"
    elif bmi >= 18.5 and bmi <= 24.9:
        state['category'] = "Normal"
    else:
        state['category'] = "Overweight"

    return state
    

# Create StateGraph 
graph = StateGraph(BMIState)

# Add Node to graph
graph.add_node("bmi_calculation",bmi_calculation)
graph.add_node("labeled_bmi",labeled_bmi)

# add edges to graph
graph.add_edge(START,'bmi_calculation')
graph.add_edge('bmi_calculation','labeled_bmi')
graph.add_edge('labeled_bmi',END)

# compile graph
workflow = graph.compile()

# invoke the graph
initial_state = {
    'weight_kg':64,
    'height_m': 2.3
}
final_state = workflow.invoke(initial_state)
print(final_state)

"""

# Show Graph 
from IPython.display import Image   
graph = Image(workflow.get_graph().draw_mermaid_png())

"""
