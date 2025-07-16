# Template-Based Agent Group Creation

## Overview

This approach uses a structured template format where you provide all requirements upfront. Perfect when you have detailed specifications, clear requirements, or want to work from existing documentation.

## How to Use

Fill out the template below with your requirements and provide it all at once. The AI will generate a complete, framework-compliant agent group.

## Template Format

```markdown
**Agent Group Name**: YourAgentGroupName

**Output Extension**: "extension"

**Agents**:
1. AgentClassName - Description of what it does
2. AgentClassName - Description of what it does
3. AgentClassName - Description of what it does
[... continue for all agents]

**Special Parameters**: (if any)
- Agent2 requires scenario_id
- Agent3 requires config_path

**Custom Logic**: (if any)
- Steps 4 and 5 both use output from step 3
- Agent2 needs special instructions set
- Linear pipeline / Custom routing details
```

## Complete Examples

### Example 1: E-commerce Order Processing
```markdown
**Agent Group Name**: EcommerceOrderProcessingAgentGroup

**Output Extension**: "json"

**Agents**:
1. OrderValidationAgent - Validate order data and customer information
2. InventoryCheckAgent - Verify product availability and reserve stock
3. PaymentProcessingAgent - Process payment and handle transactions
4. ShippingCalculationAgent - Calculate shipping costs and delivery times
5. OrderConfirmationAgent - Generate order confirmation and notifications
6. InventoryUpdateAgent - Update inventory levels after order processing

**Special Parameters**:
- PaymentProcessingAgent requires payment_gateway_config
- ShippingCalculationAgent requires carrier_api_keys

**Custom Logic**:
- Steps 5 and 6 both use output from step 4 (shipping info used for confirmation and inventory update)
```

### Example 2: Scientific Data Analysis Pipeline
```markdown
**Agent Group Name**: ScientificDataAnalysisAgentGroup

**Output Extension**: "json"

**Agents**:
1. DataIngestionAgent - Load and parse scientific datasets
2. DataCleaningAgent - Clean, normalize, and validate data
3. StatisticalAnalysisAgent - Perform statistical analysis and calculations
4. VisualizationAgent - Generate charts, graphs, and visualizations
5. ReportGenerationAgent - Create comprehensive analysis report
6. PeerReviewValidationAgent - Validate results against peer review standards

**Special Parameters**:
- StatisticalAnalysisAgent requires analysis_parameters
- PeerReviewValidationAgent requires validation_criteria

**Custom Logic**:
- Linear pipeline (each step uses previous step's output)
```

### Example 3: Multi-Language Document Translation
```markdown
**Agent Group Name**: MultiLanguageTranslationAgentGroup

**Output Extension**: "json"

**Agents**:
1. LanguageDetectionAgent - Detect source language of input document
2. TextExtractionAgent - Extract and structure text content
3. TranslationAgent - Translate text to target language
4. QualityAssuranceAgent - Validate translation quality and accuracy
5. FormattingAgent - Apply proper formatting to translated content
6. LocalizationAgent - Adapt content for cultural and regional context

**Special Parameters**:
- TranslationAgent requires target_language
- LocalizationAgent requires locale_settings

**Custom Logic**:
- Steps 4, 5, and 6 all use output from step 3 (translation output goes to QA, formatting, and localization)
```

### Example 4: Cybersecurity Threat Analysis
```markdown
**Agent Group Name**: CybersecurityThreatAnalysisAgentGroup

**Output Extension**: "json"

**Agents**:
1. LogIngestionAgent - Collect and parse security logs
2. ThreatDetectionAgent - Identify potential security threats
3. VulnerabilityAssessmentAgent - Assess system vulnerabilities
4. RiskAnalysisAgent - Calculate risk scores and impact assessment
5. IncidentResponseAgent - Generate incident response recommendations
6. ComplianceReportAgent - Generate compliance and audit reports

**Special Parameters**:
- ThreatDetectionAgent requires threat_intelligence_feeds
- ComplianceReportAgent requires compliance_frameworks
- RiskAnalysisAgent requires risk_matrix_config

**Custom Logic**:
- Steps 4, 5, and 6 all use output from step 3 (vulnerability data feeds into risk analysis, incident response, and compliance reporting)
```

## Generated Output Structure

When you provide a template, you'll receive:

### 1. Complete Python File
```python
from src.agents.transform_agent import TransformAgent
from src.agents.workflow_runner import WorkflowRunner
from src.scenario_models import TDPDocument
from typing import Tuple, TYPE_CHECKING

# All necessary imports for your specific agents
from src.agents.your_agent_1 import YourAgent1
from src.agents.your_agent_2 import YourAgent2
# ... all agent imports

if TYPE_CHECKING:
    from src.scenario_models import TDPDocument
    from src.agents.workflow_runner import WorkflowRunner


class YourAgentGroup(TransformAgent):
    output_ext = "your_extension"

    def __init__(self, step_num, runner: "WorkflowRunner", param1: str = None, param2: str = None):
        # Store special parameters
        self.param1 = param1
        self.param2 = param2
        self.runner = runner
        super().__init__(step_num, runner)

    def process_tdp_content(self, tdp: "TDPDocument") -> Tuple[bool, "TDPDocument"]:
        print("Starting Your Agent Group")
        
        # Complete implementation with all steps
        # Custom logic properly implemented
        # Error handling for each step
        # Proper content routing
        
        return success, final_doc
```

### 2. Implementation Notes
- Explanation of any custom logic implemented
- Notes about special parameter usage
- Content flow documentation
- Error handling strategy

### 3. Usage Example
```python
# How to instantiate and use your new agent group
agent_group = YourAgentGroup(
    step_num=1, 
    runner=workflow_runner,
    param1="value1",
    param2="value2"
)

success, result_doc = agent_group.process_tdp_content(input_document)
```

## Benefits of Template Approach

### ⚡ **Speed and Efficiency**
- Single request generates complete solution
- No back-and-forth conversation needed
- Perfect for batch creation of multiple agent groups

### 📋 **Comprehensive Specification**
- Forces you to think through all requirements upfront
- Ensures nothing is missed in the implementation
- Creates documentation of the intended design

### 🎯 **Precision and Control**
- Exact control over agent names and descriptions
- Precise specification of parameters and routing
- No ambiguity in requirements

### 📚 **Reproducible and Documentable**
- Template serves as specification document
- Easy to version control and modify
- Can be shared with team members for review

## When to Use Template Approach

✅ **Perfect for:**
- Well-defined requirements and specifications
- Working from existing documentation
- Creating multiple similar agent groups
- Time-sensitive implementations
- Team environments where specifications need approval

❌ **Not ideal for:**
- Exploratory or experimental pipelines
- When learning the framework capabilities
- Unclear or evolving requirements
- First-time users who need guidance

## Quick Start Templates

### Basic 3-Step Pipeline
```markdown
**Agent Group Name**: Basic3StepAgentGroup
**Output Extension**: "json"
**Agents**:
1. InputProcessorAgent - Process input data
2. TransformationAgent - Transform processed data
3. OutputFormatterAgent - Format final output
**Special Parameters**: None
**Custom Logic**: Linear pipeline
```

### Database Processing Pipeline
```markdown
**Agent Group Name**: DatabaseProcessingAgentGroup
**Output Extension**: "json"
**Agents**:
1. DatabaseConnectorAgent - Connect to database and extract data
2. DataValidationAgent - Validate data integrity and format
3. DataTransformationAgent - Transform data according to business rules
4. DataAggregationAgent - Aggregate and summarize data
5. ReportGenerationAgent - Generate final reports
**Special Parameters**: 
- DatabaseConnectorAgent requires connection_string
**Custom Logic**: Linear pipeline
```

## Getting Started

1. **Copy the template format**
2. **Fill in your specific requirements**
3. **Provide the completed template in a single message**
4. **Receive complete, ready-to-use agent group**

The AI will generate everything you need based on your specifications!
