
"""
Referral Incentive Optimizer - Tkinter GUI
Interactive desktop application for optimizing referral rewards.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io
from PIL import Image, ImageTk

from referral_optimizer import ReferralIncentiveOptimizer

class ReferralOptimizerApp:
    """Main GUI application for Referral Incentive Optimizer."""

    def __init__(self, root):
        self.root = root
        self.root.title("🎁 Referral Incentive Optimizer")
        self.root.geometry("1300x850")
        self.root.configure(bg='#f0f2f5')

        self.optimizer = ReferralIncentiveOptimizer()
        self.current_results = None

        # Color scheme
        self.colors = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'bg': '#f0f2f5',
            'card': '#ffffff',
            'text': '#2c3e50'
        }

        self._create_widgets()

    def _create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header = tk.Frame(main_frame, bg=self.colors['card'], bd=2, relief=tk.RIDGE)
        header.pack(fill=tk.X, pady=(0, 20))

        tk.Label(header, text="🎁 Referral Incentive Optimizer", 
                font=('Helvetica', 28, 'bold'), fg=self.colors['primary'], bg=self.colors['card']).pack(pady=10)
        tk.Label(header, text="Determine Optimal Referral Rewards for Maximum Profit", 
                font=('Helvetica', 13), fg='#7f8c8d', bg=self.colors['card']).pack(pady=(0, 10))

        # Content area - split into left (inputs) and right (results)
        content = tk.Frame(main_frame, bg=self.colors['bg'])
        content.pack(fill=tk.BOTH, expand=True)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=2)

        # LEFT PANEL - Inputs
        left_panel = tk.Frame(content, bg=self.colors['card'], bd=2, relief=tk.RIDGE, padx=15, pady=15)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        tk.Label(left_panel, text="📊 Business Parameters", 
                font=('Helvetica', 16, 'bold'), fg=self.colors['text'], bg=self.colors['card']).pack(anchor=tk.W, pady=(0, 15))

        # Input fields
        input_frame = tk.Frame(left_panel, bg=self.colors['card'])
        input_frame.pack(fill=tk.X)

        self.inputs = {}

        fields = [
            ('avg_order_value', 'Average Order Value ($):', '75'),
            ('purchase_frequency', 'Purchases per Year:', '4'),
            ('customer_lifespan', 'Customer Lifespan (years):', '3'),
            ('profit_margin', 'Profit Margin (0-1):', '0.35'),
            ('min_reward', 'Min Reward ($):', '5'),
            ('max_reward', 'Max Reward ($):', '200'),
            ('reward_step', 'Reward Step ($):', '5'),
            ('base_customers', 'Customers in Program:', '1000'),
        ]

        for i, (key, label, default) in enumerate(fields):
            row = tk.Frame(input_frame, bg=self.colors['card'])
            row.pack(fill=tk.X, pady=5)

            tk.Label(row, text=label, font=('Helvetica', 11), 
                    bg=self.colors['card'], fg=self.colors['text'], width=25, anchor='w').pack(side=tk.LEFT)

            var = tk.StringVar(value=default)
            entry = tk.Entry(row, textvariable=var, font=('Helvetica', 11), width=15, 
                           relief=tk.SOLID, bd=1)
            entry.pack(side=tk.RIGHT)
            self.inputs[key] = var

        # Business type
        type_frame = tk.Frame(left_panel, bg=self.colors['card'])
        type_frame.pack(fill=tk.X, pady=10)
        tk.Label(type_frame, text="Business Type:", font=('Helvetica', 11), 
                bg=self.colors['card'], fg=self.colors['text'], width=25, anchor='w').pack(side=tk.LEFT)

        self.business_type = tk.StringVar(value='general')
        ttk.Combobox(type_frame, textvariable=self.business_type, 
                    values=['general', 'ecommerce', 'saas', 'retail'], 
                    state='readonly', width=15).pack(side=tk.RIGHT)

        # Action buttons
        btn_frame = tk.Frame(left_panel, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, pady=20)

        tk.Button(btn_frame, text="🚀 Optimize Reward", font=('Helvetica', 12, 'bold'),
                 bg=self.colors['primary'], fg='white', padx=20, pady=10,
                 command=self._run_optimization, cursor='hand2').pack(fill=tk.X, pady=5)

        tk.Button(btn_frame, text="📊 Compare Structures", font=('Helvetica', 11),
                 bg=self.colors['secondary'], fg='white', padx=15, pady=8,
                 command=self._compare_structures, cursor='hand2').pack(fill=tk.X, pady=5)

        tk.Button(btn_frame, text="📈 Sensitivity Analysis", font=('Helvetica', 11),
                 bg=self.colors['warning'], fg='white', padx=15, pady=8,
                 command=self._sensitivity_analysis, cursor='hand2').pack(fill=tk.X, pady=5)

        # RIGHT PANEL - Results
        right_panel = tk.Frame(content, bg=self.colors['card'], bd=2, relief=tk.RIDGE)
        right_panel.grid(row=0, column=1, sticky='nsew')
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        # Results notebook (tabs)
        self.result_notebook = ttk.Notebook(right_panel)
        self.result_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Optimal Results
        self.results_tab = tk.Frame(self.result_notebook, bg=self.colors['card'])
        self.result_notebook.add(self.results_tab, text="🎯 Optimal Result")

        self.results_text = scrolledtext.ScrolledText(self.results_tab, wrap=tk.WORD,
                                                       font=('Consolas', 11), bg='#fafafa')
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.results_text.insert(tk.END, "Enter business parameters and click 'Optimize Reward' to see results.\n")
        self.results_text.config(state=tk.DISABLED)

        # Tab 2: Chart
        self.chart_tab = tk.Frame(self.result_notebook, bg=self.colors['card'])
        self.result_notebook.add(self.chart_tab, text="📈 Profit Chart")

        self.chart_label = tk.Label(self.chart_tab, text="Chart will appear here after optimization",
                                   font=('Helvetica', 12), bg=self.colors['card'], fg='#7f8c8d')
        self.chart_label.pack(expand=True)

        # Tab 3: Comparison
        self.compare_tab = tk.Frame(self.result_notebook, bg=self.colors['card'])
        self.result_notebook.add(self.compare_tab, text="⚖️ Compare")

        self.compare_text = scrolledtext.ScrolledText(self.compare_tab, wrap=tk.WORD,
                                                      font=('Consolas', 11), bg='#fafafa')
        self.compare_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.compare_text.insert(tk.END, "Click 'Compare Structures' to see different incentive structure comparisons.\n")
        self.compare_text.config(state=tk.DISABLED)

        # Tab 4: Sensitivity
        self.sens_tab = tk.Frame(self.result_notebook, bg=self.colors['card'])
        self.result_notebook.add(self.sens_tab, text="🔍 Sensitivity")

        self.sens_text = scrolledtext.ScrolledText(self.sens_tab, wrap=tk.WORD,
                                                    font=('Consolas', 11), bg='#fafafa')
        self.sens_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.sens_text.insert(tk.END, "Click 'Sensitivity Analysis' to see how changes affect outcomes.\n")
        self.sens_text.config(state=tk.DISABLED)

        # Tab 5: Recommendations
        self.rec_tab = tk.Frame(self.result_notebook, bg=self.colors['card'])
        self.result_notebook.add(self.rec_tab, text="💡 Recommendations")

        self.rec_text = scrolledtext.ScrolledText(self.rec_tab, wrap=tk.WORD,
                                                   font=('Consolas', 11), bg='#fafafa')
        self.rec_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.rec_text.insert(tk.END, "Run optimization to get actionable recommendations.\n")
        self.rec_text.config(state=tk.DISABLED)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                             bg='#e0e0e0', fg='#555', font=('Helvetica', 10),
                             anchor=tk.W, padx=10, pady=5)
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def _get_inputs(self):
        """Get and validate input values."""
        try:
            return {
                'avg_order_value': float(self.inputs['avg_order_value'].get()),
                'purchase_frequency': float(self.inputs['purchase_frequency'].get()),
                'customer_lifespan': float(self.inputs['customer_lifespan'].get()),
                'profit_margin': float(self.inputs['profit_margin'].get()),
                'min_reward': int(self.inputs['min_reward'].get()),
                'max_reward': int(self.inputs['max_reward'].get()),
                'reward_step': int(self.inputs['reward_step'].get()),
                'base_customers': int(self.inputs['base_customers'].get()),
            }
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
            return None

    def _run_optimization(self):
        """Run the reward optimization."""
        params = self._get_inputs()
        if params is None:
            return

        self.status_var.set("Optimizing...")
        self.root.update()

        try:
            # Calculate CLV
            clv = self.optimizer.calculate_customer_lifetime_value(
                avg_order_value=params['avg_order_value'],
                purchase_frequency=params['purchase_frequency'],
                customer_lifespan_years=params['customer_lifespan'],
                profit_margin=params['profit_margin']
            )

            # Run optimization
            result = self.optimizer.optimize_reward(
                clv=clv,
                min_reward=params['min_reward'],
                max_reward=params['max_reward'],
                step=params['reward_step']
            )

            self.current_results = result

            # Update results tab
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)

            self.results_text.insert(tk.END, "🎯 OPTIMIZATION RESULTS\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")

            self.results_text.insert(tk.END, f"💰 Customer Lifetime Value: ${clv:,.2f}\n\n")

            self.results_text.insert(tk.END, f"✅ OPTIMAL REWARD: ${result['optimal_reward']}\n")
            self.results_text.insert(tk.END, f"💵 Maximum Net Profit: ${result['max_profit']:,.2f}\n\n")

            # Find optimal scenario details
            optimal_scenario = None
            for s in result['all_scenarios']:
                if s['reward_amount'] == result['optimal_reward']:
                    optimal_scenario = s
                    break

            if optimal_scenario:
                self.results_text.insert(tk.END, "📊 Optimal Scenario Details:\n")
                self.results_text.insert(tk.END, f"   Conversion Probability: {optimal_scenario['conversion_probability']*100:.1f}%\n")
                self.results_text.insert(tk.END, f"   Expected Conversions: {optimal_scenario['expected_conversions']:.0f}\n")
                self.results_text.insert(tk.END, f"   Total Cost: ${optimal_scenario['total_cost']:,.2f}\n")
                self.results_text.insert(tk.END, f"   Total Revenue: ${optimal_scenario['total_revenue']:,.2f}\n")
                self.results_text.insert(tk.END, f"   ROI: {optimal_scenario['roi_percent']:.1f}%\n")
                self.results_text.insert(tk.END, f"   Cost per Acquisition: ${optimal_scenario['cost_per_acquisition']:.2f}\n")
                self.results_text.insert(tk.END, f"   Profit per Customer: ${optimal_scenario['profit_per_customer']:.2f}\n\n")

            # Top 5 scenarios
            self.results_text.insert(tk.END, "🏆 Top 5 Reward Scenarios:\n")
            self.results_text.insert(tk.END, "-" * 50 + "\n")
            sorted_scenarios = sorted(result['all_scenarios'], key=lambda x: x['net_profit'], reverse=True)[:5]
            for i, s in enumerate(sorted_scenarios, 1):
                marker = "⭐" if s['reward_amount'] == result['optimal_reward'] else "  "
                self.results_text.insert(tk.END, 
                    f"{marker} #{i} Reward ${s['reward_amount']}: "
                    f"Profit ${s['net_profit']:,.2f} | "
                    f"ROI {s['roi_percent']:.1f}% | "
                    f"CPA ${s['cost_per_acquisition']:.2f}\n")

            self.results_text.config(state=tk.DISABLED)

            # Update chart
            self._update_chart(result)

            # Update recommendations
            self._update_recommendations(result, clv)

            self.status_var.set(f"Optimization complete! Optimal reward: ${result['optimal_reward']}")

        except Exception as e:
            messagebox.showerror("Error", f"Optimization failed: {str(e)}")
            self.status_var.set("Optimization failed")

    def _update_chart(self, result):
        """Update the profit chart."""
        # Clear previous chart
        for widget in self.chart_tab.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        scenarios = result['all_scenarios']
        rewards = [s['reward_amount'] for s in scenarios]
        profits = [s['net_profit'] for s in scenarios]
        rois = [s['roi_percent'] for s in scenarios]

        # Profit vs Reward
        ax1.plot(rewards, profits, 'b-', linewidth=2, marker='o', markersize=4)
        ax1.axvline(x=result['optimal_reward'], color='r', linestyle='--', 
                   label=f'Optimal: ${result["optimal_reward"]}')
        ax1.set_xlabel('Reward Amount ($)', fontsize=11)
        ax1.set_ylabel('Net Profit ($)', fontsize=11)
        ax1.set_title('Net Profit vs Reward Amount', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # ROI vs Reward
        ax2.plot(rewards, rois, 'g-', linewidth=2, marker='s', markersize=4)
        ax2.axvline(x=result['optimal_reward'], color='r', linestyle='--',
                   label=f'Optimal: ${result["optimal_reward"]}')
        ax2.set_xlabel('Reward Amount ($)', fontsize=11)
        ax2.set_ylabel('ROI (%)', fontsize=11)
        ax2.set_title('ROI vs Reward Amount', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        plt.close(fig)

    def _compare_structures(self):
        """Compare different incentive structures."""
        params = self._get_inputs()
        if params is None:
            return

        self.status_var.set("Comparing structures...")
        self.root.update()

        try:
            clv = self.optimizer.calculate_customer_lifetime_value(
                avg_order_value=params['avg_order_value'],
                purchase_frequency=params['purchase_frequency'],
                customer_lifespan_years=params['customer_lifespan'],
                profit_margin=params['profit_margin']
            )

            structures = {
                'Fixed Cash ($20)': {'reward': 20, 'referrer_bonus': 0, 'referee_discount': 0},
                'Fixed Cash ($50)': {'reward': 50, 'referrer_bonus': 0, 'referee_discount': 0},
                'Dual-Sided ($15+$10)': {'reward': 15, 'referrer_bonus': 0, 'referee_discount': 10},
                'Dual-Sided ($25+$15)': {'reward': 25, 'referrer_bonus': 0, 'referee_discount': 15},
                'Tiered (Avg $30)': {'reward': 30, 'referrer_bonus': 0, 'referee_discount': 0},
                'High Reward ($75)': {'reward': 75, 'referrer_bonus': 0, 'referee_discount': 0},
            }

            comparisons = self.optimizer.compare_incentive_structures(clv, structures)

            self.compare_text.config(state=tk.NORMAL)
            self.compare_text.delete(1.0, tk.END)

            self.compare_text.insert(tk.END, "⚖️ INCENTIVE STRUCTURE COMPARISON\n")
            self.compare_text.insert(tk.END, "=" * 60 + "\n\n")
            self.compare_text.insert(tk.END, f"Customer Lifetime Value: ${clv:,.2f}\n\n")

            # Find best
            best = max(comparisons, key=lambda x: x['net_profit'])

            for c in comparisons:
                marker = "⭐ BEST" if c == best else ""
                self.compare_text.insert(tk.END, f"📌 {c['structure']} {marker}\n")
                self.compare_text.insert(tk.END, f"   Reward: ${c['reward']}")
                if c['referrer_bonus'] > 0:
                    self.compare_text.insert(tk.END, f" + Referrer Bonus: ${c['referrer_bonus']}")
                if c['referee_discount'] > 0:
                    self.compare_text.insert(tk.END, f" + Referee Discount: ${c['referee_discount']}")
                self.compare_text.insert(tk.END, "\n")
                self.compare_text.insert(tk.END, f"   Conversion Rate: {c['conversion_rate']:.1f}%\n")
                self.compare_text.insert(tk.END, f"   Expected Conversions: {c['expected_conversions']:.0f}\n")
                self.compare_text.insert(tk.END, f"   Total Cost: ${c['total_cost']:,.2f}\n")
                self.compare_text.insert(tk.END, f"   Net Profit: ${c['net_profit']:,.2f}\n")
                self.compare_text.insert(tk.END, f"   ROI: {c['roi_percent']:.1f}%\n\n")

            self.compare_text.config(state=tk.DISABLED)
            self.status_var.set("Structure comparison complete")

            # Switch to comparison tab
            self.result_notebook.select(self.compare_tab)

        except Exception as e:
            messagebox.showerror("Error", f"Comparison failed: {str(e)}")
            self.status_var.set("Comparison failed")

    def _sensitivity_analysis(self):
        """Run sensitivity analysis."""
        params = self._get_inputs()
        if params is None:
            return

        self.status_var.set("Running sensitivity analysis...")
        self.root.update()

        try:
            clv = self.optimizer.calculate_customer_lifetime_value(
                avg_order_value=params['avg_order_value'],
                purchase_frequency=params['purchase_frequency'],
                customer_lifespan_years=params['customer_lifespan'],
                profit_margin=params['profit_margin']
            )

            # Use current optimal reward or default
            base_reward = self.current_results['optimal_reward'] if self.current_results else 25

            analysis = self.optimizer.sensitivity_analysis(clv, base_reward)

            self.sens_text.config(state=tk.NORMAL)
            self.sens_text.delete(1.0, tk.END)

            self.sens_text.insert(tk.END, "🔍 SENSITIVITY ANALYSIS\n")
            self.sens_text.insert(tk.END, "=" * 60 + "\n\n")

            # Base case
            base = analysis['base_case']
            self.sens_text.insert(tk.END, "📊 BASE CASE\n")
            self.sens_text.insert(tk.END, f"   CLV: ${base['clv']:,.2f}\n")
            self.sens_text.insert(tk.END, f"   Reward: ${base['reward']}\n")
            self.sens_text.insert(tk.END, f"   Conversions: {base['conversions']}\n")
            self.sens_text.insert(tk.END, f"   Profit: ${base['profit']:,.2f}\n")
            self.sens_text.insert(tk.END, f"   ROI: {base['roi']:.1f}%\n\n")

            # CLV sensitivity
            self.sens_text.insert(tk.END, "📈 CLV SENSITIVITY\n")
            self.sens_text.insert(tk.END, "-" * 40 + "\n")
            for item in analysis['clv_sensitivity']:
                self.sens_text.insert(tk.END, 
                    f"   {item['clv_change']:>6} CLV: ${item['clv']:>10,.2f} | "
                    f"Profit: ${item['profit']:>12,.2f} | "
                    f"Change: {item['profit_change']}\n")

            self.sens_text.insert(tk.END, "\n📉 CONVERSION RATE SENSITIVITY\n")
            self.sens_text.insert(tk.END, "-" * 40 + "\n")
            for item in analysis['conversion_sensitivity']:
                self.sens_text.insert(tk.END, 
                    f"   {item['conv_change']:>6} Conv: {item['conversion_rate']:>6.2f}% | "
                    f"Profit: ${item['profit']:>12,.2f} | "
                    f"Change: {item['profit_change']}\n")

            self.sens_text.config(state=tk.DISABLED)
            self.status_var.set("Sensitivity analysis complete")

            # Switch to sensitivity tab
            self.result_notebook.select(self.sens_tab)

        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            self.status_var.set("Analysis failed")

    def _update_recommendations(self, result, clv):
        """Update recommendations tab."""
        recommendations = self.optimizer.generate_recommendations(
            result, self.business_type.get()
        )

        self.rec_text.config(state=tk.NORMAL)
        self.rec_text.delete(1.0, tk.END)

        self.rec_text.insert(tk.END, "💡 ACTIONABLE RECOMMENDATIONS\n")
        self.rec_text.insert(tk.END, "=" * 60 + "\n\n")

        for rec in recommendations:
            self.rec_text.insert(tk.END, rec + "\n")

        self.rec_text.config(state=tk.DISABLED)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = ReferralOptimizerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
