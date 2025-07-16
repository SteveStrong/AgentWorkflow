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
        step_name: str = None,
    ) -> Tuple[bool, bytes, "AIDocument"]:
        """
        Execute a complete pipeline step with standardized error handling.
        
        Args:
            agent: The agent to execute
            input_content: The content to process (or None to get from source_doc)
            source_doc: Document to create AI doc from (and get content from if input_content is None)
            step_name: Optional name for logging
        
        Returns:
            Tuple[bool, content, ai_doc] - (success, output_content, ai_document)
        """
        # Create AI document
        ai_doc = agent.create_ai_document(source_doc)
        
        # Optional start logging
        if step_name:
            print(f"Starting {step_name}")
        
        try:
            # Get content if not provided (for first step)
            if input_content is None:
                scenario_id = self.runner.get_scenario().Id
                input_content = source_doc.get_content(scenario_id)
                
            # Execute the step
            step_content = agent.process_tdp_content(input_content)
            self.runner.ai_doc_success(ai_doc, step_content)
            
            # Optional completion logging
            if step_name:
                print(f"Finished {step_name}")
                
            return True, step_content, ai_doc
        except Exception as e:
            self.runner.ai_doc_failure(ai_doc, message=str(e))
            return False, None, source_doc

    @abstractmethod
    def process_tdp_content(self, content: bytes) -> bytes:
        pass
