from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str

def compliment(state: AgentState) -> AgentState:
    """Simple node that compliments the user"""
    state['name'] = "Bob, you're doing an amazing job learning LangGraph!"
    return state

graph = StateGraph(AgentState);
graph.add_node("compliment", compliment);
graph.set_entry_point("compliment");
graph.set_finish_point("compliment");
agent = graph.compile();

result = agent.invoke({"name": "Bob"});
print(result["name"]);