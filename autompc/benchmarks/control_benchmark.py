# Created by William Edwards (wre2@illinois.edu), 2021-01-08

# Standard library includes
from abc import ABC, abstractmethod

# External library includes
import numpy as np

# Internal library includes
from .modeling_benchmark import ModelingBenchmark

class ControlBenchmark(ModelingBenchmark):
    """
    Represents a Benchmark for testing AutoMPC, including the sytem,
    task, and a method of generating data.
    """
    def __init__(self, name, system, task, data_gen_method, default_num_trajs=500, default_traj_len=200):
        self.name = name
        self.system = system
        self.task = task
        self._data_gen_method = data_gen_method
        self._default_num_trajs = default_num_trajs
        self._default_traj_len = default_traj_len

        super().__init__(name, system)

    @abstractmethod
    def dynamics(self, x, u):
        """
        Benchmark dynamics

        Parameters
        ----------
        x : np array of size self.system.obs_dim
            Current observation

        u : np array of size self.system.ctrl_dim
            Control input

        Returns
        -------
        xnew : np array of size self.system.obs_dim
            New observation.
        """
        raise NotImplementedError

    @abstractmethod
    def gen_trajs(self, seed, n_trajs, traj_len=None):
        """
        Generate trajectories.

        Parameters
        ----------
        seed : int
            Seed for trajectory generation

        n_trajs : int
            Number of trajectories to generate

        traj_len : int
            Length of trajectories to generate. Default varies
            by benchmark.

        Returns
        -------
         : List of Trajectory
            Benchmark training set
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def data_gen_methods(self):
        """
        List available data generation methods

        Returns
        -------
         : List of strings
        """
        raise NotImplementedError

    def get_trajs(self, num_trajs=None):
        """ Inherited see superclass. """
        if num_trajs is None:
            num_trajs = self._default_num_trajs
        return self.gen_trajs(num_trajs=num_trajs, traj_len=self._default_num_trajs, seed=0)

    @property
    def max_num_trajs(self):
        return None
