from src.agents.excel.excel_to_json_agent import ExcelToJSONAgent
from src.agents.json_to_sysml_agent import JSONtoSysMLAgent
from src.agents.neo4j_agent import Neo4jAgent
from src.agents.elastic_search_agent import ElasticSearchAgent
from src.agents.qdrant_agent import QdrantAgent
from src.agents.transform_agent import TransformAgent
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from src.scenario_models import TDPDocument
    from src.agents.workflow_runner import WorkflowRunner


class ExcelToSysMLAgentGroup(TransformAgent):
    output_ext = "sysml"

    def __init__(self, step_num, scenario_id: str, runner: "WorkflowRunner"):
        self.scenario_id = scenario_id
        self.runner = runner
        super().__init__(step_num, runner)

    def process_tdp_content(self, tdp: "TDPDocument") -> Tuple[bool, "TDPDocument"]:
        print("Starting Excel to SysML Agent Group")
        
        # Step 1: Convert Excel to JSON
        step_1 = ExcelToJSONAgent(1, self.runner)
        success, step_1_content, step_1_doc = self.execute_step(step_1, None, tdp)
        if not success: return success, step_1_doc

        # Step 2: Convert JSON to SysML
        step_2 = JSONtoSysMLAgent(2, self.runner)
        success, step_2_content, step_2_doc = self.execute_step(step_2, step_1_content, tdp)
        if not success: return success, step_2_doc

        # Step 3: Store in ElasticSearch
        step_3 = ElasticSearchAgent(3, self.scenario_id, self.runner)
        success, step_3_content, step_3_doc = self.execute_step(step_3, step_2_content, tdp)
        if not success: return success, step_3_doc

        # Step 4: Store in Qdrant
        step_4 = QdrantAgent(4, self.scenario_id, self.runner)
        success, step_4_content, step_4_doc = self.execute_step(step_4, step_2_content, tdp)
        if not success: return success, step_4_doc

        # Step 5: Store in Neo4j
        step_5 = Neo4jAgent(5, self.scenario_id, self.runner)
        success, step_5_content, step_5_doc = self.execute_step(step_5, step_2_content, tdp)
        if not success: return success, step_5_doc

        return success, step_5_doc
