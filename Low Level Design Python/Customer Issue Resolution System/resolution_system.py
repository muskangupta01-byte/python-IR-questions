import threading
from typing import List, Dict
from models import Agent, Issue
from strategies import AssignmentStrategy

class Helper03:
    """Mock Helper class as per problem statement"""
    def log(self, message):
        print(f"[LOG]: {message}")

class IssueResolutionSystem:
    def __init__(self):
        self.issue_types = []
        self.helper = None
        # Maps for O(1) access
        self.agents: Dict[str, Agent] = {}
        self.issues: Dict[str, Issue] = {}
        
        # RLock (Reentrant Lock) to handle thread safety
        self._lock = threading.RLock()

    def init(self, issue_types: List[String], helper: Helper03):
        with self._lock:
            self.issue_types = issue_types
            self.helper = helper
            self.agents.clear()
            self.issues.clear()
            if self.helper:
                self.helper.log("System Initialized")

    def addAgent(self, agent_id: str, expertise: List[int]) -> str:
        with self._lock:
            if agent_id in self.agents:
                return "agent already exists"
            
            new_agent = Agent(agent_id, expertise)
            self.agents[agent_id] = new_agent
            return "success"

    def createIssue(self, issue_id: str, order_id: str, issue_type: int, description: str) -> str:
        with self._lock:
            if issue_id in self.issues:
                return "issue already exists"
            
            if issue_type < 0 or issue_type >= len(self.issue_types):
                return "invalid issue type"
            
            new_issue = Issue(issue_id, order_id, issue_type, description)
            self.issues[issue_id] = new_issue
            return "issue created"

    def assignIssue(self, issue_id: str, assign_strategy: int) -> str:
        with self._lock:
            issue = self.issues.get(issue_id)
            
            if not issue:
                return "issue doesn't exist"
            
            if issue.status != "CREATED":
                return "issue already assigned"
            
            # Filter agents who have the required expertise
            qualified_agents = [
                agent for agent in self.agents.values() 
                if issue.issue_type in agent.expertise
            ]
            
            if not qualified_agents:
                return "agent with expertise doesn't exist"
            
            # Apply Strategy
            selected_agent = AssignmentStrategy.select_agent(
                qualified_agents, assign_strategy, issue.issue_type
            )
            
            # Perform Assignment
            selected_agent.assign_issue(issue.issue_type)
            issue.assigned_agent_id = selected_agent.agent_id
            issue.status = "ASSIGNED"
            
            # Log using helper if needed
            if self.helper:
                self.helper.log(f"Assigned {issue_id} to {selected_agent.agent_id}")
                
            return selected_agent.agent_id

    def resolveIssue(self, issue_id: str, resolution: str):
        with self._lock:
            issue = self.issues.get(issue_id)
            
            # We assume based on prompt issueId is always valid and refers to existing issue
            if issue and issue.status == "ASSIGNED":
                agent = self.agents[issue.assigned_agent_id]
                
                # Update Agent Stats
                agent.resolve_issue(issue_id, issue.issue_type)
                
                # Update Issue Status
                issue.status = "RESOLVED"
                issue.resolution = resolution

    def getAgentHistory(self, agent_id: str) -> List[str]:
        with self._lock:
            agent = self.agents.get(agent_id)
            if not agent:
                return []
            # Return a copy of the list to maintain thread safety outside the lock
            return list(agent.resolved_issue_ids)