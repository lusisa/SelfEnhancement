
from typing import Dict, TypedDict
from langgraph.graph import StateGraph # framework that helps you design and manage the flow of tasks in your application usring a graph structure

# We now create an AgentState - shared data structure that keeps track of information as your application runs.
class AgentState(TypedDict): # Our state schema
    message: str

def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a greeting to the state"""
    state['message'] = "Hey " + state['message'] + ", how is your day going?"
    return state

graph = StateGraph(AgentState)

graph.add_node("greeter", greeting_node)

# For start/entry point, the parameter is the name of your node which you want the start node to connect to.
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")
app = graph.compile()


#from IPython.display import Image, display
#display(Image(app.get_graph().draw_mermaid_png()))

result = app.invoke({"message": "John"})
print(result["message"])
