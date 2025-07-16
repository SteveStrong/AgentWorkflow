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
        super().__init__(step_num, runner)

    def process_tdp_content(self, tdp: TDPDocument) -> Tuple[bool, TDPDocument]:
        scenario_id = self.runner.get_scenario().Id
        special_instructions = tdp.SpecialInstructions
        print("Starting Section Image Chunk Agent Group")

        step_one = ImageDocumentAgent(1, self.runner)
        step_one.set_special_instructions(special_instructions)
        success, step_one_content, step_one_doc = self.execute_step(step_one, None, tdp, "ImageDocumentAgent")
        if not success:
            return success, step_one_doc
        
        print("Starting chunk Agent", step_one_content)
        step_two = TextChunkAgent(2, self.runner)
        success, step_two_content, step_two_doc = self.execute_step(step_two, step_one_content, step_one_doc, "TextChunkAgent")
        if not success:
            return success, step_two_doc

        print("Starting Elasticsearch Agent", step_one_content)
        step_three = ElasticSearchAgent(3, scenario_id, self.runner)
        success, step_three_content, step_three_doc = self.execute_step(step_three, step_two_content, step_two_doc, "ElasticSearchAgent")
        if not success:
            return success, step_three_doc

        step_four = QdrantAgent(4, scenario_id, self.runner)
        success, step_four_content, step_four_doc = self.execute_step(step_four, step_two_content, step_two_doc, "QdrantAgent")
        if not success:
            return success, step_four_doc

        return True, step_four_content