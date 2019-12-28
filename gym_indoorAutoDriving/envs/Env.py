import gym
import numpy as np
import cv2

from gym import error, spaces, utils
from gym.utils import seeding

class indoorAutoDrivingEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.state = None
        self.observation_space = None
        self.action_space = spaces.Discrete(4)

    def step(self, action):
        done = False
        reward = 0
        info = {}
        
        return self.state, reward, done, info

    def reset(self):
        self.__init__()

        return self.state

    def render(self, mode='human', close=False):
        img = None

        return img
