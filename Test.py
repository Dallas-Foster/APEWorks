import numpy as np
from GameEnvironment import PokerEnv
from APEAgent import PokerAgent

MAX_STATE_SIZE = 10  # Match the training configuration

def pad_state(state):
    """
    Pads or truncates a state to match the defined MAX_STATE_SIZE.
    """
    return np.pad(state, (0, max(0, MAX_STATE_SIZE - len(state))), mode='constant')[:MAX_STATE_SIZE]

def test_poker_bot(episodes=10, weights_file="poker_bot_weights.h5"):
    env = PokerEnv()
    action_size = 3  # Fold, Call, Raise

    print(f"Environment initialized. State size: {MAX_STATE_SIZE}, Action size: {action_size}")

    # Initialize the agent with the fixed state size
    agent = PokerAgent(MAX_STATE_SIZE, action_size)

    # Load weights
    try:
        agent.model.load_weights(weights_file)
        print(f"Weights loaded from {weights_file}.")
    except FileNotFoundError:
        print(f"Error: Weights file '{weights_file}' not found. Train the model first.")
        return

    for e in range(episodes):
        state = env.reset()
        state = pad_state(state)  # Pad the initial state
        state = np.reshape(state, [1, MAX_STATE_SIZE])  # Reshape for compatibility
        done = False
        total_reward = 0

        while not done:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            next_state = pad_state(next_state)  # Pad the next state
            next_state = np.reshape(next_state, [1, MAX_STATE_SIZE])  # Reshape for consistency
            state = next_state
            total_reward += reward

        print(f"Test Episode {e + 1}/{episodes} - Total Reward: {total_reward}")

if __name__ == "__main__":
    test_poker_bot()
