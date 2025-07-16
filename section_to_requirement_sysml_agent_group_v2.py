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
        print("Starting Section Chunk Agent Group")
        step_one = SectionChunkAgent(1, self.runner)
        step_one_doc = step_one.create_ai_document(tdp)
        try:
            step_one_content = step_one.process_tdp_content(
                tdp.get_content(scenario_id)
            )
            self.runner.ai_doc_success(step_one_doc, step_one_content)
        except Exception as e:
            raise 
            self.runner.ai_doc_failure(step_one_doc, message=str(e))
            return False, tdp

        print("Starting Section to Requirements Agent", step_one_content)
        step_two = SectionToRequirementsAgent(2, self.runner)
        step_two_doc = step_two.create_ai_document(step_one_doc)
        try:
            step_two_content = step_two.process_tdp_content(step_one_content)
            self.runner.ai_doc_success(step_two_doc, step_two_content)
        except Exception as e:
            self.runner.ai_doc_failure(step_two_doc, message=str(e))
            return False, step_one_doc
        
        step_three = ElasticSearchAgent(3, scenario_id, self.runner)
        step_three_doc = step_three.create_ai_document(step_two_doc)
        try:
            step_three_content = step_three.process_tdp_content(step_two_content)
            self.runner.ai_doc_success(step_three_doc, step_three_content)
        except Exception as e:
            self.runner.ai_doc_failure(step_two_doc, message=str(e))
            return False, step_one_doc

        step_four = QdrantAgent(4, scenario_id, self.runner)
        step_four_doc = step_four.create_ai_document(step_three_doc)
        try:
            step_four_content = step_four.process_tdp_content(step_two_content)
            self.runner.ai_doc_success(step_four_doc, step_four_content)
        except Exception as e:
            self.runner.ai_doc_failure(step_four_doc, message=str(e))
            return False, step_one_doc

        step_five = ElasticSearchAgent(5, scenario_id, self.runner)
        step_five_doc = step_five.create_ai_document(step_four_doc)
        try:
            step_five_content = step_five.process_tdp_content(step_one_content)
            self.runner.ai_doc_success(step_five_doc, step_five_content)
        except Exception as e:
            self.runner.ai_doc_failure(step_five_doc, message=str(e))
            return False, step_one_doc

        step_six = QdrantAgent(6, scenario_id, self.runner)
        step_six_doc = step_six.create_ai_document(step_five_doc)
        try:
            step_six_content = step_six.process_tdp_content(step_one_content)
            self.runner.ai_doc_success(step_six_doc, step_six_content)
        except Exception as e:
            self.runner.ai_doc_failure(step_six_doc, message=str(e))
            return False, step_one_doc

        return True, step_six_content
