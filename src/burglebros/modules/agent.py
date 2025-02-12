"""
"""

import numpy as np
import random
from burglebros.configs.configs import *
from burglebros.utilities.vprint import vprint

# Q-learning constants
if AGENT_EXPLORING:  
    epsilon = 0.1  # Exploration rate
else:
    epsilon = 0  # Do not explore
alpha = 0.02  # Learning rate
gamma = 0.9  # Discount factor

class Agent:

    def __init__(self, x=0, y=0, stealth=3, actions_per_turn=4):
        self.x = x
        self.y = y
        self.stealth = stealth
        self.actions_per_turn = actions_per_turn
        self.floor = None
        self.just_cracked_safe = False
        self.just_discovered_safe = False
        self.escaped = False
        self.reward = 0
        self.current_state = None
        self.current_action = None
        self.actions_taken_this_turn = []

        self.action_space = ["MOVE_UP", "MOVE_RIGHT", "MOVE_DOWN", "MOVE_LEFT", "CRACK_SAFE"]
        self.stats = {}
        self.stats['total_reward'] = 0
        self.stats['counter_found_safes'] = 0
        self.stats['counter_cracked_safes'] = 0
        self.stats['counter_move_into_guard'] = 0
        self.stats['counter_guard_move_into_agent'] = 0

    def add_q_table(self, q_table):
        self.q_table = q_table
    
    def add_floor(self, floor):
        self.floor = floor

    def is_move_valid(self, dx, dy):
        """Ensure an attempted move would be valid (within boundaries)."""
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < self.floor.grid_size and 0 <= new_y < self.floor.grid_size:
            return True
        else:
            return False
    
    def move(self, dx, dy):
        """Move the agent."""
        new_x, new_y = self.x + dx, self.y + dy
        if self.is_move_valid(dx, dy):
            self.x, self.y = new_x, new_y
            if self.floor.grid[new_x][new_y] == 'Trap':
                self.floor.guard.add_alarm(new_x, new_y) 
            if self.floor.grid[new_x][new_y] == 'Safe':
                if not self.floor.safe_location_discovered:
                    self.just_discovered_safe = True
                    self.floor.safe_location_discovered = True
            vprint(f"Agent {1} position after move: {self.x}, {self.y}") # TODO: Get rid of hardcoded 1
            return True
        return False
    
    def resolve_move_action(self, action):
        if action == 0:
            self.move(0, 1)
        elif action == 1:
            self.move(1, 0)
        elif action == 2:
            self.move(0, -1)
        elif action == 3:
            self.move(-1, 0)

        if self.just_discovered_safe:
            self.reward += REWARD_FOR_FINDING_SAFE
            self.just_discovered_safe = False
            self.stats['counter_found_safes'] += 1

        return

    def is_on_safe(self):
        if (self.x, self.y) == self.floor.safe_location:
            return True
        else:
            return False
        
    def attempt_to_crack_safe(self):
        """Attempts to crack the safe."""
        if (self.x, self.y) == self.floor.safe_location:
            if random.randint(1, 6) >= 4:
                self.floor.safe_cracked = True
                self.just_cracked_safe = True
                self.stats['counter_cracked_safes'] += 1
                vprint(f"Agent {1} has cracked the safe!") # TODO: Get rid of hardcoded 1
                return True # Safe cracked
        return False # Safe not cracked
    
    def get_state(self):
        if self.floor.safe_location_discovered:
            state = (self.x, 
                self.y, 
                self.floor.guard.x, 
                self.floor.guard.y,
                self.floor.guard.current_target[0],
                self.floor.guard.current_target[1],
                self.floor.safe_location[0],
                self.floor.safe_location[1],
                int(self.floor.safe_cracked)
            )
        else:
            state = (self.x, 
                self.y, 
                self.floor.guard.x, 
                self.floor.guard.y,
                self.floor.guard.current_target[0],
                self.floor.guard.current_target[1],
                -1,
                -1,
                int(self.floor.safe_cracked)
            )
        vprint(f"Agent {1} is in state: {state}") # TODO: Get rid of hardcoded 1
        return state

    def is_chosen_action_valid(self, choice):
        if choice == 0:
            if self.is_move_valid(0, 1):
                return True
            return False
        elif choice == 1:
            if self.is_move_valid(1, 0):
                return True
            return False
        elif choice == 2:
            if self.is_move_valid(0, -1):
                return True
            return False
        elif choice == 3:
            if self.is_move_valid(-1, 0):
                return True
            return False
        return True # Default, if not moving, is True

    def take_turn(self):
        self.actions_taken_this_turn = []
        self.reward = 0
        for i in range(self.actions_per_turn):
            vprint(f"Agent {1} taking action {i}") # TODO: Get rid of hardcoded 1
            self.current_state = self.get_state()
            self.current_action = self.choose_action()
            self.actions_taken_this_turn.append(self.current_action)
            
            # If action is to move
            if self.current_action in [0,1,2,3]:
                self.reward += PUNISHMENT_FOR_MOVING
                self.resolve_move_action(self.current_action)

                # Check if the agent moved into the guard's tile
                if (self.x, self.y) == (self.floor.guard.x, self.floor.guard.y):
                    self.stealth -= 1 # Lose a stealth token
                    self.reward += PUNISHMENT_FOR_LOSING_STEALTH # Punish for walking into a guard
                    self.stats['counter_move_into_guard'] += 1
                    if self.stealth == -1: # Game is over if agent loses stealth when they have no spare tokens
                        self.reward += PUNISHMENT_FOR_LOSING
                        break

            # If action is to attempt to crack the safe
            elif self.current_action == 4:
                if not self.floor.safe_cracked:
                    if self.is_on_safe():
                        if self.attempt_to_crack_safe():
                            self.reward += REWARD_FOR_SAFE_CRACK_ATTEMPT
                            if self.just_cracked_safe:
                                self.reward += REWARD_FOR_CRACKING_SAFE
                                self.just_cracked_safe = False
                    else:
                        # Not standing on a safe
                        self.reward += PUNISHMENT_FOR_BAD_SAFE_CRACK_ACTION_USE
                else:
                    # Safe is already cracked
                    self.reward += PUNISHMENT_FOR_BAD_SAFE_CRACK_ACTION_USE
            
            if self.floor.safe_cracked:
                if self.x == 0 and self.y == 0:
                    self.reward += REWARD_FOR_WINNING
                    self.escaped = True
        
            # On the last action, we hold off on giving a reward until we figure out if the guard is going to move into their space and cause them to lose stealth
            # In which case, we need to punish the agent for taking an action that put it at risk of the guard moving into it
            if i != self.actions_per_turn-1: 
                new_state = self.get_state()
                self.update_q_table(self.current_state, self.current_action, self.reward, new_state)
                self.stats['total_reward'] += self.reward
                vprint(f"Agent {1} reward for this action: {self.reward}") # TODO: Get rid of hardcoded 1
                self.reward = 0

        return
    
    def resolve_end_of_guards_turn(self):
        new_state = self.get_state()
        self.update_q_table(self.current_state, self.current_action, self.reward, new_state)
        self.stats['total_reward'] += self.reward
        vprint(f"Agent {1} reward for this final action: {self.reward}") # TODO: Get rid of hardcoded 1
        self.reward = 0

    def choose_random_action(self):
        choice = random.randint(0, len(self.action_space)-1)  # Explore: Random action
        while True: # Loop until a valid action is taken
            if self.is_chosen_action_valid(choice):
                break
            choice = random.randint(0, len(self.action_space)-1)  # Explore: Random action
        return choice
    
    def choose_action(self):
        chosen_action = None
        if random.uniform(0, 1) < epsilon:
            chosen_action = self.choose_random_action()
        else:
            choice = np.argmax(self.q_table[self.current_state]) # Exploit: Try to take the best action from Q-table
            if self.is_chosen_action_valid(choice):
                chosen_action = choice
            else: # The "best" action isn't actually valid, fall back to picking a random action
                chosen_action = self.choose_random_action()
        vprint(f"Agent {1} chosen action: {chosen_action}")
        return chosen_action
    
    def update_q_table(self, state, action, reward, new_state):
        best_next_action = np.max(self.q_table[new_state])
        self.q_table[state][action] = (1 - alpha) * self.q_table[state][action] + alpha * (reward + gamma * best_next_action)
