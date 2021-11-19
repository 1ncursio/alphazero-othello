from GameBorder import Border
from Qagent import Qplayer


if __name__ == "__main__":
    p1 = Qplayer(1)
    p2 = Qplayer(-1)
    border = Border()

    musyoubu = 0
    ler = 50000
    for x in range(ler):

        while border.done == False:
            if len(border.availablePositions()) == 0:
                p1.rewardUpdate(0.2)
                p2.rewardUpdate(0.2)
                musyoubu += 1
                break
            position = border.availablePositions()
            if(border.symbol == 1):
                action = p1.chooseAction(position, border.state)
                position = border.step(action, p1.symbol)
                p1.update(position)
            else:
                action = p2.chooseAction(position, border.state)
                position = border.step(action, p2.symbol)
                p2.update(position)
            if(border.done):
                if border.symbol == 1:
                    p1.rewardUpdate(1)
                    p1.count += 1
                    p2.rewardUpdate(-1)
                else:
                    p1.rewardUpdate(-1)
                    p2.rewardUpdate(1)
                    p2.count += 1
        p2.exp_rate = 0.5-x/(ler//1.5)
        p1.exp_rate = 0.5-x/(ler//1.5)
        border.reset()
        # print((0.5-x/(ler/2)))
        if x % 1000 == 0:
            print(x, '번째 훈련중')
            print((0.5-x/(ler//1.5)))
    p2.save()
