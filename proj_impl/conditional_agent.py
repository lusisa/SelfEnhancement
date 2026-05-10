from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    first_num: int
    second_num: int
    operation1: str
    final_num1: int
    third_num: int
    fourth_num: int
    operation2: str
    final_num2: int

def add(state: AgentState) -> AgentState:
    """Add the first two numbers"""
    state["final_num1"] = state["first_num"] + state["second_num"]
    return state

def subtract(state: AgentState) -> AgentState:
    """Subtract the first two numbers"""
    state["final_num1"] = state["first_num"] - state["second_num"]
    return state

def add2(state: AgentState) -> AgentState:
    """Add the second two numbers"""
    state["final_num2"] = state["third_num"] + state["fourth_num"]
    return state

def subtract2(state: AgentState) -> AgentState:
    """Subtract the second two numbers"""
    state["final_num2"] = state["third_num"] - state["fourth_num"]
    return state

def decision_node(state: AgentState) -> str:
    """Decision node to determine the operation1"""
    if state["operation1"] == "+":
        return "add_operation1"
    elif state["operation1"] == "-":
        return "subtract_operation1"
   

def decision_node2(state: AgentState) -> str:
    """Decision node to determine the operation2"""
    if state["operation2"] == "+":
        return "add_operation2"
    elif state["operation2"] == "-":
        return "subtract_operation2"


graph = StateGraph(AgentState)
graph.add_node("add_node", add)
graph.add_node("subtract_node", subtract)
graph.add_node("add_node2", add2)
graph.add_node("subtract_node2", subtract2)
graph.add_node("router1", lambda state: state)
graph.add_node("router2", lambda state: state)

graph.add_edge(START, "router1")
graph.add_conditional_edges(
    "router1", 
    decision_node,
    {
        # Edges for the decision node
        "add_operation1": "add_node",
        "subtract_operation1": "subtract_node"
    }
)
graph.add_edge("add_node", "router2")
graph.add_edge("subtract_node", "router2")
graph.add_conditional_edges(
    "router2",
    decision_node2,
    {
        "add_operation2": "add_node2",
        "subtract_operation2": "subtract_node2"
    }
)
graph.add_edge("add_node2", END)
graph.add_edge("subtract_node2", END)
agent = graph.compile() 

result = agent.invoke({"first_num": 10, "operation1": "-", "second_num": 5, "third_num": 7, "fourth_num": 2, 
    "operation2": "+"})
print(result)
