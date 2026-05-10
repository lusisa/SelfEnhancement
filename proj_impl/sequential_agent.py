from typing import TypedDict # Imports all the data types we need
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: str
    skills: list[str]
    final: str

def first_node(state: AgentState) -> AgentState:
    """First node that greets the user"""
    state["final"] = f"{state["name"]}, welcome to the system!"
    return state

def second_node(state: AgentState) -> AgentState:
    """Second node that asks the user for their age"""
    state["final"] = state["final"] + f" You are {state["age"]} years old!"
    return state

def third_node(state: AgentState) -> AgentState:
    """Third node that asks the user for their skills"""
    state["final"] = state["final"] + f" You have the following skills: {state["skills"]}"
    return state

graph = StateGraph(AgentState)
graph.add_node("first_n", first_node)
graph.add_node("second_n", second_node)
graph.add_edge("first_n", "second_n")
graph.add_node("third_n", third_node)
graph.add_edge("second_n", "third_n")
graph.set_entry_point("first_n")
graph.set_finish_point("third_n")
agent = graph.compile()

result = agent.invoke({"name": "John", "age": "20", "skills": ["Python", "Java", "C++"]})
print(result["final"])

