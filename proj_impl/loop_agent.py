from typing import TypedDict
import random
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    name: str
    random_nums: list[int]
    count: int

def greeting_node(state: AgentState) -> AgentState:
    """Greeting node"""
    state["name"] = "Hello, " + state["name"]
    state["random_nums"] = []
    state["count"] = 0
    return state
 
def random_nums_node(state: AgentState) -> AgentState:
    """Generate random numbers"""
    state["random_nums"].append(random.randint(1, 100))
    state["count"] = state["count"] + 1
    return state

def should_continue(state: AgentState) -> str:
    """Decision node to determine if the loop should continue"""
    if state["count"] < 5:
        return "loop"
    else:
        return "END"

graph = StateGraph(AgentState)
graph.add_node("greeting", greeting_node)
graph.add_node("random_nums", random_nums_node)
graph.add_edge(START, "greeting")
graph.add_edge("greeting", "random_nums")
graph.add_conditional_edges(
    "random_nums",
    should_continue,
    {
        "loop": "random_nums",
        "END": END
    }
)

agent = graph.compile()
result = agent.invoke({"name": "John"})
print(result)


