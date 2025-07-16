# Agent Group Creation Guide

## Overview

This guide provides a standardized template and process for creating new agent groups that follow our established refactoring framework. Use this template when you need to create a new multi-step processing pipeline with proper error handling, logging, and consistency.

## Quick Start Template

When creating a new agent group, provide the following information:

### Required Information
1. **Agent Group Name**: What should the class be called? (e.g., `DocumentProcessingAgentGroup`)
2. **Output Extension**: What file extension should the final output have? (e.g., `"json"`, `"txt"`, `"xml"`)
3. **Agent List**: Ordered list of agents to execute in sequence
4. **Special Parameters**: Any agents that require additional parameters (like `scenario_id`)
5. **Custom Logic**: Any special routing or content flow requirements

### Agent List Format
Provide your agents in this format:
```
1. AgentClassName - Description of what it does
2. AgentClassName - Description of what it does  
3. AgentClassName - Description of what it does
```

### Example Request
```
Agent Group Name: DocumentProcessingAgentGroup
Output Extension: json
Agents:
1. PDFParserAgent - Extract text from PDF documents
2. TextCleanupAgent - Clean and normalize the extracted text
3. EntityExtractionAgent - Extract named entities and relationships
4. JSONFormatterAgent - Format results as structured JSON
5. ValidationAgent - Validate the final JSON output

Special Parameters: EntityExtractionAgent requires scenario_id
Custom Logic: Steps 4 and 5 both use output from step 3
```

## Generated Template Structure

When you provide the agent list, the following standardized template will be generated:

```python
from src.agents.transform_agent import TransformAgent
from src.agents.workflow_runner import WorkflowRunner
from src.scenario_models import TDPDocument
from typing import Tuple, TYPE_CHECKING

# Import your specific agents
from src.agents.your_agent_1 import YourAgent1
from src.agents.your_agent_2 import YourAgent2
# ... additional imports

if TYPE_CHECKING:
    from src.scenario_models import TDPDocument
    from src.agents.workflow_runner import WorkflowRunner


class YourAgentGroup(TransformAgent):
    output_ext = "your_extension"

    def __init__(self, step_num, runner: "WorkflowRunner", **kwargs):
        # Store any special parameters
        # self.scenario_id = scenario_id  # if needed
        self.runner = runner
        super().__init__(step_num, runner)

    def process_tdp_content(self, tdp: "TDPDocument") -> Tuple[bool, "TDPDocument"]:
        print("Starting Your Agent Group")
        
        # Step 1: First Agent
        success, step_one_content, step_one_doc = self.execute_step(
            YourAgent1(1, self.runner), 
            None, 
            tdp, 
            "YourAgent1"
        )
        if not success: return success, step_one_doc

        # Step 2: Second Agent
        success, step_two_content, step_two_doc = self.execute_step(
            YourAgent2(2, self.runner), 
            step_one_content, 
            tdp, 
            "YourAgent2"
        )
        if not success: return success, step_two_doc

        # ... additional steps following the same pattern

        return success, final_doc
```

## Framework Requirements

### Constructor Pattern
All agent groups must follow this constructor pattern:
```python
def __init__(self, step_num, runner: "WorkflowRunner", **kwargs):
    # Store any special parameters first
    self.special_param = special_param  # if needed
    
    # Always store runner and call super
    self.runner = runner
    super().__init__(step_num, runner)
```

### Method Signature
All agent groups must implement this exact method signature:
```python
def process_tdp_content(self, tdp: "TDPDocument") -> Tuple[bool, "TDPDocument"]:
```

### Step Pattern
Each step must follow this exact 3-line pattern:
```python
# Step N: Description
success, content, doc = self.execute_step(Agent(N, self.runner), input_content, tdp, "AgentName")
if not success: return success, doc
```

### Error Handling
- Each step automatically returns on failure with graceful fallback
- No manual try/catch blocks needed
- Built-in logging and AI document creation

## Special Cases

### Agents with Additional Parameters
For agents requiring extra parameters (like `scenario_id`):
```python
# Store in constructor
def __init__(self, step_num, runner: "WorkflowRunner", scenario_id: str):
    self.scenario_id = scenario_id
    self.runner = runner
    super().__init__(step_num, runner)

# Use in execute_step
success, content, doc = self.execute_step(
    SpecialAgent(step_num, self.scenario_id, self.runner), 
    input_content, 
    tdp, 
    "SpecialAgent"
)
```

### Custom Content Routing
For complex routing (like multiple steps using the same input):
```python
# Step 3: Process content
success, step_three_content, step_three_doc = self.execute_step(...)
if not success: return success, step_three_doc

# Step 4: Uses step 3 output
success, step_four_content, step_four_doc = self.execute_step(..., step_three_content, ...)
if not success: return success, step_four_doc

# Step 5: Also uses step 3 output (not step 4)
success, step_five_content, step_five_doc = self.execute_step(..., step_three_content, ...)
if not success: return success, step_five_doc
```

### Agents with Special Instructions
For agents that need configuration:
```python
# In the step execution
agent = SpecialAgent(step_num, self.runner)
agent.set_special_instructions(some_config)
success, content, doc = self.execute_step(agent, input_content, tdp, "SpecialAgent")
```

## Import Requirements

### Standard Imports (Always Required)
```python
from src.agents.transform_agent import TransformAgent
from src.agents.workflow_runner import WorkflowRunner
from src.scenario_models import TDPDocument
from typing import Tuple, TYPE_CHECKING
```

### TYPE_CHECKING Imports (Recommended)
```python
if TYPE_CHECKING:
    from src.scenario_models import TDPDocument
    from src.agents.workflow_runner import WorkflowRunner
```

### Agent-Specific Imports
```python
# Import each agent class you'll be using
from src.agents.your_specific_agent import YourSpecificAgent
```

## Validation Checklist

Before considering your agent group complete, verify:

- [ ] Follows exact constructor pattern with `runner` parameter
- [ ] Implements correct `process_tdp_content` signature
- [ ] Each step uses the 3-line `execute_step` pattern
- [ ] All agent imports are present
- [ ] Special parameters are properly stored and used
- [ ] Error handling returns appropriate fallback documents
- [ ] Custom content routing is correctly implemented
- [ ] Final return statement returns `(success, final_doc)`

## Examples

### Simple Linear Pipeline
```python
# 3-step linear processing
success, step_one_content, step_one_doc = self.execute_step(Agent1(1, self.runner), None, tdp, "Agent1")
if not success: return success, step_one_doc

success, step_two_content, step_two_doc = self.execute_step(Agent2(2, self.runner), step_one_content, tdp, "Agent2")
if not success: return success, step_two_doc

success, step_three_content, step_three_doc = self.execute_step(Agent3(3, self.runner), step_two_content, tdp, "Agent3")
if not success: return success, step_three_doc

return success, step_three_doc
```

### Complex Routing Pipeline
```python
# Steps 1-3 are linear
success, step_three_content, step_three_doc = self.execute_step(Agent3(3, self.runner), step_two_content, tdp, "Agent3")
if not success: return success, step_three_doc

# Steps 4 and 5 both use step 3 output
success, step_four_content, step_four_doc = self.execute_step(Agent4(4, self.runner), step_three_content, tdp, "Agent4")
if not success: return success, step_four_doc

success, step_five_content, step_five_doc = self.execute_step(Agent5(5, self.runner), step_three_content, tdp, "Agent5")
if not success: return success, step_five_doc

return success, step_five_doc
```

## Request Format

To create a new agent group, provide a request in this format:

---

**Agent Group Name**: `YourAgentGroupName`

**Output Extension**: `"ext"`

**Agents**:
1. `AgentClass1` - Description
2. `AgentClass2` - Description  
3. `AgentClass3` - Description

**Special Parameters**: (if any)
- `Agent2` requires `scenario_id`
- `Agent3` requires `config_path`

**Custom Logic**: (if any)
- Steps 4 and 5 both use output from step 3
- Agent2 needs special instructions set

---

This will generate a complete, framework-compliant agent group ready for use!
