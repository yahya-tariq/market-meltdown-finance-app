import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time # done to add a delay when running 
#introduction tot the app,
st.title("💸 Market Meltdown: Survive The Crash")
st.write("""
Discover how long your finances would survive a market crash. 
This tool helps you understand your financial resilience by simulating historical crisis scenarios.
""")

#the sidebard for user inputs, user enters his details 
st.sidebar.header("📊 Your Financial Profile")
# creatign a function to validate inputs 
def validate_input(value, field_name):
    if value < 0:
        st.sidebar.error(f"{field_name} cannot be negative!")
        return 0
    return value

investment_stocks = validate_input(st.sidebar.number_input("Stocks Investment ($)", min_value=0, value=10000), "Stocks")
investment_crypto = validate_input(st.sidebar.number_input("Crypto Investment ($)", min_value=0, value=5000), "Crypto")
investment_bonds = validate_input(st.sidebar.number_input("Bonds Investment ($)", min_value=0, value=7000), "Bonds")
cash_savings = validate_input(st.sidebar.number_input("Cash Savings ($)", min_value=0, value=3000), "Cash Savings")
monthly_expenses = validate_input(st.sidebar.number_input("Monthly Expenses ($)", min_value=0, value=2000), "Monthly Expenses")

# Crash scenario selection, yahan pe sara defined hai, what to do to assets (factors) when each crash happens
crashes = {
    "2008 Financial Crisis": {"stocks": -50, "crypto": 0, "bonds": 5},
    "COVID-19 Crash": {"stocks": -30, "crypto": -40, "bonds": 10},
    "Dot-com Bubble": {"stocks": -40, "crypto": 0, "bonds": 7},
    "Great Depression": {"stocks": -90, "crypto": 0, "bonds": -10},
    "Crypto Winter": {"stocks": 0, "crypto": -80, "bonds": 0}
}
selected_crash = st.sidebar.selectbox("Select Crisis Scenario", list(crashes.keys()))

# Function for the Simulation
def simulate_crash(stocks, crypto, bonds, cash, expenses, crash_type):
    if expenses <= 0:
        st.error("Monthly expenses must be greater than $0!")
        return None
    
    #applying the crash impacts
    crash = crashes[crash_type]
    new_stocks = stocks * (1 + crash["stocks"]/100)
    new_crypto = crypto * (1 + crash["crypto"]/100)
    new_bonds = bonds * (1 + crash["bonds"]/100)
    
    # Liquidation assumptions (you don't get full value when selling in a crisis)
    liquid_assets = (new_stocks * 0.8) + (new_crypto * 0.7) + (new_bonds * 0.9) + cash
    months_survivable = liquid_assets / expenses
    
    return {
        "months": months_survivable,
        "liquid_assets": liquid_assets,
        "stocks_after": new_stocks,
        "crypto_after": new_crypto,
        "bonds_after": new_bonds,
        "total_before": stocks + crypto + bonds + cash,
        "total_after": new_stocks + new_crypto + new_bonds + cash
    }

# Only running the simulation when the button is clicked
if st.sidebar.button("💥 Run Stress Test"):
    #to give a more game feeling, made a message to show when the button is clicked
    with st.spinner("💣 Detonating financial crisis..."):
        time.sleep(2.5)
        results = simulate_crash(
            investment_stocks, investment_crypto, investment_bonds,
            cash_savings, monthly_expenses, selected_crash)
    
    if results:
        # Display Results only if Resulkts exist
        st.subheader(f"📉 Crisis Impact: {selected_crash}")
        
        # Explanation of calculation
        with st.expander("🔍 How your survival time is calculated", expanded=True):
            st.markdown(f"""
            **Formula:**  
            `(Liquid Assets After Crash) / (Monthly Expenses) = Survival Time`
            
            - **Liquid Assets** = (Stocks x 80%) + (Crypto x 70%) + (Bonds x 90%) + Cash  
              = (${results['stocks_after']:,.0f} x 0.8) + (${results['crypto_after']:,.0f} x 0.7) + (${results['bonds_after']:,.0f} x 0.9) + ${cash_savings:,.0f}  
              = **${results['liquid_assets']:,.0f}**
            
            - **Monthly Expenses** = ${monthly_expenses:,.0f}
            
            - **Survival Time** = ${results['liquid_assets']:,.0f} ÷ ${monthly_expenses:,.0f}  
              = **{results['months']:.1f} months**
            """)
        
        # Created a badge system to give the user a game feeling and defining each badge
        st.subheader("🏆 Your Financial Resilience Rating")
        
        badge_info = {
            "💎 Diamond (24+ months)": {
                "threshold": 24,
                "description": "Exceptional preparedness! You could survive 2+ years without income."
            },
            "🥇 Gold (12-23 months)": {
                "threshold": 12,
                "description": "Strong position. You could survive 1-2 years without income."
            },
            "🥈 Silver (6-11 months)": {
                "threshold": 6,
                "description": "Good preparation. Covers most short-term crises."
            },
            "🥉 Bronze (3-5 months)": {
                "threshold": 3,
                "description": "Basic emergency coverage. Consider building more savings."
            },
            "⚠️ Needs Improvement (<3 months)": {
                "threshold": 0,
                "description": "High risk. Immediate action recommended to build reserves."
            }
        }
        
        earned_badge = None
        for badge, details in badge_info.items():
            if results["months"] >= details["threshold"]:
                earned_badge = (badge, details["description"])
                break
        
        if earned_badge:
            st.success(f"**{earned_badge[0]}**")
            st.write(earned_badge[1])
        #custom celebrations for top performers    
        if "Diamond" in earned_badge[0]:  # Top-tier achievement
            st.balloons()
            st.snow()
        elif "Gold" in earned_badge[0]:    # Excellent performance
            st.balloons()
        # Created a Bar Graph to compre the before and after of each asset when they go thru a crash
        st.subheader("📊 Asset Value Changes")
        
        assets = ["Stocks", "Crypto", "Bonds"]
        before_values = [investment_stocks, investment_crypto, investment_bonds]
        after_values = [results["stocks_after"], results["crypto_after"], results["bonds_after"]]
        
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        x = np.arange(len(assets))
        width = 0.35
        ax1.bar(x - width/2, before_values, width, label="Before Crash", color='#1f77b4')
        ax1.bar(x + width/2, after_values, width, label="After Crash", color='#ff7f0e')
        ax1.set_xticks(x)
        ax1.set_xticklabels(assets)
        ax1.set_ylabel("Value ($)")
        ax1.set_title("Asset Value Before vs After Crash")
        ax1.legend()
        plt.tight_layout()
        st.pyplot(fig1)
        
        # made a line graph to show how funds deplete over time
        st.subheader("⏳ Funds Depletion Timeline")

        months = np.arange(0, int(results["months"]) + 1)
        remaining_funds = [max(results["liquid_assets"] - (month * monthly_expenses), 0) 
                        for month in months]

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        # Main depletion line (green)
        ax2.plot(months, remaining_funds, marker='o', color='#2ca02c', linewidth=2, label='Remaining Funds')
        # Zero balance line (red)
        ax2.axhline(y=0, color='r', linestyle='--', linewidth=1.5, label='Zero Balance')
        ax2.set_xlabel("Months")
        ax2.set_ylabel("Remaining Funds ($)")
        ax2.set_title("How Long Your Funds Will Last")
        ax2.grid(True)
        ax2.legend()  
        plt.tight_layout()
        st.pyplot(fig2)
        
        # created a Pie Chart to show how portfolio is allocated
        st.subheader("🥧 Portfolio Composition")
        
        fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(12, 5))
        labels = ["Stocks", "Crypto", "Bonds", "Cash"]
        
        # Before crash
        sizes_before = [investment_stocks, investment_crypto, investment_bonds, cash_savings]
        ax3a.pie(sizes_before, labels=labels, autopct='%1.1f%%', startangle=90)
        ax3a.set_title("Before Crash")
        
        # After crash
        sizes_after = [results["stocks_after"], results["crypto_after"], 
                      results["bonds_after"], cash_savings]
        ax3b.pie(sizes_after, labels=labels, autopct='%1.1f%%', startangle=90)
        ax3b.set_title("After Crash")
        
        plt.tight_layout()
        st.pyplot(fig3)
        
        # Personalized Recommendations
        st.subheader("📋 Action Plan & Recommendations")
        
        recommendations = []
        
        # Savings recommendations
        if results["months"] < 6:
            recommendations.append(
                f"🚨 **Emergency Fund Boost**: Aim to save ${6*monthly_expenses:,.0f} "
                f"(6 months of expenses). Currently at {results['months']:.1f} months coverage."
            )
        
        # Investment mix analysis
        crypto_percent = investment_crypto / (investment_stocks + investment_crypto + investment_bonds) * 100
        if crypto_percent > 30:
            recommendations.append(
                f"⚖️ **Diversify Investments**: Your crypto allocation is {crypto_percent:.0f}% of investments. "
                "Consider rebalancing to reduce volatility risk."
            )
        
        # Expense management
        if monthly_expenses > cash_savings:
            recommendations.append(
                "💳 **Expense Warning**: Your monthly expenses exceed your cash savings. "
                "Identify areas to reduce spending."
            )
        
        # Display recommendations
        if recommendations:
            for rec in recommendations:
                st.markdown(f"- {rec}")
        else:
            st.success("✅ Your financial position looks strong! Maintain these good habits.")
        
        # A section to show professional tips and how to build financial resilience gotten from google
        st.subheader("💡 Financial Resilience Tips")
        st.markdown("""
        - **3-6-1 Rule**: Maintain 3 months expenses in cash, 6 months in liquid assets, 1 year in investments
        - **Ladder CDs**: Consider certificate of deposits for better interest on emergency funds
        - **Automatic Savings**: Set up automatic transfers to build reserves effortlessly
        - **Expense Audit**: Review subscriptions/services monthly to eliminate unnecessary costs
        """)

# Footer with assumptions
st.markdown("---")
st.caption("""
**Simulation Assumptions**:  
- Stocks liquidate at 80% value, Crypto at 70%, Bonds at 90% during crisis  
- No additional income during simulation period  
- Monthly expenses remain constant  
- Does not account for inflation or taxes  
""")