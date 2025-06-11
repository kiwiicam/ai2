import pyautogui
import time
import keyboard
import numpy as np
import random
from collections import defaultdict

# Hyperparameters
INITIAL_EPSILON = 1.0
MIN_EPSILON = 0.01        
DECAY_RATE = 0.9995
LEARNING_RATE = 0.4
DISCOUNT_FACTOR = 0.9

class QLearningAgent:
    def __init__(self):
        # Discretized state space: (time_mod, obstacle_detected)
        # States: 100 time slots × 2 obstacle states = 200 states
        self.q_table = np.zeros((200, 2))  # 200 states, 2 actions
        self.epsilon = INITIAL_EPSILON
        self.last_jump_time = 0
        
    def get_state(self):
        """Simplified state representation for Geometry Dash"""
        # Time since last jump (discretized into 0-99)
        time_since_jump = min(int((time.time() - self.last_jump_time) * 10), 99)
        
        # Simple obstacle detection (adjust coordinates for your game)
        # Returns 1 if obstacle detected, 0 otherwise
        obstacle = 0
        try:
            if pyautogui.pixel(700, 500)[0] < 100:  # Dark pixel = obstacle
                obstacle = 1
        except:
            pass
            
        return time_since_jump * 2 + obstacle  # 0-199 state index
    
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 1)  # Explore
        return np.argmax(self.q_table[state])  # Exploit
    
    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + DISCOUNT_FACTOR * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += LEARNING_RATE * td_error
    
    def decay_epsilon(self):
        self.epsilon = max(MIN_EPSILON, self.epsilon * DECAY_RATE)

def is_alive():
    """Check if player is still alive"""
    try:
        return pyautogui.pixel(636, 68) == (114, 228, 3)  # Green = alive
    except:
        return False

def train(episodes):
    agent = QLearningAgent()
    
    for episode in range(1, episodes+1):
        agent.last_jump_time = time.time()
        start_time = time.time()
        survived_time = 0
        
        while is_alive():
            if keyboard.is_pressed('esc'):
                print("Training stopped by user")
                np.savetxt("q_table_gd.txt", agent.q_table)
                return
            
            # Get current state
            state = agent.get_state()
            
            # Choose and execute action
            action = agent.choose_action(state)
            if action == 0:  # Jump
                pyautogui.click(500, 500)
                agent.last_jump_time = time.time()
            
            # Wait briefly to see result (shorter than original)
            time.sleep(0.05)
            
            # Get new state and reward
            new_state = agent.get_state()
            survived_time = time.time() - start_time
            reward = 1 if is_alive() else -100
            
            # Update Q-table
            agent.update_q_table(state, action, reward, new_state)
            
            # Decay exploration rate
            agent.decay_epsilon()
        
        print(f"Episode {episode}: Survived {survived_time:.1f}s | ε={agent.epsilon:.3f}")
    
    np.savetxt("q_table_gd.txt", agent.q_table)

def play():
    """Run the trained agent"""
    q_table = np.loadtxt("q_table_gd.txt")
    agent = QLearningAgent()
    agent.q_table = q_table
    agent.epsilon = 0  # Pure exploitation
    
    print("Running trained agent (Press ESC to stop)")
    while not keyboard.is_pressed('esc'):
        agent.last_jump_time = time.time()
        while is_alive():
            state = agent.get_state()
            action = np.argmax(agent.q_table[state])
            
            if action == 0:  # Jump
                pyautogui.click(500, 500)
                agent.last_jump_time = time.time()
            
            time.sleep(0.02)  # Very short delay for responsiveness

# Start after 3 second delay
print("Starting in 3 seconds...")
time.sleep(3)

# Uncomment one of these:
#train(50000)  # Train the agent
play()        # Run the trained agent