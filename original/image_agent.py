from src.agents.transform_agent import TransformAgent
from src.agents.text_to_chunk_agent import TextChunkAgent
from src.agents.elastic_search_agent import ElasticSearchAgent
from src.agents.qdrant_agent import QdrantAgent
from src.agents.image_capture_agent import ImageDocumentAgent
from src.agents.workflow_runner import WorkflowRunner
from src.scenario_models import TDPDocument, AIDocument
from typing import Tuple


class ImageChunkAgentGroupV2(TransformAgent):
    output_ext = "json"

    def __init__(self, step_num, runner: WorkflowRunner):
        self.runner = runner
        super().__init__(step_num)

    def process_tdp_content(self, tdp: TDPDocument) -> Tuple[bool, TDPDocument]:
        scenario_id = self.runner.get_scenario().Id
        special_instructions = tdp.SpecialInstructions
        print("Starting Section Image Chunk Agent Group")

        step_one = ImageDocumentAgent(1)
        step_one.set_special_instructions(special_instructions)
        step_one_doc = AIDocument(
            FileName=self.runner.compute_ai_doc_filename(
                tdp.FileName, step_one.output_ext
            ),
            Description="",
            SourceFileName=tdp.FileName,
            SourceURL=tdp.URL,
        )
        try:
            step_one_content = step_one.process_tdp_content(
                tdp.get_content(scenario_id)
            )
            self.runner.ai_doc_success(step_one_doc, step_one_content)
        except Exception as e:
            self.runner.ai_doc_failure(step_one_doc, message=str(e))
            return False, tdp
        
        print("Starting chunk Agent", step_one_content)
        step_two = TextChunkAgent(2)
        step_two_doc = AIDocument(
            FileName=self.runner.compute_ai_doc_filename(
                step_one_doc.FileName, step_two.output_ext
            ),
            Description="",
            SourceFileName=step_one_doc.FileName,
            SourceURL=step_one_doc.URL,
        )
        try:
            step_two_content = step_two.process_tdp_content(step_one_content)
            self.runner.ai_doc_success(step_two_doc, step_two_content)
        except Exception as e:
            self.runner.ai_doc_failure(step_two_doc, message=str(e))
            return False, step_one_doc

        print("Starting Elasticsearch Agent", step_one_content)
        step_three = ElasticSearchAgent(3, scenario_id)
        step_three_doc = AIDocument(
            FileName=self.runner.compute_ai_doc_filename(
                step_two_doc.FileName, step_two.output_ext
            ),
            Description="",
            SourceFileName=step_two_doc.FileName,
            SourceURL=step_two_doc.URL,
        )
        try:
            step_three_content = step_three.process_tdp_content(step_two_content)
            self.runner.ai_doc_success(step_three_doc, step_three_content)
        except Exception as e:
            self.runner.ai_doc_failure(step_two_doc, message=str(e))
            return False, step_one_doc

        step_four = QdrantAgent(4, scenario_id)
        step_four_doc = AIDocument(
            FileName=self.runner.compute_ai_doc_filename(
                step_two_doc.FileName, step_two.output_ext
            ),
            Description="",
            SourceFileName=step_two_doc.FileName,
            SourceURL=step_two_doc.URL,
        )
        try:
            step_four_content = step_four.process_tdp_content(step_two_content)
            self.runner.ai_doc_success(step_four_doc, step_four_content)
        except Exception as e:
            self.runner.ai_doc_failure(step_four_doc, message=str(e))
            return False, step_one_doc

        return True, step_four_content