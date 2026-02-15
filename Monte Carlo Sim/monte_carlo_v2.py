import numpy as np
import matplotlib.pyplot as plt

def run_simulation():
    print("--- MONTE CARLO SIMULATOR v2.0 ---")
    print("Please enter the simulation parameters:")
    
    # --- 1. USER INPUTS (Making it Dynamic) ---
    try:
        S0 = float(input("Current Stock Price ($): "))
        mu = float(input("Expected Annual Return (e.g., 0.10 for 10%): "))
        sigma = float(input("Annual Volatility (e.g., 0.20 for 20%): "))
        T = float(input("Time Horizon (Years): "))
        sims = int(input("Number of Simulations (Recommended: 1000-5000): "))
    except ValueError:
        print("Error: Please enter numbers only.")
        return

    days = int(T * 252)
    dt = T / days
    
    print(f"\nRunning {sims} simulations for {days} trading days...")

    # --- 2. THE ENGINE (Vectorized) ---
    stock_prices = np.zeros((days + 1, sims))
    stock_prices[0] = S0

    Z = np.random.normal(0, 1, (days, sims))
    drift_daily = (mu - 0.5 * sigma**2) * dt
    shock_daily = sigma * np.sqrt(dt) * Z
    
    daily_log_returns = drift_daily + shock_daily
    cum_returns = np.cumsum(daily_log_returns, axis=0)
    
    stock_paths = S0 * np.exp(cum_returns)
    
    # Add start price (S0) to the top
    S0_row = np.full((1, sims), S0)
    stock_paths = np.vstack([S0_row, stock_paths])

    # --- 3. ANALYSIS ---
    final_prices = stock_paths[-1, :]
    expected_price = np.mean(final_prices)
    cutoff_price = np.percentile(final_prices, 5) # 5th percentile
    VaR = S0 - cutoff_price # The actual money at risk
    
    # --- 4. PROFESSIONAL OUTPUT ---
    print("\n" + "="*40)
    print(f"RESULTS REPORT")
    print("="*40)
    print(f"Start Price:          ${S0:,.2f}")
    print(f"Expected Future Price:${expected_price:,.2f}")
    print(f"5th Percentile Floor: ${cutoff_price:,.2f}")
    print("-" * 40)
    print(f"Value at Risk (95%):  ${VaR:,.2f}")
    print(f"(You are 95% confident you won't lose more than ${VaR:,.2f})")
    print("="*40)

    # --- 5. VISUALIZATION ---
    # We will use a 'subplot' to show both charts in one window
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Chart 1: The Spaghetti
    ax1.plot(stock_paths[:, :50], alpha=0.5, linewidth=0.8)
    ax1.set_title(f"Monte Carlo Paths (First 50/{sims})")
    ax1.set_xlabel("Days")
    ax1.set_ylabel("Price")
    ax1.grid(True)

    # Chart 2: The Histogram
    ax2.hist(final_prices, bins=50, color='skyblue', edgecolor='black')
    ax2.axvline(x=cutoff_price, color='red', linestyle='--', linewidth=2, label=f'Var Cutoff: ${cutoff_price:.2f}')
    ax2.set_title("Distribution of Final Prices")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

# Run the function
if __name__ == "__main__":
    run_simulation()
    