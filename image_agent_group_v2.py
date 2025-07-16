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
        print("Starting Image Chunk Agent Group V2")

        # Step 1: Process image document
        step_1 = ImageDocumentAgent(1, self.runner)
        step_1.set_special_instructions(special_instructions)
        success, step_1_content, step_1_doc = self.execute_step(step_1, None, tdp)
        if not success: return success, step_1_doc
        
        # Step 2: Chunk text content
        step_2 = TextChunkAgent(2, self.runner)
        success, step_2_content, step_2_doc = self.execute_step(step_2, step_1_content, step_1_doc)
        if not success: return success, step_2_doc

        # Step 3: Store in ElasticSearch
        step_3 = ElasticSearchAgent(3, scenario_id, self.runner)
        success, step_3_content, step_3_doc = self.execute_step(step_3, step_2_content, step_2_doc)
        if not success: return success, step_3_doc

        # Step 4: Store in Qdrant
        step_4 = QdrantAgent(4, scenario_id, self.runner)
        success, step_4_content, step_4_doc = self.execute_step(step_4, step_2_content, step_2_doc)
        if not success: return success, step_4_doc

        return success, step_4_doc