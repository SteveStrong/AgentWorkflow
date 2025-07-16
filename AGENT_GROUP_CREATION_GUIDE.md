# Agent Group Creation Guide

## Overview

This guide provides a standardized template and process for creating new agent groups that follow our established refactoring framework. Use this template when you need to create a new multi-step processing pipeline with proper error handling, logging, and consistency.

## TransformAgent Base Class

All agent groups inherit from `TransformAgent`, which provides the foundation for the framework. Here is the complete implementation that should be copied when recreating the framework:

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Set, TYPE_CHECKING, Tuple
import re

if TYPE_CHECKING:
    from src.scenario_models import AIDocument, TDPDocument
    from src.agents.workflow_runner import WorkflowRunner


class TransformAgent(ABC):
    input_agents: List[str]
    description: str = ""
    output_ext: str

    def __init__(self, step_num, runner: "WorkflowRunner" = None):
        if not self.output_ext:
            raise ValueError(
                f"Output extension not provided for {self.__class__.__name__}"
            )

        self.step_num = step_num
        self.runner = runner

    def compute_filename(self, source_filename: str) -> str:
        # Extract base name (without extension if present)
        if "." in source_filename:
            base_name, ext = source_filename.rsplit(".", 1)
        else:
            base_name = source_filename

        # Check if base_name ends with _x (where x is a digit sequence)
        match = re.search(r"_(\d+)$", base_name)
        if match:
            new_name = re.sub(r"_\d+$", f"_{self.step_num}", base_name)
        else:
            # Append _step_num to the base name
            new_name = f"{base_name}_{self.step_num}"

        return f"{new_name}.{self.output_ext}"

    def create_ai_document(
        self,
        source_doc: "TDPDocument",
        description: str = "",
    ) -> "AIDocument":
        """
        Create an AIDocument instance from any TDPDocument (including AIDocument).
        Since AIDocument inherits from TDPDocument, this works for both initial 
        TDPDocuments and chained AIDocuments.

        Args:
            source_doc: The source document (TDPDocument or AIDocument)
            description: Document description (optional)

        Returns:
            AIDocument instance
        """
        from src.scenario_models import AIDocument

        return AIDocument(
            FileName=self.runner.compute_ai_doc_filename(
                source_doc.FileName, self.output_ext
            ),
            Description=description,
            AgentName=self.__class__.__name__,
            SourceFileName=source_doc.FileName,
            SourceURL=source_doc.URL,
        )

    def execute_step(
        self,
        agent: "TransformAgent",
        input_content: bytes = None,
        source_doc: "TDPDocument" = None,
    ) -> Tuple[bool, bytes, "AIDocument"]:
        """
        Execute a complete pipeline step with standardized error handling.
        
        Args:
            agent: The agent to execute
            input_content: The content to process (or None to get from source_doc)
            source_doc: Document to create AI doc from (and get content from if input_content is None)
        
        Returns:
            Tuple[bool, content, ai_doc] - (success, output_content, ai_document)
        """
        # Extract agent name from class
        step_name = agent.__class__.__name__
        
        # Create AI document
        ai_doc = agent.create_ai_document(source_doc)
        
        # Start logging
        print(f"Starting {step_name}")
        
        try:
            # Get content if not provided (for first step)
            if input_content is None:
                scenario_id = self.runner.get_scenario().Id
                input_content = source_doc.get_content(scenario_id)
                
            # Execute the step
            step_content = agent.process_tdp_content(input_content)
            self.runner.ai_doc_success(ai_doc, step_content)
            
            # Completion logging
            print(f"Finished {step_name}")
                
            return True, step_content, ai_doc
        except Exception as e:
            self.runner.ai_doc_failure(ai_doc, message=str(e))
            return False, None, source_doc

    @abstractmethod
    def process_tdp_content(self, tdp: "TDPDocument") -> Tuple[bool, "TDPDocument"]:
        pass
```

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
        step_1 = YourAgent1(1, self.runner)
        success, step_1_content, step_1_doc = self.execute_step(step_1, None, tdp)
        if not success: return success, step_1_doc

        # Step 2: Second Agent
        step_2 = YourAgent2(2, self.runner)
        success, step_2_content, step_2_doc = self.execute_step(step_2, step_1_content, tdp)
        if not success: return success, step_2_doc

        return success, step_2_doc

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
Each step must follow this exact pattern:
```python
# Step N: Description
step_N = AgentName(N, self.runner)  # or with scenario_id: AgentName(N, self.scenario_id, self.runner)
success, step_N_content, step_N_doc = self.execute_step(step_N, input_content, tdp)
if not success: return success, step_N_doc
```

### Error Handling
- Each step automatically returns on failure with graceful fallback
- No manual try/catch blocks needed
- Built-in logging and AI document creation
- Agent name is automatically extracted from the agent class

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
step_1 = Agent1(1, self.runner)
success, step_1_content, step_1_doc = self.execute_step(step_1, None, tdp)
if not success: return success, step_1_doc

step_2 = Agent2(2, self.runner)
success, step_2_content, step_2_doc = self.execute_step(step_2, step_1_content, tdp)
if not success: return success, step_2_doc

step_3 = Agent3(3, self.runner)
success, step_3_content, step_3_doc = self.execute_step(step_3, step_2_content, tdp)
if not success: return success, step_3_doc

return success, step_3_doc
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
