#!/usr/bin/env python3
"""
train_atari.py
"""
import torch
import torch.optim as optim
import wandb

from agents import NaiveDQNAgent, DQN2013Agent
from commons import get_linear_decay, get_train_args
from networks import DQN
from replays import UniformReplayBuffer
from wrappers import make_env


def main():
    # Check GPU
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    # Parse arguments
    ARGS = get_train_args()

    # Setup wandb
    wandb.init(project='baselines')
    wandb.config.update(ARGS)

    # Setup Environment
    env = make_env(ARGS.ENV_ID)

    # Setup NaiveDQNAgent
    if ARGS.AGENT == 'naive':
        dqn = DQN(num_inputs=env.observation_space.shape[0],
                  num_actions=env.action_space.n).to(device)
        optimizer = optim.Adam(dqn.parameters(), lr=ARGS.LR)
        epsilon_func = get_linear_decay(ARGS.EPSILON_DECAY_START, ARGS.EPSILON_DECAY_FINAL, ARGS.EPSILON_DECAY_DURATION)
        agent = NaiveDQNAgent(env, dqn, optimizer, epsilon_func, device,
                              ARGS.DISCOUNT)
    # Setup DQN2013Agent
    elif ARGS.AGENT == 'dqn2013':
        dqn = DQN(num_inputs=env.observation_space.shape[0],
                  num_actions=env.action_space.n).to(device)
        optimizer = optim.Adam(dqn.parameters(), lr=ARGS.LR)
        epsilon_func = get_linear_decay(ARGS.EPSILON_DECAY_START, ARGS.EPSILON_DECAY_FINAL, ARGS.EPSILON_DECAY_DURATION)
        replay_buffer = UniformReplayBuffer(ARGS.REPLAY_BUFFER_SIZE)
        agent = DQN2013Agent(env, dqn, optimizer, replay_buffer, epsilon_func, device,
                             ARGS.DISCOUNT,
                             ARGS.BATCH_SIZE,
                             ARGS.MIN_REPLAY_BUFFER_SIZE)

    # Train agent
    agent.train(ARGS.NB_STEPS)


if __name__ == '__main__':
    main()
