from dataclasses import dataclass
from domain.billboards import Billboard
@dataclass
class BillboardRepsitory:
    config: dict


    def add(self, billboard: Billboard):
        pass