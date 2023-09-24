from keras.models import load_model
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from main import BlackJack
from keras.optimizers import Adam
import numpy as np

env1 = BlackJack(4)
states1=np.array([env1.reset()])
states = env1.player_hand, env1.house_hand, env1.A_Player,env1.Prob()
#Loading model from a file
model = load_model(".\\model_nauczony")
memory = SequentialMemory(limit=5000, window_length=1)
agent = DQNAgent(model=model, memory=memory, policy=BoltzmannQPolicy(), nb_actions=2, nb_steps_warmup=20,
                 target_model_update=1e-2)
agent.compile(optimizer=Adam(learning_rate=1e-3))
wynik = agent.test(env=env1, nb_episodes=1000, visualize=False, verbose=0)
#testing Model
skutecznosc = 0
print(wynik.history.keys())
for i in wynik.history['episode_reward']:
    skutecznosc += i
mozliwosci=0
for i in wynik.history['nb_steps']:
    mozliwosci += i
print(skutecznosc/mozliwosci)
print(model.predict(states1.reshape((1, 1, 4))))

