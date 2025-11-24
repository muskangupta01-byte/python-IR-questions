from collections import defaultdict
from typing import List

class Issue:
    def __init__(self, issue_id: str, order_id: str, issue_type: int, description: str):
        self.issue_id = issue_id
        self.order_id = order_id
        self.issue_type = issue_type
        self.description = description
        self.status = "CREATED"  # Statuses: CREATED, ASSIGNED, RESOLVED
        self.assigned_agent_id = None
        self.resolution = None

class Agent:
    def __init__(self, agent_id: str, expertise: List[int]):
        self.agent_id = agent_id
        # Set of expertise for O(1) lookup
        self.expertise = set(expertise)
        
        # Data for strategies
        self.total_open_issues = 0
        self.open_issues_by_type = defaultdict(int)
        self.resolved_issues_by_type = defaultdict(int)
        
        # History
        self.resolved_issue_ids = []

    def assign_issue(self, issue_type: int):
        """Updates counters when an issue is assigned."""
        self.total_open_issues += 1
        self.open_issues_by_type[issue_type] += 1

    def resolve_issue(self, issue_id: str, issue_type: int):
        """Updates counters and history when an issue is resolved."""
        self.total_open_issues -= 1
        self.open_issues_by_type[issue_type] -= 1
        self.resolved_issues_by_type[issue_type] += 1
        self.resolved_issue_ids.append(issue_id)