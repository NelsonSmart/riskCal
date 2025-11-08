import sys

def calculate_position_size(entry_price, stop_loss_price, trading_amount, order_type):
    """
    Calculate position size and risk metrics for crypto trading
    
    Parameters:
    entry_price (float): Entry price of the trade
    stop_loss_price (float): Stop loss price
    trading_amount (float): Amount of capital to use for trading
    order_type (str): 'buy' for long, 'sell' for short
    
    Returns:
    dict: Dictionary containing all calculated metrics
    """
    
    # Validate inputs
    if entry_price <= 0 or stop_loss_price <= 0 or trading_amount <= 0:
        raise ValueError("All price and amount values must be positive")
    
    if order_type.lower() not in ['buy', 'sell']:
        raise ValueError("Order type must be 'buy' or 'sell'")
    
    # Calculate stop loss percentage
    if order_type.lower() == 'sell':  # Short position
        stop_loss_percentage = ((stop_loss_price - entry_price) / entry_price) * 100
    else:  # Long position
        stop_loss_percentage = ((entry_price - stop_loss_price) / entry_price) * 100
    
    # Calculate risk factor
    risk_factor = abs(stop_loss_percentage) / 100
    
    # Calculate order value (position size)
    if risk_factor > 0:
        order_value = trading_amount / risk_factor
    else:
        order_value = 0
    
    # Calculate position size in units
    position_size = order_value / entry_price
    
    # Calculate risk amount (potential loss)
    risk_amount = order_value * risk_factor
    
    # Return all calculated metrics
    return {
        'stop_loss_percentage': round(stop_loss_percentage, 4),
        'risk_factor': round(risk_factor, 6),
        'order_value': round(order_value, 2),
        'position_size': round(position_size, 6),
        'risk_amount': round(risk_amount, 2),
        'risk_reward_ratio': f"1:{round(1/risk_factor, 2)}" if risk_factor > 0 else "N/A"
    }

def main():
    """
    Main function to interact with user and display results
    """
    print("=== Crypto Risk Management Calculator ===")
    print()
    
    try:
        # Get user inputs
        entry_price = float(input("Enter entry price: "))
        stop_loss_price = float(input("Enter stop loss price: "))
        trading_amount = float(input("Enter amount to use for trading: "))
        order_type = input("Enter order type (buy/short): ").strip().lower()
        
        # Handle 'short' as synonym for 'sell'
        if order_type == 'short':
            order_type = 'sell'
        
        # Validate stop loss logic
        if order_type == 'buy' and stop_loss_price >= entry_price:
            print("Warning: For long positions, stop loss should be below entry price")
            sys.exit(1) 
        
        if order_type == 'sell' and stop_loss_price <= entry_price:
            print("Warning: For short positions, stop loss should be above entry price")
            sys.exit(1) 
        
        # Calculate position metrics
        results = calculate_position_size(entry_price, stop_loss_price, trading_amount, order_type)
        
        # Display results
        print("\n" + "="*50)
        print("RISK MANAGEMENT ANALYSIS RESULTS")
        print("="*50)
        print(f"Order Type: {'LONG' if order_type == 'buy' else 'SHORT'}")
        print(f"Entry Price: ${entry_price:.4f}")
        print(f"Stop Loss Price: ${stop_loss_price:.4f}")
        print(f"Trading Capital: ${trading_amount:.2f}")
        print(f"Stop Loss Percentage: {results['stop_loss_percentage']:.4f}%")
        print(f"Risk Factor: {results['risk_factor']:.6f}")
        print(f"Recommended Order Value: ${results['order_value']:.2f}")
        print(f"Position Size: {results['position_size']:.6f} units")
        print(f"Potential Loss: ${results['risk_amount']:.2f}")
        print(f"Risk-Reward Ratio: {results['risk_reward_ratio']}")
        print("="*50)
        
        # Additional risk warnings
        risk_percentage = (results['risk_amount'] / trading_amount) * 100
        print(f"\nRisk Analysis:")
        print(f"Potential loss represents {risk_percentage:.1f}% of your trading capital")
        
        if risk_percentage > 5:
            print("⚠️  WARNING: High risk exposure! Consider reducing position size.")
        elif risk_percentage > 2:
            print("⚠️  Moderate risk level.")
        else:
            print("✅ Conservative risk level.")
            
    except ValueError as e:
        print(f"Input error: {e}")
    except ZeroDivisionError:
        print("Error: Entry price cannot be zero")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Example usage
if __name__ == "__main__":
    main()
    
   