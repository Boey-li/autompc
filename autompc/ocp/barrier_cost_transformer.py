# Created by Teodor Tchalakov (tcha2@illinois.edu), 2022-04-18

# Standard library includes
import copy
from collections import defaultdict

# Internal library includes
from .ocp_transformer import OCPTransformer, PrototypeOCP
from ..costs import LogBarrierCost

# External library includes
import numpy as np
import ConfigSpace as CS
import ConfigSpace.hyperparameters as CSH
import ConfigSpace.conditions as CSC

def construct_default_bounds():
    return (0, 100, 1.0, False)
BARRIER_COST_DEFAULT_BOUNDS = (0, 100)
BARRIER_COST_DEFAULT_VALUE = 1.0
BARRIER_COST_DEFAULT_LOG = False
class LogBarrierCostTransformer(OCPTransformer):
    def __init__(self, system):
        self._scale_bounds = defaultdict(construct_default_bounds) # Key: obsname, Value: (lower, upper, default, log_scale)
        self._limits = {} # Key: obs/ctrlname, Value: (limit, upper)
        self._scale_fixed = {} # Key: obs/ctrlname, Value: limit
        super().__init__(system, 'LogBarrierCostTransformer')
    """
        boundedState : String
            Name of observation or control in the system.

        lower : double
            lower limit value that barrier is placed at.
            Default is -np.inf and the barrier isn't placed

        upper : double
            upper limit value that barrier is placed at.
            Default is -np.inf and the barrier isn't placed

    """
    def set_limit(self, boundedState, lower=-np.inf, upper=np.inf):
        if(boundedState in self.system.observations or boundedState in self.system.controls):
            self._limits[boundedState] = (lower, upper)
        else:
            raise ValueError(str(boundedState) + " is not in system")

    """
        boundedState : String
            Name of observation or control in the system.

        lower_bound : double
            lower bound of configuration space

        upper_bound : double
            upper bound of configuration space

        default : double
            default value of configuration space
        
        log : boolean
            Whether hyperparameter should use logarithmic scale. (Default: False)
    """
    def set_bounds(self, boundedState, lower_bound, upper_bound, default, log=False):
        if(boundedState in self.system.observations or boundedState in self.system.controls):
            if(boundedState in self._limits):
                self._scale_bounds[boundedState] = (lower_bound, upper_bound, default, log)

            else:
                raise ValueError(str(boundedState) + " does not have a configured limit use set_limit")
        else:
            raise ValueError(str(boundedState) + " is not in system")

    def set_fixed_scale(self, boundedState, scale):
        if(boundedState in self.system.observations or boundedState in self.system.controls):
            if(boundedState in self._limits):
                self._scale_fixed[boundedState] = scale
            else:
                raise ValueError(str(boundedState) + " does not have a configured limit use set_limit")
        else:
            raise ValueError(str(boundedState) + " is not in system")

    def _get_hyperparameters(self, label, bounds_dict, fixed_dict):
        hyperparameters = []
        for name in (self.system.controls + self.system.observations):
            if name in fixed_dict or name not in self._limits:
                continue
            lower, upper = self._limits[name]
            lower_scale, upper_scale, default, log = bounds_dict[name]
            hyper = CSH.UniformFloatHyperparameter("{}_{}".format(name, label),
                    lower=lower_scale, upper=upper_scale, default_value=default, log=log)
            hyperparameters.append(hyper)    
        return hyperparameters

    def _get_boundedState(self, cfg, label, fixed_dict):
        boundedStates = dict()
        for name in (self.system.controls + self.system.observations):
            if name in fixed_dict:
                lower, upper = self._limits[name]
                scale = self._scale_fixed[name]
                boundedStates[name] = (lower, upper, scale)
            elif name in self._limits:
                lower, upper = self._limits[name]
                hyper_name = f"{name}_{label}"
                scale = cfg[hyper_name]
                boundedStates[name] = (lower, upper, scale)
        return boundedStates

    def get_default_config_space(self):
        cs = CS.ConfigurationSpace()
        for name in self.system.observations + self.system.controls:
            hyper = CSH.UniformFloatHyperparameter(name+"_LogBarrier",
                                                lower=BARRIER_COST_DEFAULT_BOUNDS[0], upper=BARRIER_COST_DEFAULT_BOUNDS[1],
                                                default_value=BARRIER_COST_DEFAULT_VALUE, log=BARRIER_COST_DEFAULT_LOG
            )
            cs.add_hyperparameter(hyper)
        return cs

    def get_prototype(self, config, ocp):
        return PrototypeOCP(ocp, cost=LogBarrierCost)

    def is_compatible(self, ocp):
        return True
    
    def ocp_requirements(self) -> dict:
        return {}

    def __call__(self, ocp):
        boundedStates = self._get_boundedState(self.get_config(), "LogBarrier", self._scale_fixed)
        new_cost = LogBarrierCost(self.system, boundedStates)
        new_ocp = copy.deepcopy(ocp)
        new_ocp.set_cost(new_cost)
        return new_ocp

    