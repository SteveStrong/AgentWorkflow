
class TDPDocument(BaseModel):
    """
    Represent metadata for a Technical Data Package (TDP) document.

    Inputs:
        FileName (str): The name of the TDP file
        Description (str): A description of the TDP contents
        URL (str): The storage location of the TDP file
    """

    FileName: str
    Description: str
    URL: str = ""
    Metadata: str = ""

    Status: TDPStatus = TDPStatus.UNKNOWN
    LoadInContext: bool = False
    LoadingMethod: TDPLoadingMethod = TDPLoadingMethod.UNDECIDED
    FileSizeKB: float = -1
    ConsumingAIDocuments: List[str] = []
    SpecialInstructions: str = ""
    InitialAssessment: str = ""
    FinalAssessment: str = ""
    Error: str = ""

    @property
    def ext(self):
        return self.FileName.split(".")[-1]

    def assess(self, scenario_id: str) -> "TDPDocument":
        """
        Set the file size, load into context, and initial assessment
        """
        from src.storage_service import storage_service

        try:
            tdp_file = storage_service.read_tdp(scenario_id, self.FileName)
        except Exception:
            try:
                tdp_file = storage_service.read_ai_doc(scenario_id, self.FileName)
            except Exception:
                return self

        self.FileSizeKB = len(tdp_file) / 1024

        from src.service_layer import model_service

        model_service.set_tdp_consumabitlity(self)

        return self

    def set_status_transformed(
        self, scenario_id: str, outgoing_doc_name: Optional[str] = None
    ) -> "TDPDocument":
        from src.storage_service import storage_service

        self.Status = TDPStatus.TRANSFORMED
        self.LoadInContext = False
        self.LoadingMethod = TDPLoadingMethod.OBSOLETE
        if outgoing_doc_name:
            self.ConsumingAIDocuments.append(outgoing_doc_name)

        if isinstance(self, AIDocument):
            storage_service.write_ai_doc(scenario_id, self)
        else:
            storage_service.write_tdp(scenario_id, self)

        return self

    def mock_consuming_ai_document(
        self, scenario_id: str, agent_name: str
    ) -> "AIDocument":
        from src.agents.agent_factory import TransformAgentFactory
        from src.storage_service import storage_service

        agent_factory = TransformAgentFactory()

        ai_doc = AIDocument(
            FileName=agent_factory.compute_filename(agent_name, self.FileName),
            Description=f"Mocked output document.",
        )
        ai_doc.set_status_mocked(scenario_id, self, agent_name)

        return ai_doc

    def write(
        self, scenario: "AIScenario", content: Optional[bytes] = None
    ) -> "TDPDocument":
        from src.storage_service import storage_service

        storage_service.write_tdp(scenario.Id, self, content)

        return self

    def is_ready(self) -> bool:
        if self.Status in [
            TDPStatus.TRANSFORMED,
            TDPStatus.IN_CONTEXT,
            TDPStatus.IN_KNOWLEDGEBASE,
            TDPStatus.REQUIRES_TRANSFORMATION,
            TDPStatus.PROCESSED,
        ]:
            return True

        return False

    def get_content(self, scenario_id) -> bytes:
        from src.storage_service import storage_service

        tdp_content = storage_service.read_tdp(scenario_id, self.FileName)

        return tdp_content


class AIDocument(TDPDocument):
    """
    Represent metadata for an AI-processed document.

    Inputs:
        FileName (str): The name of the AI document
        Description (str): A description of the document contents
        URL (str): The storage location of the document
        SourceURL (str): The URL of the source TDP
        Status (str): The processing status of the document
        ProcessedTime (datetime): When the document was processed
        AgentName (str): The name of the agent that processed the document
        Error (Optional[str]): Any error that occurred during processing

    Custom Objects Used:
        TDPDocument: Base class for document metadata
    """

    SourceURL: str = ""
    SourceFileName: str = ""
    ProcessedTime: datetime = datetime.utcnow()
    AgentName: str = ""
    URL: str = ""

    def set_status_error(self, scenario_id: str, msg: str) -> "AIDocument":
        from src.storage_service import storage_service

        self.Status = TDPStatus.ERROR
        self.Error = msg
        storage_service.write_ai_doc(scenario_id, self)

        return self

    def set_status_processed(
        self, scenario_id: str, content: bytes = None
    ) -> "AIDocument":
        from src.storage_service import storage_service

        self.Status = TDPStatus.PROCESSED
        self.Error = ""
        print(f"url: {self.URL}")
        storage_service.write_ai_doc(scenario_id, self, content)

        source_doc_ref = storage_service.get_tdp_ref(scenario_id, self.SourceFileName)
        source_doc_ref.set_status_transformed(
            scenario_id, outgoing_doc_name=self.FileName
        )

        return self

    def set_status_mocked(
        self, scenario_id: str, source_doc: TDPDocument, agent_name: str
    ) -> "AIDocument":
        from src.storage_service import storage_service

        self.Status = TDPStatus.MOCKED
        self.SourceURL = source_doc.URL
        self.SourceFileName = source_doc.FileName
        self.AgentName = agent_name

        storage_service.write_ai_doc(scenario_id, self)

        return self

    def set_status_queued(self, scenario_id: str) -> "AIDocument":
        from src.storage_service import storage_service

        self.Status = TDPStatus.QUEUED
        storage_service.write_ai_doc(scenario_id, self)

        return self

    def set_status_processing(self, scenario_id: str) -> "AIDocument":
        from src.storage_service import storage_service

        self.Status = TDPStatus.PROCESSING
        self.Error = ""
        storage_service.write_ai_doc(scenario_id, self)

        return self

    def get_source_doc_ref(self, scenario: "AIScenario") -> TDPDocument:
        source_doc_ref = scenario.get_tdp_ref(self.SourceFileName)

        return source_doc_ref

    def get_source_doc_content(self, scenario: "AIScenario"):
        content = scenario.get_tdp_content(self.SourceFileName)

        return content

    def write(self, scenario, content=None) -> "AIDocument":
        from src.storage_service import storage_service

        storage_service.write_ai_doc(scenario.Id, self, content)

        return self

    def process_from_source_doc(self, scenario_id: str) -> Tuple[bool, "AIDocument"]:
        from src.agents import agent_index

        agent = agent_index.get_agent(self.AgentName)
        success = agent.process_ai_document(scenario_id, self)

        return success, self