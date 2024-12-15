import numpy as np
from GameEnvironment import PokerEnv
from APEAgent import PokerAgent

MAX_STATE_SIZE = 10  # Define a fixed state size for consistency

def pad_state(state):
    """
    Pads or truncates a state to match the defined MAX_STATE_SIZE.
    """
    return np.pad(state, (0, max(0, MAX_STATE_SIZE - len(state))), mode='constant')[:MAX_STATE_SIZE]

def train_poker_bot(episodes=1000, batch_size=32, weights_file="poker_bot_weights.weights.h5"):
    env = PokerEnv()
    action_size = 3  # Fold, Call, Raise

    print(f"Environment initialized. State size: {MAX_STATE_SIZE}, Action size: {action_size}")

    # Initialize the agent with the fixed state size
    agent = PokerAgent(MAX_STATE_SIZE, action_size)

    for e in range(episodes):
        state = env.reset()
        state = pad_state(state)  # Ensure state matches MAX_STATE_SIZE
        state = np.reshape(state, [1, MAX_STATE_SIZE])  # Reshape for compatibility

        for time in range(500):
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            next_state = pad_state(next_state)  # Pad the next state
            next_state = np.reshape(next_state, [1, MAX_STATE_SIZE])  # Reshape for consistency

            agent.remember(state, action, reward, next_state, done)
            state = next_state

            if done:
                agent.update_target_model()
                print(f"Episode {e + 1}/{episodes} - Time {time} - Reward: {reward} - Epsilon: {agent.epsilon:.2}")
                break

        # Replay experiences
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

        # Save weights periodically
        if (e + 1) % 100 == 0:
            agent.model.save_weights(weights_file)
            print(f"Weights saved at episode {e + 1}")

    # Final save
    agent.model.save_weights(weights_file)
    print(f"Training completed. Final weights saved to {weights_file}.")

if __name__ == "__main__":
    train_poker_bot()
