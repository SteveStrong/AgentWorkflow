# Interactive Agent Group Creation

## Overview

This approach uses an interactive conversation to gather requirements and create agent groups step-by-step. Perfect when you're not sure about all the details upfront or want guidance through the process.

## How to Use

Simply say: **"Create an agent group"** or **"I need a new agent group for [general purpose]"**

The AI will then guide you through the process with targeted questions.

## Interactive Process Flow

### Step 1: Initial Request
```
User: "Create an agent group for processing financial documents"
```

### Step 2: AI Gathers Requirements
```
AI: "I'll help you create a financial document processing agent group. 
Let me gather the required information:

1. **Agent Group Name**: What should the class be called? 
   (e.g., FinancialDocumentAgentGroup)

2. **Output Extension**: What file extension for the final output? 
   (json, xml, txt, csv, etc.)

3. **Agent List**: What agents should be in the pipeline and in what order?
   Please describe the processing steps you need.

4. **Special Parameters**: Do any agents need extra parameters like scenario_id?

5. **Custom Logic**: Any special routing or content flow requirements?

Please provide these details and I'll generate the complete agent group."
```

### Step 3: User Provides Information
```
User: "The class should be called FinancialDocumentAgentGroup. 
Output should be JSON. I need to:
1. Parse PDF financial statements
2. Extract key financial metrics
3. Validate the data
4. Generate summary report
5. Store in database

The validation agent needs a scenario_id parameter."
```

### Step 4: AI Clarifies Details
```
AI: "Great! Let me clarify a few details:

1. For the agents, would these names work?
   - PDFFinancialParserAgent
   - FinancialMetricsExtractionAgent  
   - FinancialDataValidationAgent
   - FinancialSummaryReportAgent
   - FinancialDatabaseStorageAgent

2. You mentioned scenario_id for validation - any other agents need special parameters?

3. Is this a linear pipeline (each step uses the previous step's output) 
   or do you need custom routing?"
```

### Step 5: AI Generates Complete Solution
```
AI: "Perfect! I'll create the FinancialDocumentAgentGroup with your specifications."
```

## Example Interactive Sessions

### Session 1: Simple Linear Pipeline
```
User: "Create an agent group"

AI: "I'll help you create a new agent group. What type of processing pipeline do you need?"

User: "Something to process medical images"

AI: "Great! Medical image processing. Let me gather the details:

1. **Agent Group Name**: How about MedicalImageAgentGroup?
2. **Output Extension**: What format should the final output be? (json, xml, dicom, etc.)
3. **Processing Steps**: What should happen to the medical images? 
   (e.g., enhance → analyze → diagnose → report)"

User: "MedicalImageAgentGroup sounds good. Output should be JSON. 
I need: enhance image quality, detect anomalies, classify findings, generate report"

AI: "Perfect! So the pipeline would be:
1. ImageEnhancementAgent - Improve image quality
2. AnomalyDetectionAgent - Detect potential issues  
3. FindingsClassificationAgent - Classify detected findings
4. MedicalReportGenerationAgent - Generate final report

Any special parameters needed? Linear flow (each step uses previous output)?"

User: "Yes, linear flow. No special parameters."

AI: "Creating MedicalImageAgentGroup now..."
```

### Session 2: Complex Routing Pipeline
```
User: "I need an agent group for document analysis"

AI: "What type of documents and what kind of analysis?"

User: "Legal contracts. Need to extract clauses, analyze risks, check compliance"

AI: "Interesting! Legal contract analysis. Let me map this out:

1. **Agent Group Name**: LegalContractAnalysisAgentGroup?
2. **Output Extension**: JSON for structured data?
3. **Pipeline**: 
   - Parse contract text
   - Extract clauses  
   - Analyze risks
   - Check compliance
   - Generate report

Do both risk analysis and compliance checking use the extracted clauses?"

User: "Yes, both risk and compliance agents should use the clause extraction output"

AI: "Got it! So custom routing where steps 3 and 4 both use step 2's output. 
Any special parameters needed?"

User: "Compliance agent needs a regulatory_framework parameter"

AI: "Perfect! Creating LegalContractAnalysisAgentGroup with:
- Linear flow through clause extraction
- Parallel processing for risk/compliance analysis
- Special parameter for regulatory framework
..."
```

## Benefits of Interactive Approach

### 🎯 **Guided Discovery**
- AI helps you think through the requirements
- Suggests appropriate agent names and flow patterns
- Identifies potential issues before implementation

### 🔍 **Clarification and Validation**
- AI asks follow-up questions to ensure accuracy
- Validates assumptions about data flow
- Confirms special requirements are captured

### 📚 **Educational Value**
- Learn about framework capabilities during the conversation
- Understand best practices through AI recommendations
- Get explanations of why certain patterns are suggested

### 🛠️ **Flexible and Iterative**
- Can adjust requirements during the conversation
- Easy to modify specifications based on AI suggestions
- Natural back-and-forth until requirements are perfect

## When to Use Interactive Approach

✅ **Perfect for:**
- Exploring new processing pipelines
- Learning the framework capabilities
- When requirements are not fully defined
- Complex workflows that need validation
- First-time users of the framework

❌ **Not ideal for:**
- When you have complete, detailed specifications
- Batch creation of multiple similar agent groups
- When working from existing documentation
- Time-sensitive implementations with known requirements

## Getting Started

Just say one of these phrases:

- **"Create an agent group"**
- **"I need a new agent group for [purpose]"**
- **"Help me build a pipeline for [use case]"**
- **"Generate an agent group"**
- **"I want to process [type] documents"**

The AI will take care of the rest, guiding you through each step to create a perfect, framework-compliant agent group!
