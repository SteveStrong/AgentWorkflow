from abc import ABC, abstractmethod
from typing import List, Dict, Any, Set
import re


class TransformAgent(ABC):
    input_agents: List[str]
    description: str = ""
    output_ext: str

    def __init__(self, step_num):
        if not self.output_ext:
            raise ValueError(
                f"Output extension not provided for {self.__class__.__name__}"
            )

        self.step_num = step_num

    def compute_filename(self, source_filename: str) -> str:

        # Extract base name (without extension if present)
        if "." in source_filename:
            base_name, ext = source_filename.rsplit(".", 1)
        else:
            base_name = source_filename

        # Check if base_name ends with _x (where x is a digit sequence)
        match = re.search(r"_(\d+)$", base_name)
        if match:
            new_name = re.sub(r"_\d+$", f"_{self.step_num}", base_name)
        else:
            # Append _step_num to the base name
            new_name = f"{base_name}_{self.step_num}"

        return f"{new_name}.{self.output_ext}"

    @abstractmethod
    def process_tdp_content(self, content: bytes) -> bytes:
        pass
