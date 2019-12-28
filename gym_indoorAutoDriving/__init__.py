from gym.envs.registration import register

register(
    id='indoorAutoDriving-v0',
    entry_point='gym_indoorAutoDriving.envs:indoorAutoDrivingEnv',
)