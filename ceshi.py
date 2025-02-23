import numpy as np
from gym_pybullet_drones.envs.HoverDistb import HoverDistbEnv
from gym_pybullet_drones.envs.HoverAviary import HoverAviary
from stable_baselines3.common.env_checker import check_env
import os 
import json
import pandas
import torch
import torch.nn as nn
import imageio


# Function to create GIF
def create_gif(image_list, filename, duration=0.1):
    images = []
    for img in image_list:
        images.append(img.astype(np.uint8))  # Convert to uint8 for imageio
    imageio.mimsave(f'{filename}', images, duration=duration)


# Check the env
env = HoverDistbEnv(disturbance_type='fixed', distb_level=0.0, record=True, randomization_reset=False)
# check_env(env)
# init_obs, init_info = env.reset()
# print(f"The init_obs shape is {init_obs.shape}")
# print(f"The initial position is {init_obs[0][0:3]}")

# check performances
print(f"The disturbance level is {env.distb_level}")
num_gifs = 1
frames = [[] for _ in range(num_gifs)]

num=0

while num < num_gifs:
    terminated, truncated = False, False
    rewards = 0.0
    steps = 0
    max_steps=500
    init_obs, init_info = env.reset()
    print(f"The init_obs shape is {init_obs.shape}")
    print(f"The initial position is {init_obs[0][0:3]}")
    frames[num].append(env.get_CurrentImage())  # the return frame is np.reshape(rgb, (h, w, 4))
    
    for _ in range(max_steps):
        # action, _ = validate_model.predict(obs, deterministic=False)
        motor = 0.0
        action = np.array([[motor, motor, motor, motor]])
        # action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        # print(f"The current reward of the step{_} is {reward} and this leads to {terminated} and {truncated}")
        # print(f"The current penalty of the step{_} is {info['current_penalty']} and the current distance is {info['current_dist']}")
        frames[num].append(env.get_CurrentImage())
        rewards += reward
        steps += 1
        
        if terminated or truncated or steps>=max_steps:
            print(f"[INFO] Test {num} is terminated or truncated with rewards = {rewards} and {steps} steps.")
            create_gif(frames[num], f'check_env_gif{num}-motor{motor}-{steps}.gif', duration=0.1)
            print(f"The final position is {obs[0][0:3]}.")
            num += 1
            break
env.close()