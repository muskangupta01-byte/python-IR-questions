from resolution_system import IssueResolutionSystem, Helper03

def run_tests():
    # 1. Setup
    system = IssueResolutionSystem()
    helper = Helper03()
    
    # Initialize
    issue_types = ["wrong product received", "order delayed", "cancel delivery", "damaged product received"]
    # Mapping: 0: Wrong, 1: Delayed, 2: Cancel, 3: Damaged
    system.init(issue_types, helper)
    
    print("--- Adding Agents ---")
    # Add Agents
    print(f"Add A-0: {system.addAgent('A-0', [0, 1, 3])}") # Skills: Wrong, Delayed, Damaged
    print(f"Add A-1: {system.addAgent('A-1', [1, 2, 3])}") # Skills: Delayed, Cancel, Damaged
    print(f"Add A-2: {system.addAgent('A-2', [1, 3])}")    # Skills: Delayed, Damaged
    
    print("\n--- Workflow 1: Strategy 1 (Expertise) ---")
    # Create Issue I-0 (Type 3: Damaged product)
    print(f"Create I-0: {system.createIssue('I-0', 'Order-0', 3, 'damaged product')}")
    
    # Assign I-0 using Strategy 1 (Most Resolved of Type 3)
    # Initially all have 0 resolved. Tie break -> any one (Logic picks first/max default)
    assigned_agent = system.assignIssue('I-0', 1)
    print(f"Assigned I-0 to: {assigned_agent}") 
    
    # Resolve I-0
    system.resolveIssue('I-0', "Refunded")
    print(f"I-0 Resolved by {assigned_agent}")

    print("\n--- Workflow 2: Strategy 1 (Expertise Impact) ---")
    # Create Issue I-1 (Type 3: Damaged product) - Same type as before
    print(f"Create I-1: {system.createIssue('I-1', 'Order-1', 3, 'damaged again')}")
    
    # Assign I-1 using Strategy 1
    # Logic: Agent assigned in Workflow 1 now has 1 resolved issue of Type 3. 
    # Others have 0. The previous agent should be picked again.
    assigned_agent_2 = system.assignIssue('I-1', 1)
    print(f"Assigned I-1 to: {assigned_agent_2} (Should match previous agent)")

    print("\n--- Workflow 3: Strategy 0 (Load Balancing) ---")
    # Create I-2 (Type 1: Order Delayed)
    print(f"Create I-2: {system.createIssue('I-2', 'Order-2', 1, 'delayed')}")
    
    # Assign I-2 using Strategy 0 (Lowest Total Open)
    # The agent from Workflow 2 currently has I-1 OPEN.
    # The other agents have 0 open. System should pick one of the idle agents.
    assigned_agent_3 = system.assignIssue('I-2', 0)
    print(f"Assigned I-2 to: {assigned_agent_3} (Should be different from I-1 agent)")

    print("\n--- History Check ---")
    history = system.getAgentHistory(assigned_agent)
    print(f"History for {assigned_agent}: {history}")

if __name__ == "__main__":
    run_tests()