def raise_implied(line):
    prob_1 = 1 / line[3]
    prob_2 = 1 / line[5]
    total = prob_1 + prob_2
    if total < 1:
        return True
    return False

def calculate_stakes(arb, winnings):
    stake_1 = (float(winnings) / arb[3])
    stake_2 = (float(winnings) / arb[5])
    total_stake = stake_1 + stake_2
    profit = float(winnings) - total_stake
    print(f"Bet ${stake_1:.2f} on {arb[1]} at {arb[4]} and ${stake_2:.2f} on {arb[2]} at {arb[6]} on {arb[0]} for a total stake of ${total_stake:.2f} to profit ${profit:.2f}.") 
