from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated,Literal
import operator

# Create State Class
class Workflow_State(TypedDict):
    a : int
    b : int
    c : int
    discriminant : float
    roots : dict
    equation : str
    
def find_Discriminant(state:Workflow_State) -> Workflow_State:
    a = state['a']
    b = state['b']
    c = state['c']

    descriminant = ((b ** 2) - (4 * a * c)) ** 0.5
    descriminant = descriminant if isinstance(descriminant, float) else -1

    return {"discriminant" : descriminant}

def descriminant_equal_to_zero(state: Workflow_State) -> Workflow_State:
    b = state['b']
    a = state['a']
    root = -b / (4 * a)

    return {"roots" : {"root" : root}}


def descriminant_greater_then_zero(state:Workflow_State) -> Workflow_State:
    descriminant = state['discriminant']
    a = state['a']
    b = state['b']

    root1 = - (b - descriminant)/(2 * a)
    root2 = - (b + descriminant)/(2 * a)

    return {"roots" : {
        "root1" : root1,
        "root2" : root2
    }}

def descriminant_less_then_zero(state:Workflow_State) -> Workflow_State:
    return {"roots" : {"message" : "There is no roots!"}}

def print_equation(state:Workflow_State) :
    a = state['a']
    b = state['b']
    c = state['c']

    if b > 0 and c > 0:
        return {"equation" : f"{a}x**2+{b}x+{c}=0"}
    elif b < 0 and c > 0:
        return {"equation" :f"{a}x**2{b}x+{c}=0"}
    elif b > 0 and c < 0:
        return {"equation" :f"{a}x**2+{b}x{c}=0"}
    else: 
        return {"equation":f"{a}x**2{b}x{c}=0"}


def check_condition(state:Workflow_State) -> Literal['descriminant_equal_to_zero','descriminant_greater_then_zero','descriminant_less_then_zero']:
    descriminant = state['discriminant']

    if descriminant > 0:
        return "descriminant_greater_then_zero"
    elif descriminant == 0:
        return "descriminant_equal_to_zero"
    else: 
        return "descriminant_less_then_zero"

# Create Graph
graph = StateGraph(Workflow_State)

# Add Nodes
graph.add_node('find_Discriminant',find_Discriminant)
graph.add_node('descriminant_equal_to_zero',descriminant_equal_to_zero)
graph.add_node("descriminant_greater_then_zero",descriminant_greater_then_zero)
graph.add_node('descriminant_less_then_zero',descriminant_less_then_zero)
graph.add_node('print_equation',print_equation)

# Create Edges
graph.add_edge(START,"print_equation")
graph.add_edge("print_equation","find_Discriminant")
graph.add_conditional_edges("find_Discriminant",check_condition)
graph.add_edge('descriminant_equal_to_zero',END)
graph.add_edge('descriminant_greater_then_zero',END)
graph.add_edge('descriminant_less_then_zero',END)

# Compile Graph 
workflow = graph.compile()

# Invoke Graph

# initil_state = {"a" : 1, "b" : -5, "c" :6} 
# --> {'a': 1, 'b': -5, 'c': 6, 'discriminant': 1.0, 'roots': {'root1': 3.0, 'root2': 2.0}, 'equation': '1x**2-5x+6=0'}

# initil_state = {"a" : 1, "b" : 1, "c" :1} 
# --> {'a': 1, 'b': 1, 'c': 1, 'discriminant': -1, 'roots': {'message': 'There is no roots!'}, 'equation': '1x**2+1x+1=0'}

initil_state = {"a" : 1, "b" : -4, "c" :4} 
# --> {'a': 1, 'b': -4, 'c': 4, 'discriminant': 0.0, 'roots': {'root': 1.0}, 'equation': '1x**2-4x+4=0'}


final_state = workflow.invoke(initil_state)
print(final_state)






    

