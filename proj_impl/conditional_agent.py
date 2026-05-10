from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    first_num: int
    operation: str
    second_num: int
    final_num: int

def add(state: AgentState) -> AgentState:
    """Add the two numbers"""
    state["final_num"] = state["first_num"] + state["second_num"]
    return state

def subtract(state: AgentState) -> AgentState:
    """Subtract the two numbers"""
    state["final_num"] = state["first_num"] - state["second_num"]
    return state

def multiply(state: AgentState) -> AgentState:
    """Multiply the two numbers"""
    state["final_num"] = state["first_num"] * state["second_num"]
    return state

def divide(state: AgentState) -> AgentState:
    """Divide the two numbers"""
    state["final_num"] = state["first_num"] / state["second_num"]
    return state

def decision_node(state: AgentState) -> str:
    """Decision node to determine the operation"""
    if state["operation"] == "+":
        return "add_operation"
    elif state["operation"] == "-":
        return "subtract_operation"
    elif state["operation"] == "*":
        return "multiply_operation"
    elif state["operation"] == "/":
        return "divide_operation"

graph = StateGraph(AgentState)
graph.add_node("add_node", add)
graph.add_node("subtract_node", subtract)
graph.add_node("multiply_node", multiply)
graph.add_node("divide_node", divide)
graph.add_node("router", lambda state: state)

graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router", 
    decision_node,
    {
        # Edges for the decision node
        "add_operation": "add_node",
        "subtract_operation": "subtract_node",
        "multiply_operation": "multiply_node",
        "divide_operation": "divide_node",
    }
)

graph.add_edge("add_node", END)
graph.add_edge("subtract_node", END)
graph.add_edge("multiply_node", END)
graph.add_edge("divide_node", END)
agent = graph.compile() 

result = agent.invoke({"first_num": 10, "operation": "*", "second_num": 20})
print(result["final_num"])