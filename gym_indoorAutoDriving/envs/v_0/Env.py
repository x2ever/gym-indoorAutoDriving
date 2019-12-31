import gym
import numpy as np
import cv2

from gym import error, spaces, utils
from gym.utils import seeding

from ..env_utilsenv_utils import *

class indoorAutoDrivingEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, map_size=32, random_shifting=False):
        self.observation_space = spaces.Box(low=0, high=1, shape=(9 * 5 + map_size * 4 + 4, )) # Obs space + start_X, start_Y, target_X, target_Y, direction
        self.action_space = spaces.Discrete(9) # 3x3 (Left Stop Right), (Forward Stop Backward)
        self.map_size = map_size
        self.without_reward = 0
        self.random_shifting = random_shifting
        m = Map(size=map_size)
        wall_obstacles = [
            WallObstacle((0, 0), width=map_size),
            WallObstacle((0, 0), height=map_size),
            WallObstacle((map_size - 1, 0), width=map_size),
            WallObstacle((0, map_size - 1), height=map_size)
        ]

        table_obstacles = [
            TableObstacle((np.random.randint(map_size), np.random.randint(map_size))) for i in range(10)
        ]
        
        for table_obstacle in table_obstacles:
            m.addObstacle(table_obstacle)

        for wall_obstacle in wall_obstacles:
            m.addObstacle(wall_obstacle)

        self.map_state = m.data

        while True:
            robot_pos = np.random.randint(map_size, size=2)
            if self.map_state[robot_pos[0], robot_pos[1]] == 0:
                break

        while True:
            target_pos = np.random.randint(map_size, size=2)
            if self.map_state[target_pos[0], target_pos[1]] == 0:
                break

        self.robot_pos = robot_pos
        self.target_pos = target_pos
        self.direction = np.random.randint(4)

    def step(self, action):
        done = False
        obs = None
        reward = 0
        info = {}

        direction = action // 3
        speed = action % 3 - 1

        if direction == 1:
            self.direction += 1
            self.direction %= 4
        elif direction == 0:
            pass
        elif direction == -1:
            self.direction -= 1
            self.direction %= 4
        else:
            pass
        
        # speed: -1 or 0 or 1
        if self.direction == 0:
            self.robot_pos[0] += speed
        elif self.direction == 1:
            self.robot_pos[0] -= speed
        elif self.direction == 2:
            self.robot_pos[1] += speed
        elif self.direction == 3:
            self.robot_pos[1] -= speed
        else:
            pass

        if (self.robot_pos == self.target_pos).all():
            done = True
            reward = 1

        if self.map_state[self.robot_pos[0], self.robot_pos[1]] != 0:
            done = True
            reward = -1

        if self.without_reward > self.map_size * self.map_size:
            done = True
            reward = 0

        if done:
            obs = None
        else:
            self.without_reward += 1
            obs = self._make_obs_space()
        
        return obs, reward, done, info

    def reset(self):
        self.__init__()
        obs = self._make_obs_space()

        return obs

    def render(self, mode='human', close=False):
        img = None

        return img

    def _make_obs_space(self, init=True):
        map_state = np.copy(self.map_state)

        direction_obs = np.zeros((4, ))
        # Enter Direction
        direction_obs[self.direction] = 1

        if init:
            # Enter Robot and Target
            mission_obs = np.zeros((4, self.map_size))
            mission_obs[0, self.robot_pos[0]] = 1
            mission_obs[1, self.robot_pos[1]] = 1
            mission_obs[2, self.target_pos[0]] = 1
            mission_obs[3, self.target_pos[1]] = 1

            # Save and Don't Change
            self.mission_obs = mission_obs
        else:
            mission_obs = self.mission_obs

        map_obs= np.ones((9, 9)) * 0.7 # intensity of wall.
        for i in range(-4, 5):
            for j in range(-4, 5):
                if 0 <= i + self.robot_pos[0] < self.map_size and 0 <= j + self.robot_pos[1] < self.map_size:
                    map_obs[4 + i, 4 + j] = map_state[i + self.robot_pos[0], j + self.robot_pos[1]]

        if self.direction == 0:
            map_obs = map_obs[4:, :]
        elif self.direction == 1:
            map_obs = map_obs[:5, :]
        elif self.direction == 2:
            map_obs = map_obs[:, 4:]
        elif self.direction == 3:
            map_obs = map_obs[:, :5]
        else:
            pass

        flatten_map_obs = np.reshape(map_obs, (-1,))
        flatten_mission_obs = np.reshape(mission_obs, (-1,))
        flatten_direction_obs = np.reshape(direction_obs, (-1,))

        obs = np.concatenate((flatten_direction_obs, flatten_map_obs, flatten_mission_obs), axis=None)

        return obs

if __name__ == "__main__":
    env = indoorAutoDrivingEnv(map_size=8)
    while True:
        obs = env.reset()

        while True:
            # obs state shape test:
            if obs.shape != (177, ):
                raise Exception
            else:
                print(obs.shape)

            action = np.random.randint(9)
            obs, reward, done, info = env.step(action)
            if done:
                break

    