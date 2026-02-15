import numpy as np
import matplotlib.pyplot as plt

# --- 1. SETUP PARAMETERS ---
S0 = 100        # Initial Stock Price
mu = 0.10       # Expected Return (10%)
sigma = 0.20    # Volatility (20%)
T = 1.0         # Time Horizon (1 year)
days = 252      # Trading days in a year
sims = 1000     # Number of Simulations (The "Multiverse")

# Time step size
dt = T / days

# --- 2. VECTORIZED SIMULATION (The Pro Way) ---

# Step A: Generate ALL random shocks (Z) at once.
# We create a matrix of size (days x sims).
# Rows = Time, Columns = Different Simulations
# This replaces the loop inside the simulation.
Z = np.random.normal(0, 1, (days, sims))

# Step B: Calculate the daily returns for every single day and simulation at once.
# Formula: drift + diffusion
# drift is fixed for every step. shock depends on Z.
drift_daily = (mu - 0.5 * sigma**2) * dt
shock_daily = sigma * np.sqrt(dt) * Z

# This gives us a matrix of daily % changes (log returns)
daily_log_returns = drift_daily + shock_daily

# Step C: Accumulate returns over time (The "Path")
# np.cumsum adds them up: Day 1, Day 1+2, Day 1+2+3...
cum_returns = np.cumsum(daily_log_returns, axis=0)

# Step D: Convert returns back to Prices
# S_t = S_0 * e^(cumulative_returns)
# We add S0 to the top so every path starts at the same point
stock_paths = S0 * np.exp(cum_returns)

# Prepend the starting price (Day 0) to all paths
# (This is just for the chart to look nice, starting at 100)
S0_row = np.full((1, sims), S0)
stock_paths = np.vstack([S0_row, stock_paths])

# --- 3. VISUALIZATION ---
plt.figure(figsize=(12, 6))

# Plot the first 50 simulations (plotting all 1000 makes the computer lag)
plt.plot(stock_paths[:, :50], alpha=0.6, linewidth=0.8)

plt.title(f"Monte Carlo Simulation: {sims} Scenarios", fontsize=16)
plt.xlabel("Trading Days")
plt.ylabel("Price ($)")
plt.grid(True)
plt.show()

# --- 4. STATISTICS (The "So What?") ---
# Let's look at the FINAL price of all 1000 simulations (the last row)
final_prices = stock_paths[-1, :]

print(f"--- RESULTS FOR {sims} SIMULATIONS ---")
print(f"Average Final Price: ${np.mean(final_prices):.2f}")
print(f"Minimum Price:       ${np.min(final_prices):.2f}")
print(f"Maximum Price:       ${np.max(final_prices):.2f}")

# --- 5. VALUE AT RISK (VaR) ---
# We want to find the "cutoff" point for the worst 5% of scenarios.
# np.percentile(data, 5) finds the value where 5% of data is below it.

future_prices = stock_paths[-1, :] # Get all 1000 final prices
VaR_95 = np.percentile(future_prices, 5)

print(f"--- RISK METRICS ---")
print(f"VaR (95% Confidence): ${VaR_95:.2f}")
print(f"This means: We are 95% confident the price will NOT fall below ${VaR_95:.2f}")
print(f"Or: There is only a 5% chance the price falls below ${VaR_95:.2f}")

# Visualizing the Cutoff on a Histogram
plt.figure(figsize=(10, 6))
plt.hist(future_prices, bins=50, alpha=0.6, color='blue', edgecolor='black')
plt.axvline(x=VaR_95, color='red', linestyle='--', linewidth=2, label=f'95% VaR: ${VaR_95:.2f}')
plt.title("Distribution of Final Prices (Histogram)")
plt.xlabel("Price ($)")
plt.ylabel("Frequency")
plt.legend()
plt.show()