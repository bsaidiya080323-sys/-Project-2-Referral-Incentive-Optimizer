
"""
Referral Incentive Optimizer - Core Logic
Determines optimal referral rewards using mathematical optimization.
"""
import numpy as np
import json

class ReferralIncentiveOptimizer:
    """
    Optimizes referral incentive programs by calculating:
    - Optimal reward amounts
    - Expected customer acquisition cost
    - Program ROI
    - Break-even analysis
    """

    def __init__(self):
        self.scenarios = []
        self.optimal_config = None

    def calculate_conversion_probability(self, reward_amount, base_rate=0.05, sensitivity=0.02, saturation=500):
        """
        Calculate probability of referral conversion based on reward amount.
        Uses a logistic/sigmoid model with saturation.

        Args:
            reward_amount: Dollar amount of referral reward
            base_rate: Base conversion rate without reward
            sensitivity: How much reward increases conversion
            saturation: Reward amount where conversion plateaus
        """
        # Logistic function: conversion increases with reward but plateaus
        import math
        prob = base_rate + (1 - base_rate) * (1 / (1 + math.exp(-sensitivity * (reward_amount - saturation/2))))
        return min(prob, 0.95)  # Cap at 95%

    def calculate_customer_lifetime_value(self, avg_order_value, purchase_frequency, customer_lifespan_years, profit_margin=0.3):
        """
        Calculate Customer Lifetime Value (CLV).

        CLV = (Avg Order Value × Purchase Frequency × Profit Margin × Lifespan in years)
        """
        clv = avg_order_value * purchase_frequency * profit_margin * customer_lifespan_years
        return clv

    def optimize_reward(self, clv, min_reward=5, max_reward=200, step=5, 
                       referrer_cost=0, referee_discount=0, program_overhead=0.1):
        """
        Find optimal reward amount that maximizes net profit from referral program.

        Net Profit = (CLV - Reward - Referrer Cost - Referee Discount - Overhead) × Conversions
        """
        best_reward = min_reward
        best_profit = -float('inf')
        results = []

        for reward in range(min_reward, max_reward + step, step):
            # Conversion probability based on reward
            conv_prob = self.calculate_conversion_probability(reward)

            # Assume 1000 customers in the program for calculation
            base_customers = 1000
            expected_conversions = base_customers * conv_prob

            # Costs
            total_reward_cost = expected_conversions * reward
            total_referrer_cost = expected_conversions * referrer_cost
            total_referee_cost = expected_conversions * referee_discount
            total_overhead = (total_reward_cost + total_referrer_cost + total_referee_cost) * program_overhead

            total_cost = total_reward_cost + total_referrer_cost + total_referee_cost + total_overhead

            # Revenue from new customers
            total_revenue = expected_conversions * clv

            # Net profit
            net_profit = total_revenue - total_cost

            # ROI
            roi = (net_profit / total_cost) * 100 if total_cost > 0 else 0

            # Cost per acquisition
            cpa = total_cost / expected_conversions if expected_conversions > 0 else float('inf')

            result = {
                'reward_amount': reward,
                'conversion_probability': round(conv_prob, 4),
                'expected_conversions': round(expected_conversions, 1),
                'total_cost': round(total_cost, 2),
                'total_revenue': round(total_revenue, 2),
                'net_profit': round(net_profit, 2),
                'roi_percent': round(roi, 2),
                'cost_per_acquisition': round(cpa, 2),
                'profit_per_customer': round(net_profit / expected_conversions, 2) if expected_conversions > 0 else 0
            }
            results.append(result)

            if net_profit > best_profit:
                best_profit = net_profit
                best_reward = reward

        self.optimal_config = {
            'optimal_reward': best_reward,
            'max_profit': round(best_profit, 2),
            'all_scenarios': results
        }

        return self.optimal_config

    def compare_incentive_structures(self, clv, structures):
        """
        Compare different incentive structures:
        - Fixed cash reward
        - Percentage discount
        - Tiered rewards
        - Dual-sided (both referrer and referee get reward)
        """
        comparisons = []

        for name, config in structures.items():
            reward = config.get('reward', 20)
            referrer_bonus = config.get('referrer_bonus', 0)
            referee_discount = config.get('referee_discount', 0)

            conv_prob = self.calculate_conversion_probability(reward)
            base_customers = 1000
            expected_conversions = base_customers * conv_prob

            total_cost = expected_conversions * (reward + referrer_bonus + referee_discount)
            total_revenue = expected_conversions * clv
            net_profit = total_revenue - total_cost
            roi = (net_profit / total_cost) * 100 if total_cost > 0 else 0

            comparisons.append({
                'structure': name,
                'reward': reward,
                'referrer_bonus': referrer_bonus,
                'referee_discount': referee_discount,
                'conversion_rate': round(conv_prob * 100, 2),
                'expected_conversions': round(expected_conversions, 1),
                'total_cost': round(total_cost, 2),
                'net_profit': round(net_profit, 2),
                'roi_percent': round(roi, 2)
            })

        return comparisons

    def sensitivity_analysis(self, clv, base_reward, variables=['clv', 'conversion_rate', 'reward_amount']):
        """
        Perform sensitivity analysis to understand how changes affect outcomes.
        """
        analysis = {}

        # Base case
        base_conv = self.calculate_conversion_probability(base_reward)
        base_conversions = 1000 * base_conv
        base_cost = base_conversions * base_reward
        base_revenue = base_conversions * clv
        base_profit = base_revenue - base_cost

        analysis['base_case'] = {
            'clv': clv,
            'reward': base_reward,
            'conversions': round(base_conversions, 1),
            'profit': round(base_profit, 2),
            'roi': round((base_profit / base_cost) * 100, 2) if base_cost > 0 else 0
        }

        # CLV sensitivity (+/- 20%)
        analysis['clv_sensitivity'] = []
        for delta in [-0.2, -0.1, 0, 0.1, 0.2]:
            new_clv = clv * (1 + delta)
            new_revenue = base_conversions * new_clv
            new_profit = new_revenue - base_cost
            analysis['clv_sensitivity'].append({
                'clv_change': f"{delta*100:+.0f}%",
                'clv': round(new_clv, 2),
                'profit': round(new_profit, 2),
                'profit_change': f"{((new_profit - base_profit) / abs(base_profit) * 100):+.1f}%" if base_profit != 0 else "N/A"
            })

        # Conversion rate sensitivity
        analysis['conversion_sensitivity'] = []
        for delta in [-0.2, -0.1, 0, 0.1, 0.2]:
            new_conv = min(base_conv * (1 + delta), 0.95)
            new_conversions = 1000 * new_conv
            new_cost = new_conversions * base_reward
            new_revenue = new_conversions * clv
            new_profit = new_revenue - new_cost
            analysis['conversion_sensitivity'].append({
                'conv_change': f"{delta*100:+.0f}%",
                'conversion_rate': round(new_conv * 100, 2),
                'profit': round(new_profit, 2),
                'profit_change': f"{((new_profit - base_profit) / abs(base_profit) * 100):+.1f}%" if base_profit != 0 else "N/A"
            })

        return analysis

    def generate_recommendations(self, optimal_result, business_type='general'):
        """Generate actionable recommendations based on optimization results."""
        recommendations = []

        reward = optimal_result['optimal_reward']
        profit = optimal_result['max_profit']

        # Find the scenario with optimal reward
        optimal_scenario = None
        for s in optimal_result['all_scenarios']:
            if s['reward_amount'] == reward:
                optimal_scenario = s
                break

        if optimal_scenario is None:
            return recommendations

        recommendations.append(f"💰 OPTIMAL REWARD: ${reward}")
        recommendations.append(f"   This reward maximizes net profit at ${profit:,.2f}")
        recommendations.append(f"   Expected conversion rate: {optimal_scenario['conversion_probability']*100:.1f}%")
        recommendations.append(f"   Cost per acquisition: ${optimal_scenario['cost_per_acquisition']:.2f}")
        recommendations.append("")

        # Business-specific recommendations
        if business_type == 'ecommerce':
            recommendations.append("🛒 E-COMMERCE SPECIFIC:")
            recommendations.append("   - Offer store credit instead of cash (reduces cost by ~30%)")
            recommendations.append("   - Set minimum order value for referral discount")
            recommendations.append("   - Use tiered rewards: $10 for 1st referral, $25 for 3rd, $50 for 5th")
        elif business_type == 'saas':
            recommendations.append("☁️ SAAS SPECIFIC:")
            recommendations.append("   - Offer subscription credits (e.g., 1 month free)")
            recommendations.append("   - Higher rewards for annual plan referrals")
            recommendations.append("   - Consider feature unlocks as non-monetary rewards")
        elif business_type == 'retail':
            recommendations.append("🏪 RETAIL SPECIFIC:")
            recommendations.append("   - Use percentage discounts (10-20% off next purchase)")
            recommendations.append("   - Bundle rewards with loyalty program points")
            recommendations.append("   - Seasonal bonus rewards during holidays")
        else:
            recommendations.append("📋 GENERAL RECOMMENDATIONS:")
            recommendations.append("   - Test A/B with reward amounts around the optimal value")
            recommendations.append("   - Monitor actual conversion rates vs. predicted")
            recommendations.append("   - Adjust quarterly based on performance data")

        recommendations.append("")
        recommendations.append("⚠️ IMPORTANT CONSIDERATIONS:")

        if optimal_scenario['roi_percent'] < 100:
            recommendations.append("   ⚠️ ROI is below 100%. Consider:")
            recommendations.append("      - Increasing customer engagement before launching")
            recommendations.append("      - Reducing program overhead costs")
            recommendations.append("      - Focusing on high-CLV customer segments")
        else:
            recommendations.append("   ✅ Program is profitable. Consider scaling up!")

        if reward > 100:
            recommendations.append("   ⚠️ High reward amount may attract low-quality referrals")
            recommendations.append("      - Add qualification criteria (e.g., referee must make purchase)")

        return recommendations


if __name__ == '__main__':
    optimizer = ReferralIncentiveOptimizer()

    # Example: E-commerce business
    clv = optimizer.calculate_customer_lifetime_value(
        avg_order_value=75,
        purchase_frequency=4,
        customer_lifespan_years=3,
        profit_margin=0.35
    )
    print(f"Customer Lifetime Value: ${clv:.2f}")

    result = optimizer.optimize_reward(clv, min_reward=5, max_reward=150, step=5)
    print(f"\nOptimal Reward: ${result['optimal_reward']}")
    print(f"Maximum Profit: ${result['max_profit']:,.2f}")
