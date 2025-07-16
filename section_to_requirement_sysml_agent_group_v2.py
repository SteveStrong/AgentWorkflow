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
        print("Starting Section Chunk Agent Group")
        
        step_one = SectionChunkAgent(1, self.runner)
        success, step_one_content, step_one_doc = self.execute_step(step_one, None, tdp)
        if not success:
            return success, step_one_doc

        step_two = SectionToRequirementsAgent(2, self.runner)
        success, step_two_content, step_two_doc = self.execute_step(step_two, step_one_content, step_one_doc)
        if not success:
            return success, step_two_doc
        
        step_three = ElasticSearchAgent(3, self.runner.get_scenario().Id, self.runner)
        success, step_three_content, step_three_doc = self.execute_step(step_three, step_two_content, step_two_doc)
        if not success:
            return success, step_three_doc

        step_four = QdrantAgent(4, self.runner.get_scenario().Id, self.runner)
        success, step_four_content, step_four_doc = self.execute_step(step_four, step_two_content, step_two_doc)
        if not success:
            return success, step_four_doc

        step_five = ElasticSearchAgent(5, self.runner.get_scenario().Id, self.runner)
        success, step_five_content, step_five_doc = self.execute_step(step_five, step_one_content, step_four_doc)
        if not success:
            return success, step_five_doc

        step_six = QdrantAgent(6, self.runner.get_scenario().Id, self.runner)
        success, step_six_content, step_six_doc = self.execute_step(step_six, step_one_content, step_five_doc)
        if not success:
            return success, step_six_doc

        return True, step_six_content
