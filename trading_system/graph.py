from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from .state import TradingState
from .agents.supervisor import supervisor
from .agents.technical_analyst import technical_analyst
from .agents.sentiment_analyst import sentiment_analyst
from .agents.macro_analyst import macro_analyst
from .agents.strategist import strategist
from .agents.risk_agent import risk_agent
from .agents.executor import executor
from .agents.news_researcher import news_researcher

# Production use:
# from langgraph.checkpoint.redis import RedisSaver
# from .config import config

def build_graph():
    builder = StateGraph(TradingState)
    
    # 1. Add Nodes
    builder.add_node("supervisor", supervisor.run)
    builder.add_node("technical_analyst", technical_analyst.run)
    builder.add_node("sentiment_analyst", sentiment_analyst.run)
    builder.add_node("macro_analyst", macro_analyst.run)
    builder.add_node("news_researcher", news_researcher.run)
    builder.add_node("strategist", strategist.run)
    builder.add_node("risk_agent", risk_agent.run)
    builder.add_node("executor", executor.run)
    
    # 2. Add Edges
    
    # Entry to Supervisor
    builder.add_edge(START, "supervisor")
    
    # Supervisor -> Parallel Analysts
    def route_to_analysts(state):
        return ["technical_analyst", "sentiment_analyst", "macro_analyst", "news_researcher"]
        
    builder.add_conditional_edges(
        "supervisor",
        route_to_analysts,
        ["technical_analyst", "sentiment_analyst", "macro_analyst", "news_researcher"]
    )
    
    # Analysts -> Strategist (Synchronization point)
    builder.add_edge("technical_analyst", "strategist")
    builder.add_edge("sentiment_analyst", "strategist")
    builder.add_edge("macro_analyst", "strategist")
    builder.add_edge("news_researcher", "strategist")
    
    # Strategist -> Risk Agent
    builder.add_edge("strategist", "risk_agent")
    
    # Risk Agent -> Executor (Conditional)
    def route_to_execution(state):
        if state.get("risk_approved", False):
            return "executor"
        else:
            return END
            
    builder.add_conditional_edges(
        "risk_agent",
        route_to_execution,
        {
            "executor": "executor",
            END: END
        }
    )
    
    # Executor -> END
    builder.add_edge("executor", END)
    
    # 3. Compile
    checkpointer = MemorySaver() # For dev/demo
    
    return builder.compile(checkpointer=checkpointer)
