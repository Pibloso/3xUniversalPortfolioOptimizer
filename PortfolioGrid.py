
from DataImportYH import np
from DataImportYH import plt
from DataImportYH import returns

step = 0.01
weights = []
borrow = (1-0.092)**(1/252)-1

for w_vt in np.arange(0, 1/.3 + step, step):
    for w_vmfo in np.arange(0, 1/.3 + step, step):
        w_cash = 1 - w_vt - w_vmfo
        if w_cash >1 or w_vt + w_vmfo > 1/.3:
            continue
        elif w_cash <0:
            if sum(w_vt * returns['VT']) + sum(w_vmfo * returns['VFMO']) + sum([w_cash * borrow]) <0:
                continue 
        weights.append((w_vt, w_vmfo, w_cash))

portfolio_log_returns = []
for w_vt, w_vmfo, w_cash in weights:
    port_log_return = (
        w_vt * returns['VT'] +
        w_vmfo * returns['VFMO']
        )
    if w_cash >=0:
        port_log_return += w_cash * returns['CASH']
    else: port_log_return += w_cash * borrow
    cum_log_wealth = port_log_return.cumsum()
    portfolio_log_returns.append(cum_log_wealth)

print(len(portfolio_log_returns),len(weights))

final_wealths = [p.iloc[-1] for p in portfolio_log_returns]
wavg = final_wealths / sum(final_wealths)
best_weights = np.average(weights, axis=0, weights=wavg)
print(f"Best Allocation VT:{best_weights[0]}, VFMO: {best_weights[1]}, CASH: {best_weights[2]}")

top_n = 5
top_indices = np.argsort(final_wealths)[-top_n:]

for idx in top_indices:
    print(weights[idx], final_wealths[idx])

plt.figure(figsize=(12, 6))
for idx in top_indices:
    label = f"VT: {weights[idx][0]:.2f}, VFMO: {weights[idx][1]:.2f}, CASH: {weights[idx][2]:.2f}"
    plt.plot(portfolio_log_returns[idx],label=label)

plt.grid(True)
plt.tight_layout()
plt.show()
