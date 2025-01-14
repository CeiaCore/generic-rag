from src.core.components.input.interface.InputInterface import InputInterface
from src.core.components.memory.interface.memory_interface import MemoryInterface
from src.core.components.orchestrator.interface.orchestrator_inteface import OrchestratorInterface
from src.core.components.retrieval.interface.retrieval_inteface import RetrievalInterface
from src.core.patterns.interface.pattern_interface import PatternInterface


class InputSelfRagDto:
    def __init__(self):
        pass

class outputSelfRagDto:
    def __init__(self):
        pass


class SelfRag(PatternInterface):

    def __init__(self, input_module: InputInterface, orchestrator_module: OrchestratorInterface):
        self.input_module = input_module
        self.orchestrator_module = orchestrator_module

    def execute(self, input: InputSelfRagDto):
        input = self.input_module.input(input)
        result = self.orchestrator_module.orchestrate(input)
        return result

        



