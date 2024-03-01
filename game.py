import random
import random


class cards:
    def __init__(self):
        self.cards = ['a', 'a', 'a', 'a', '1', '1', '1', '1', '2', '2', '2', '2', '3', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5',
                      '6', '6', '6', '6', '8', '8', '8', '8', '9', '9', '9', '9', '10', '10', '10', '10', 'j', 'j', 'j', 'j', 'q', 'q', 'q', 'q', 'k', 'k', 'k', 'k']
        self.n = len(self.cards)
        self.count = 0

    def removeCard(self, c):
        self.cards.remove(c)
        self.n = self.n - 1
        return

    def adjustCount(self, c):
        # c = card being removed
        if c == 'j' or c == 'q' or c == 'k' or c == 'a':
            self.count -= 1
        elif int(c) < 7:
            self.count += 1


class player:
    def __init__(self, deck):
        self.deck = deck
        self.total = 0
        self.hand = []
        self.aces = 0
        self.hit()
        self.hit()

    def getVal(self, card):
        if card == 'j' or card == 'q' or card == 'k':
            return 10
        elif card == 'a':
            return 11
        else:
            return int(card)

    def sum(self, card):
        n = self.total
        if card == 'j' or card == 'q' or card == 'k':
            n = n + 10
        elif card == 'a':
            self.aces += 1
            n = n + 11
        else:
            n = n + int(card)
        self.total = n
        return

    def hit(self):
        c = self.deck.cards[random.randint(0, self.deck.n - 1)]
        self.hand.append(c)
        self.sum(c)
        self.deck.removeCard(c)
        return

    def bust(self):
        if self.total <= 21:
            return False
        else:
            if self.aces >= 1:
                self.total -= 10
                self.aces -= 1
                if self.total > 21:
                    return True
                return False
            else:
                return True

    def decision(self):
        while True:
            print("your hand is: ", self.hand)
            print("your total is: ", self.total)
            dec = int(input("type 1 to hit and 2 to stay"))
            if dec == 1:
                self.hit()
                if self.bust() == True:
                    print("your hand is: ", self.hand)
                    print("your total is: ", self.total)
                    print("You bust")
                    return
            else:
                return


class dealer(player):

    def policy(self):
        while True:
            print("Dealer hand is: ", self.hand)
            print("Dealer total is: ", self.total)
            if self.total <= 16:
                self.hit()
                if self.bust() == True:
                    print("Dealer hand is: ", self.hand)
                    print("Dealer total is: ", self.total)
                    print("Dealer bust")
                    return
            else:
                return


class state():
    def __init__(self, p, d):
        self.pTotal = p.total
        self.pHand = p.hand
        self.dCard = d.hand[0]
        print("ptot: ", self.pTotal)
        print("pHand: ", self.pHand)
        print("dCard: ", self.dCard)
        # evenetually add card count

    def getState(self):
        return self.pTotal, self.pHand, self.dCard


class game():
    def __init__(self):
        self.c = cards()
        self.p = player(self.c)
        self.d = dealer(self.c)
        self.state = state(self.p, self.d)
        self.reward = 0

    def updateState(self):
        self.state = state(self.p, self.d)

    def winner(self):
        if self.p.total > 21:
            print("Dealer Wins")
            self.reward = -1
        elif self.d.total > 21:
            print("Player Wins (Dealer Busts")
            self.reward = 1
        elif self.p.total > self.d.total:
            print("Player wins")
            self.reward = 1
        elif self.p.total == self.d.total:
            print("push")
            self.reward = 0
        else:
            self.reward = -1
            print("Dealer wins")
        return self.reward

    def play(self):
        if self.d.total == 21:
            reward = self.winner()
            return reward
        self.p.decision()
        self.updateState()
        if self.p.total < 21:
            self.d.policy()
        self.updateState()
        reward = self.winner()
        return reward


def main():
    print("This is the main function")
    g = game()
    print(g.p.hand)
    print(g.p.total)
    print(g.d.hand)
    print(g.d.total)
    reward = g.play()
    print(reward)


if __name__ == "__main__":
    main()
