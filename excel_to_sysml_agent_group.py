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


    output_ext = "sysml"

    def __init__(self, step_num, scenario_id: str, runner: "WorkflowRunner"):
        self.scenario_id = scenario_id
        self.runner = runner
        super().__init__(step_num, runner)

    def process_tdp_content(self, tdp: "TDPDocument") -> Tuple[bool, "TDPDocument"]:
        print("Starting Excel to SysML Agent Group")
        
        # Step 1: Convert Excel to JSON
        success, step_one_content, step_one_doc = self.execute_step(ExcelToJSONAgent(1, self.runner), None, tdp, "ExcelToJSONAgent")
        if not success: return success, step_one_doc

        # Step 2: Convert JSON to SysML
        success, step_two_content, step_two_doc = self.execute_step(JSONtoSysMLAgent(2, self.runner), step_one_content, tdp, "JSONtoSysMLAgent")
        if not success: return success, step_two_doc

        # Step 3: Store in ElasticSearch
        success, step_three_content, step_three_doc = self.execute_step(ElasticSearchAgent(3, self.scenario_id, self.runner), step_two_content, tdp, "ElasticSearchAgent")
        if not success: return success, step_three_doc

        # Step 4: Store in Qdrant
        success, step_four_content, step_four_doc = self.execute_step(QdrantAgent(4, self.scenario_id, self.runner), step_two_content, tdp, "QdrantAgent")
        if not success: return success, step_four_doc

        # Step 5: Store in Neo4j
        success, step_five_content, step_five_doc = self.execute_step(Neo4jAgent(5, self.scenario_id, self.runner), step_two_content, tdp, "Neo4jAgent")
        if not success: return success, step_five_doc

        return success, step_five_doc
