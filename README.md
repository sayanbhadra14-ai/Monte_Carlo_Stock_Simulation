# Monte Carlo Stock Price Simulator

A Python-based Monte Carlo simulation tool to model possible future stock prices using expected return and volatility.

---

## What This Project Does

This simulator uses random sampling to generate possible future stock prices over time using Geometric Brownian Motion.

You provide:

- Current stock price  
- Expected annual return  
- Annual volatility  
- Time horizon (in years)  
- Number of simulations  

The program then:

- Simulates daily price movements  
- Generates thousands of possible future price paths  
- Calculates risk metrics  
- Plots price path simulations  
- Plots the distribution of final outcomes  

---

## Outputs

The simulation provides:

- Expected future price  
- 5th percentile worst-case scenario  
- 95% Value at Risk (VaR)  
- Visual simulation of price paths  
- Histogram of terminal price distribution  
