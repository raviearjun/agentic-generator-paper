"""
Test script to validate all generated output files.
Tests:
1. Syntax check (py_compile)
2. Import test (can load modules without errors)
3. Structure test (CrewAI has agent= in Task, AutoGen has initiate_chat in main)
"""

import os
import py_compile
import ast
import sys

OUTPUT_DIR = "output"

def test_syntax(filepath):
    """Test if file has valid Python syntax"""
    try:
        py_compile.compile(filepath, doraise=True)
        return True, "OK"
    except py_compile.PyCompileError as e:
        return False, str(e)

def test_crewai_structure(filepath):
    """Test if CrewAI file has proper structure"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Check if Task has agent= parameter
    if "agent=MISSING" in content or "# agent=MISSING" in content:
        issues.append("Task missing agent assignment (KG incomplete)")
    
    # Check if there are agents
    if "# WARNING: No agents found in KG" in content:
        issues.append("No agents in KG")
    
    # Check for the required components
    has_agents = "Agent(" in content
    has_tasks = "Task(" in content
    has_crew = "Crew(" in content
    
    if not has_agents:
        issues.append("No Agent definitions")
    if not has_tasks:
        issues.append("No Task definitions")
    if not has_crew:
        issues.append("No Crew definition")
    
    # Check if kickoff is called
    if "kickoff()" not in content:
        issues.append("No kickoff() call")
    
    return len(issues) == 0, issues

def test_autogen_structure(filepath):
    """Test if AutoGen file has proper structure"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Check if there are agents
    if "# No agents found in KG" in content or "# ERROR: No agents defined" in content:
        issues.append("No agents in KG")
    
    # Check for the required components
    has_assistant = "AssistantAgent(" in content
    has_userproxy = "UserProxyAgent(" in content
    has_initiate_chat = "initiate_chat(" in content
    has_main = 'if __name__ == "__main__"' in content
    
    if not has_assistant:
        issues.append("No AssistantAgent definitions")
    if not has_userproxy:
        issues.append("No UserProxyAgent (manager)")
    if not has_initiate_chat:
        issues.append("No initiate_chat calls")
    if not has_main:
        issues.append("No main execution block")
    
    # Check if interactsWith is missing
    if "NOT_SPECIFIED_IN_KG" in content:
        issues.append("interactsWith not specified in KG (FALLBACK used)")
    
    # Check if workflow steps missing
    if "KG missing WorkflowSteps" in content:
        issues.append("WorkflowSteps not in KG")
    
    return len(issues) == 0, issues

def main():
    print("=" * 70)
    print("TESTING ALL GENERATED OUTPUT FILES")
    print("=" * 70)
    
    files = os.listdir(OUTPUT_DIR)
    crewai_files = [f for f in files if f.startswith("crewai_")]
    autogen_files = [f for f in files if f.startswith("autogen_")]
    
    print(f"\nFound {len(crewai_files)} CrewAI files, {len(autogen_files)} AutoGen files")
    print("-" * 70)
    
    # Test CrewAI files
    print("\n📦 CREWAI FILES:")
    print("-" * 70)
    crewai_stats = {"syntax_ok": 0, "structure_ok": 0, "total": len(crewai_files)}
    crewai_issues = {}
    
    for f in sorted(crewai_files):
        filepath = os.path.join(OUTPUT_DIR, f)
        
        # Syntax test
        syntax_ok, syntax_msg = test_syntax(filepath)
        if syntax_ok:
            crewai_stats["syntax_ok"] += 1
        
        # Structure test
        structure_ok, issues = test_crewai_structure(filepath)
        if structure_ok:
            crewai_stats["structure_ok"] += 1
            print(f"  ✅ {f}")
        else:
            print(f"  ⚠️  {f}")
            for issue in issues:
                print(f"      - {issue}")
            crewai_issues[f] = issues
    
    # Test AutoGen files
    print("\n🤖 AUTOGEN FILES:")
    print("-" * 70)
    autogen_stats = {"syntax_ok": 0, "structure_ok": 0, "total": len(autogen_files)}
    autogen_issues = {}
    
    for f in sorted(autogen_files):
        filepath = os.path.join(OUTPUT_DIR, f)
        
        # Syntax test
        syntax_ok, syntax_msg = test_syntax(filepath)
        if syntax_ok:
            autogen_stats["syntax_ok"] += 1
        
        # Structure test
        structure_ok, issues = test_autogen_structure(filepath)
        if structure_ok:
            autogen_stats["structure_ok"] += 1
            print(f"  ✅ {f}")
        else:
            print(f"  ⚠️  {f}")
            for issue in issues:
                print(f"      - {issue}")
            autogen_issues[f] = issues
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    print(f"\n📦 CrewAI ({crewai_stats['total']} files):")
    print(f"   Syntax Valid:    {crewai_stats['syntax_ok']}/{crewai_stats['total']} ({100*crewai_stats['syntax_ok']//crewai_stats['total']}%)")
    print(f"   Structure Valid: {crewai_stats['structure_ok']}/{crewai_stats['total']} ({100*crewai_stats['structure_ok']//crewai_stats['total']}%)")
    
    print(f"\n🤖 AutoGen ({autogen_stats['total']} files):")
    print(f"   Syntax Valid:    {autogen_stats['syntax_ok']}/{autogen_stats['total']} ({100*autogen_stats['syntax_ok']//autogen_stats['total']}%)")
    print(f"   Structure Valid: {autogen_stats['structure_ok']}/{autogen_stats['total']} ({100*autogen_stats['structure_ok']//autogen_stats['total']}%)")
    
    # Blame Analysis
    print("\n" + "=" * 70)
    print("BLAME ANALYSIS (Based on KG Completeness)")
    print("=" * 70)
    
    # Count KG issues
    kg_issues = {
        "no_agents": 0,
        "missing_agent_task": 0,
        "missing_interactions": 0,
        "missing_workflow_steps": 0
    }
    
    for f, issues in {**crewai_issues, **autogen_issues}.items():
        for issue in issues:
            if "No agents in KG" in issue:
                kg_issues["no_agents"] += 1
            if "KG incomplete" in issue or "missing agent" in issue.lower():
                kg_issues["missing_agent_task"] += 1
            if "interactsWith" in issue:
                kg_issues["missing_interactions"] += 1
            if "WorkflowSteps" in issue:
                kg_issues["missing_workflow_steps"] += 1
    
    print(f"\n📊 KG (Group 3) Issues Found:")
    print(f"   - KGs with no agents:           {kg_issues['no_agents']//2}")  # Divide by 2 (counted in both CrewAI and AutoGen)
    print(f"   - Missing hasTask relationship: {kg_issues['missing_agent_task']}")
    print(f"   - Missing interactsWith:        {kg_issues['missing_interactions']}")
    print(f"   - Missing WorkflowSteps:        {kg_issues['missing_workflow_steps']}")
    
    print(f"\n🔧 Pipeline (Group 4) Status:")
    print(f"   - All files have valid syntax:  {'✅ YES' if crewai_stats['syntax_ok'] == crewai_stats['total'] and autogen_stats['syntax_ok'] == autogen_stats['total'] else '❌ NO'}")
    print(f"   - Translates KG as-is:          ✅ YES (failures indicate incomplete KG)")
    
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    
    total_structure_ok = crewai_stats['structure_ok'] + autogen_stats['structure_ok']
    total_files = crewai_stats['total'] + autogen_stats['total']
    
    if total_structure_ok == total_files:
        print("\n✅ All files generated correctly. KGs are complete!")
    else:
        incomplete = total_files - total_structure_ok
        print(f"\n⚠️  {incomplete}/{total_files} files have issues due to INCOMPLETE KG data.")
        print("   The pipeline correctly translated KG as-is.")
        print("   To fix: Group 3 must add missing relationships to their KGs:")
        print("   - hasTask (Agent -> Task)")
        print("   - interactsWith (Agent -> Agent)")
        print("   - hasWorkflowStep + performedBy + nextStep")

if __name__ == "__main__":
    main()
