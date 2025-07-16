from src.agents.visio.visio_agent import VisioAgent
from src.agents.visio_json_to_sysml_agent import VisioJSONtoSysMLAgent
from src.agents.sysml_chunk_agent import SysMLChunkAgent
from src.agents.elastic_search_agent import ElasticSearchAgent
from src.agents.qdrant_agent import QdrantAgent
from src.agents.transform_agent import TransformAgent
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from src.scenario_models import TDPDocument
    from src.agents.workflow_runner import WorkflowRunner


class VisioAgentGroup(TransformAgent):
    output_ext = "json"

    def __init__(self, step_num, scenario_id: str, runner: "WorkflowRunner"):
        self.scenario_id = scenario_id
        self.runner = runner
        super().__init__(step_num, runner)

    def process_tdp_content(self, tdp: "TDPDocument") -> Tuple[bool, "TDPDocument"]:
        print("Starting Visio Agent Group")
        
        # Step 1: Extract Visio diagram content
        success, step_one_content, step_one_doc = self.execute_step(VisioAgent(1, self.runner), None, tdp, "VisioAgent")
        if not success: return success, step_one_doc

        # Step 2: Convert Visio JSON to SysML
        success, step_two_content, step_two_doc = self.execute_step(VisioJSONtoSysMLAgent(2, self.runner), step_one_content, tdp, "VisioJSONtoSysMLAgent")
        if not success: return success, step_two_doc

        # Step 3: Chunk SysML content
        success, step_three_content, step_three_doc = self.execute_step(SysMLChunkAgent(3, self.runner), step_two_content, tdp, "SysMLChunkAgent")
        if not success: return success, step_three_doc

        # Step 4: Store in ElasticSearch
        success, step_four_content, step_four_doc = self.execute_step(ElasticSearchAgent(4, self.scenario_id, self.runner), step_three_content, tdp, "ElasticSearchAgent")
        if not success: return success, step_four_doc

        # Step 5: Store in Qdrant (using step_three_content like original)
        success, step_five_content, step_five_doc = self.execute_step(QdrantAgent(5, self.scenario_id, self.runner), step_three_content, tdp, "QdrantAgent")
        if not success: return success, step_five_doc

        return success, step_five_doc
