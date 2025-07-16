from src.agents.transform_agent import TransformAgent
from src.agents.london_agent import LondonAgent
from src.agents.rome_agent import RomeAgent
from src.agents.dublin_agent import DublinAgent
from src.agents.orlando_agent import OrlandoAgent
from src.agents.reno_agent import RenoAgent
from src.agents.workflow_runner import WorkflowRunner
from src.scenario_models import TDPDocument, AIDocument
from typing import Tuple


class CityAgentGroup(TransformAgent):
    output_ext = "json"

    def __init__(self, step_num, runner: WorkflowRunner):
        self.runner = runner
        super().__init__(step_num, runner)

    def process_tdp_content(self, tdp: TDPDocument) -> Tuple[bool, TDPDocument]:
        print("Starting City Agent Group")

        # Step 1: London Agent
        london_agent = LondonAgent(1, self.runner)
        success, london_content, london_doc = self.execute_step(london_agent, None, tdp)
        if not success:
            return success, london_doc

        # Step 2: Rome Agent
        rome_agent = RomeAgent(2, self.runner)
        success, rome_content, rome_doc = self.execute_step(rome_agent, london_content, london_doc)
        if not success:
            return success, rome_doc

        # Step 3: Dublin Agent
        dublin_agent = DublinAgent(3, self.runner)
        success, dublin_content, dublin_doc = self.execute_step(dublin_agent, rome_content, rome_doc)
        if not success:
            return success, dublin_doc

        # Step 4: Orlando Agent
        orlando_agent = OrlandoAgent(4, self.runner)
        success, orlando_content, orlando_doc = self.execute_step(orlando_agent, dublin_content, dublin_doc)
        if not success:
            return success, orlando_doc

        # Step 5: Reno Agent
        reno_agent = RenoAgent(5, self.runner)
        success, reno_content, reno_doc = self.execute_step(reno_agent, orlando_content, orlando_doc)
        if not success:
            return success, reno_doc

        return True, reno_doc
