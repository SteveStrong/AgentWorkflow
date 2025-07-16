from src.agents.transform_agent import TransformAgent
from src.agents.pdf_agents.page_chunk_agent import PageChunkAgent
from src.agents.llm.table_of_contents_extraction_agent import TableOfContentsExtractionAgent
from src.agents.pdf_agents.section_chunk_with_table_of_contents_agent import SectionChunkWithTableOfContentsAgent
from src.agents.elastic_search_agent import ElasticSearchAgent
from src.agents.qdrant_agent import QdrantAgent
from src.agents.workflow_runner import WorkflowRunner
from src.scenario_models import TDPDocument, AIDocument
from typing import Tuple
import json


class SectionChunkAgentGroupV3(TransformAgent):
    output_ext = "json"

    def __init__(self, step_num, runner: WorkflowRunner):
        self.runner = runner
        super().__init__(step_num, runner)

    def process_tdp_content(self, tdp: TDPDocument) -> Tuple[bool, TDPDocument]:
        scenario_id = self.runner.get_scenario().Id

        print("Starting Section Chunk Agent Group")
        step_1 = PageChunkAgent(1, self.runner, pages_per_chunk=10, number_of_chunks=1)
        success, step_1_content, step_1_doc = self.execute_step(step_1, None, tdp)
        if not success:
            return success, step_1_doc

        step_2 = TableOfContentsExtractionAgent(2, self.runner)
        success, step_2_content, step_2_doc = self.execute_step(step_2, step_1_content, step_1_doc)
        if not success:
            return success, step_2_doc

        # TODO: Abstract this logic into a separate method or class
        # Start of Logic for getting from step 2 to step 3
        step_2_content_json = json.loads(step_2_content.decode('utf-8'))
        list_of_toc = step_2_content_json.get("toc", [])

        headers = [entry.get("title") for entry in list_of_toc]
        first_page = list_of_toc[0].get("page", 0) if list_of_toc else 0
        first_page = int(first_page)  # Ensure first_page is an integer
        # End of Logic for getting from step 2 to step 3

        step_3 = SectionChunkWithTableOfContentsAgent(3, self.runner, table_of_contents=headers, first_page=first_page)
        success, step_3_content, step_3_doc = self.execute_step(step_3, None, tdp)
        if not success:
            return success, step_3_doc

        step_4 = ElasticSearchAgent(4, scenario_id, self.runner)
        success, step_4_content, step_4_doc = self.execute_step(step_4, step_3_content, step_3_doc)
        if not success:
            return success, step_4_doc

        step_5 = QdrantAgent(5, scenario_id, self.runner)
        success, step_5_content, step_5_doc = self.execute_step(step_5, step_3_content, step_3_doc)
        if not success:
            return success, step_5_doc

        return True, step_5_doc

