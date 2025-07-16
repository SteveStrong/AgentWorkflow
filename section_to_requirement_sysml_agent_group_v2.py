from src.agents.transform_agent import TransformAgent
from src.agents.section_chunk_agent import SectionChunkAgent
from src.agents.sections_to_requirements_agent import SectionToRequirementsAgent
from src.agents.elastic_search_agent import ElasticSearchAgent
from src.agents.qdrant_agent import QdrantAgent
from src.agents.workflow_runner import WorkflowRunner
from src.scenario_models import TDPDocument, AIDocument
from typing import Tuple

class SectionToRequirementSysmlAgentGroupV2(TransformAgent):
    output_ext = "json"

    def __init__(self, step_num, runner: WorkflowRunner):
        self.runner = runner
        super().__init__(step_num, runner)

    def process_tdp_content(self, tdp: TDPDocument) -> Tuple[bool, TDPDocument]:
        scenario_id = self.runner.get_scenario().Id
        print("Starting Section to Requirement SysML Agent Group V2")
        
        # Step 1: Chunk sections
        step_1 = SectionChunkAgent(1, self.runner)
        success, step_1_content, step_1_doc = self.execute_step(step_1, None, tdp)
        if not success: return success, step_1_doc

        # Step 2: Convert sections to requirements
        step_2 = SectionToRequirementsAgent(2, self.runner)
        success, step_2_content, step_2_doc = self.execute_step(step_2, step_1_content, step_1_doc)
        if not success: return success, step_2_doc
        
        # Step 3: Store requirements in ElasticSearch
        step_3 = ElasticSearchAgent(3, scenario_id, self.runner)
        success, step_3_content, step_3_doc = self.execute_step(step_3, step_2_content, step_2_doc)
        if not success: return success, step_3_doc

        # Step 4: Store requirements in Qdrant
        step_4 = QdrantAgent(4, scenario_id, self.runner)
        success, step_4_content, step_4_doc = self.execute_step(step_4, step_2_content, step_2_doc)
        if not success: return success, step_4_doc

        # Step 5: Store sections in ElasticSearch
        step_5 = ElasticSearchAgent(5, scenario_id, self.runner)
        success, step_5_content, step_5_doc = self.execute_step(step_5, step_1_content, step_4_doc)
        if not success: return success, step_5_doc

        # Step 6: Store sections in Qdrant
        step_6 = QdrantAgent(6, scenario_id, self.runner)
        success, step_6_content, step_6_doc = self.execute_step(step_6, step_1_content, step_5_doc)
        if not success: return success, step_6_doc

        return success, step_6_doc
