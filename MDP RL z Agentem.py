import gym
import numpy as np

from main import BlackJack
from keras import Sequential

from keras.layers import Dense, Flatten
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from keras.optimizers import Adam


#buliding Deep Reinforcment Leranign model
env1 = BlackJack(4)
states1 = np.array([env1.reset()])
states = [env1.player_hand, env1.house_hand, env1.A_Player,env1.Prob()]
actions = [0, 1]
model = Sequential()
#Input data PlayerHand, HouseHand, Numer of A's on players hand, Propability of drawing not lossing card by Player
model.add(Flatten(input_shape=(1,len(states))))
print(model.output_shape)
model.add(Dense(32, activation='relu'))
print(model.output_shape)
model.add(Dense(32, activation='relu'))
print(model.output_shape)
model.add(Dense(input_shape=(len(actions),), activation='softmax', units=2))
print(model.output_shape)
memory = SequentialMemory(limit=20000, window_length=1)
policy = BoltzmannQPolicy()
agent = DQNAgent(model=model, memory=memory, policy=policy, nb_actions=2, nb_steps_warmup=20000, target_model_update=1e-2)
#Start of learning process
agent.compile(optimizer=Adam(learning_rate=1e-3))
agent.fit(env1, nb_steps=20000, visualize=False, verbose=1)
wynik = agent.test(env=env1, nb_episodes=100, visualize=False, verbose=0)
# Testing Model
print(wynik.history.keys)
skutecznosc = 0
for i in wynik.history['episode_reward']:
    skutecznosc += i
mozliwosci = 0
for i in wynik.history['nb_steps']:
    mozliwosci += i
print(skutecznosc/mozliwosci)
print(model.predict(states1.reshape((1, 1, 4))))
# Saving model to a file
model.save("model_nauczony", save_format="keras", include_optimizer=True)


