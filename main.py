from numpy.random import choice


#Creating a BlackJack environment from scratch to include the possibility of card counting
class BlackJack(object):
    def __init__(self,liczba_talii):
        self.liczba_talii = liczba_talii
        # Zakładmy 4 zestawy kart
        self.cards_value = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10,
                      'K': 10, 'A': 11}
        self.cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        #self.cards_quant = {'2': 16, '3': 16, '4': 16, '5': 16, '6': 16, '7': 16, '8': 16, '9': 16, '10': 16, 'J': 16,
                            #'Q': 16, 'K': 16, 'A': 16}
        self.cards_quant = {i: 4 * liczba_talii for i in self.cards}
        self.player_hand = 0
        self.house_hand = 0
        self.A_Player = 0
        self.A_House = 0
        self.dobierzkarteGracze()
        self.dobierzkarteGracze()
        self.dobierzkarteHouse()
        self.games = 0

    def step(self, actions):
        reward = 0
        info = {}
        prob = self.Prob()
        if self.player_hand == 21:
            actions = 0
            done = True
            reward = 1
        elif actions == 0:  # stand
            while self.house_hand < 17:
                self.dobierzkarteHouse()
                if self.house_hand > 21 and self.A_House != 0:
                    self.house_hand -= 10
                    self.A_House -= 1
            if self.player_hand > 21:
                reward = -1
            elif self.house_hand > 21:
                reward = 1
            elif self.player_hand > self.house_hand:
                reward = 1
            elif self.player_hand < self.house_hand:
                reward = -1
            else:
                reward = 0
            done = True
        else:                   # hit
            self.dobierzkarteGracze()
            if self.player_hand > 21 and self.A_Player > 0:
                self.player_hand -= 10
                self.A_Player -= 1
            if self.player_hand > 21:
                done = True
                reward = -1
            else:
                done = False
        gracz = self.player_hand
        kasyno = self.house_hand
        if done == True:
            self.reset()

        return [gracz, kasyno, self.A_Player, prob], done, reward, info

    def Hreset(self):
        self.cards_value = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10,
                            'K': 10, 'A': 11}
        self.cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards_quant = {'2': 16, '3': 16, '4': 16, '5': 16, '6': 16, '7': 16, '8': 16, '9': 16, '10': 16, 'J': 16,
                            'Q': 16, 'K': 16, 'A': 16}
        self.player_hand = 0
        self.house_hand = 0
        self.A_Player = 0
        self.A_House = 0
        self.dobierzkarteGracze()
        self.dobierzkarteGracze()
        self.dobierzkarteHouse()

    def dobierzkarteGracze(self):
        suma=0
        czypusty=False
        for i in self.cards_quant.values():
            suma += i
        if suma <= 12:
            czypusty =True
        if czypusty:
            self.cards_quant = {'2': 16, '3': 16, '4': 16, '5': 16, '6': 16, '7': 16, '8': 16, '9': 16, '10': 16,'J': 16, 'Q': 16, 'K': 16, 'A': 16}
        karta = choice(self.cards)
        if self.cards_quant[karta] == 0:
            self.dobierzkarteGracze()
        else:
            if karta == 'A':
                self.A_Player += 1
            self.player_hand += self.cards_value[karta]
            self.cards_quant[karta] -= 1

    def dobierzkarteHouse(self):
        suma = 0
        czypusty = False
        for i in self.cards_quant.values():
            suma += i
        if suma <= 12:
            czypusty = True
        if czypusty:
            self.cards_quant = {'2': 16, '3': 16, '4': 16, '5': 16, '6': 16, '7': 16, '8': 16, '9': 16, '10': 16,
                                'J': 16, 'Q': 16, 'K': 16, 'A': 16}
        karta = choice(self.cards)
        if self.cards_quant[karta] == 0:
            self.dobierzkarteHouse()
        else:
            if karta == 'A':
                self.A_House += 1
            self.house_hand += self.cards_value[karta]
            self.cards_quant[karta] -= 1
    def Prob(self):
        suma = 0
        dobre = 0
        if self.A_Player > 0:
            chance = 1
        else:
            for i in self.cards_quant.values():
                suma += i
            if suma < 12:
                self.DeckRestart()
                suma = 208
            for i in self.cards:
                if self.player_hand + self.cards_value[i] <= 21:
                    dobre += self.cards_quant[i]
            chance = dobre/suma
        return chance
    def reset(self):
        self.player_hand = 0
        self.house_hand = 0
        self.A_Player = 0
        self.A_House = 0
        self.dobierzkarteGracze()
        self.dobierzkarteGracze()
        self.dobierzkarteHouse()
        return self.player_hand, self.house_hand, self.A_Player, self.Prob()
    def DeckRestart(self):
        suma = 0
        czypusty = False
        for i in self.cards_quant.values():
            suma += i
        if suma <= 12:
            czypusty =True
        if czypusty:
            self.cards_quant = {'2': 16, '3': 16, '4': 16, '5': 16, '6': 16, '7': 16, '8': 16, '9': 16, '10': 16,
                                'J': 16,
                                'Q': 16, 'K': 16, 'A': 16}
    def Show(self):
        print(self.player_hand,self.house_hand)


#Testing environment on 100 games with random actions
BJ1 = BlackJack(4)
score = 0
suma = 0
for i in range(0, 10):
    for j in range(0, 10):
        done = False
        while not done:
            #print(1-BJ1.Prob(), BJ1.Prob())
            actions = choice([0, 1])
            BJ1.Show()
            observation, done, reward, info = BJ1.step(actions)
            score += reward
            print(f"Gracz:{observation[0]},Kasyno:{observation[1]},akcja:{actions},prob:{round(observation[2],3)},reward:{reward}")
        BJ1.reset()
        print("Gra Zakończona!!!!")
print(score)