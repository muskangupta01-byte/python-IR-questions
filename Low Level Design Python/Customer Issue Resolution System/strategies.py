from typing import List, Optional
from models import Agent

class AssignmentStrategy:
    @staticmethod
    def select_agent(candidates: List[Agent], strategy_code: int, issue_type: int) -> Optional[Agent]:
        """
        Selects an agent from the candidates list based on the strategy code.
        Returns None if candidates list is empty.
        """
        if not candidates:
            return None

        # Strategy 0: Lowest number of total issues open
        if strategy_code == 0:
            return min(candidates, key=lambda agent: agent.total_open_issues)

        # Strategy 1: Most experience (resolved issues) of this specific issue type
        elif strategy_code == 1:
            return max(candidates, key=lambda agent: agent.resolved_issues_by_type[issue_type])

        # Strategy 2: Least open issues of this specific issue type
        elif strategy_code == 2:
            return min(candidates, key=lambda agent: agent.open_issues_by_type[issue_type])
            
        return candidates[0] # Fallback