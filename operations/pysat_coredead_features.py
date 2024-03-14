from typing import Any

from pysat.solvers import Solver

from flamapy.core.operations import Operation
from flamapy.metamodels.pysat_metamodel.models.pysat_model import PySATModel


class SATCoreDeadFeatures(Operation):

    def __init__(self, solver_name: str = 'glucose3') -> None:
        self.result: tuple[list[Any], list[Any]] = ()
        self.solver_name = solver_name

    def get_coredead_features(self) -> tuple[list[Any], list[Any]]:
        return self.result

    def get_result(self) -> tuple[list[Any], list[Any]]:
        return self.result

    def execute(self, model: PySATModel) -> 'SATCoreDeadFeatures':
        solver = Solver(name=self.solver_name)
        self.result = coredead_features(model, solver)
        if solver is not None:
            try:
                solver.delete()
            except:
                pass
        return self
        

def coredead_features(model: PySATModel, solver: Solver) -> tuple[list[Any], list[Any]]:
    for clause in model.get_all_clauses():
        solver.add_clause(clause) 
    core_features = []
    dead_features = []
    if solver.solve():
        for variable in model.variables.items():
            if not solver.solve(assumptions=[-variable[1]]):
                core_features.append(variable[0])
            if not solver.solve(assumptions=[variable[1]]):
                dead_features.append(variable[0])
    return (core_features, dead_features)