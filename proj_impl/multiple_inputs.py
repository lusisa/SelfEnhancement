from turtle import st
from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
     values: list[int]
     name: str
     result: str

def process_values(state: AgentState) -> AgentState:
    """This function handles multiple different inputs"""
    print(f"old state: {state}")

    state["result"] = f"Hi there {state["name"]}! Your sum = {sum(state["values"])}"
    print(f"new state: {state}")
    return state

graph = StateGraph(AgentState)

graph.add_node("processor", process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")
agent = graph.compile()

from IPython.display import Image, display
display(Image(agent.get_graph().draw_mermaid_png()))


anwser = agent.invoke({"values": [1, 2, 3, 4, 5], "name": "Bob"})
print(anwser)
print(anwser["result"])

anwser = agent.invoke({"values": [10, 20, 30, 40, 50], "name": "Alice"})
print(anwser)
print(anwser["result"])

anwser = agent.invoke({"values": [100, 200, 300, 400, 500], "name": "Charlie"})
print(anwser)
print(anwser["result"])
