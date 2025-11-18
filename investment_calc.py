import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Test if imports work
print("Python version:", sys.version)
print("Tkinter imported successfully!")

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    print("Matplotlib imported successfully!")
except ImportError as e:
    print("ERROR: Matplotlib not found!")
    print("Please install it with: pip install matplotlib")
    input("Press Enter to exit...")
    sys.exit(1)

try:
    import numpy as np
    print("Numpy imported successfully!")
except ImportError as e:
    print("ERROR: Numpy not found!")
    print("Please install it with: pip install numpy")
    input("Press Enter to exit...")
    sys.exit(1)

print("\nAll imports successful! Starting application...\n")

class InvestmentCalculator:
    def __init__(self, root):
        print("  -> Setting up window properties...")
        self.root = root
        self.root.title("Investment Strategy Calculator - Path to Financial Freedom")
        self.root.geometry("1400x900")
        
        print("  -> Defining color scheme...")
        # Dark theme colors
        self.bg_dark = "#1a1a2e"
        self.bg_medium = "#16213e"
        self.bg_light = "#0f3460"
        self.accent_green = "#00ff88"
        self.accent_blue = "#00d4ff"
        self.accent_gold = "#ffd700"
        self.text_color = "#e4e4e4"
        self.text_dim = "#a0a0a0"
        
        self.root.configure(bg=self.bg_dark)
        
        print("  -> Configuring styles...")
        # Configure dark theme style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors for all widgets
        self.style.configure('TFrame', background=self.bg_dark)
        self.style.configure('TLabelframe', background=self.bg_dark, foreground=self.text_color, bordercolor=self.accent_blue, relief='flat')
        self.style.configure('TLabelframe.Label', background=self.bg_dark, foreground=self.accent_green, font=('Arial', 11, 'bold'))
        self.style.configure('TLabel', background=self.bg_dark, foreground=self.text_color, font=('Arial', 10))
        self.style.configure('TCheckbutton', background=self.bg_dark, foreground=self.text_color, font=('Arial', 10))
        self.style.map('TCheckbutton', background=[('active', self.bg_dark)])
        
        self.style.configure('TButton', 
                           background=self.accent_green, 
                           foreground=self.bg_dark,
                           borderwidth=0,
                           font=('Arial', 11, 'bold'),
                           padding=10)
        self.style.map('TButton',
                      background=[('active', self.accent_blue), ('pressed', '#00cc70')])
        
        self.style.configure('TEntry', 
                           fieldbackground=self.bg_light,
                           foreground=self.text_color,
                           bordercolor=self.accent_blue,
                           insertcolor=self.accent_green)
        
        self.style.configure('Horizontal.TScale',
                           background=self.bg_dark,
                           troughcolor=self.bg_light,
                           bordercolor=self.accent_blue,
                           lightcolor=self.accent_green,
                           darkcolor=self.accent_green)
        
        print("  -> Setting up tooltips...")
        # Tooltips dictionary with detailed explanations
        self.tooltips = {
            "monthly": (
                "Monthly Contribution\n\n"
                "This is how much money you plan to invest each month.\n\n"
                "TIP: Even $30/month can grow into $44,000+ over 30 years!\n"
                "Start with what you can afford, even if it's just $10-20.\n\n"
                "EXAMPLE: If you set $50/month, that's $600/year going into\n"
                "your investments automatically."
            ),
            "increase": (
                "Annual Increase\n\n"
                "Each year, your monthly contribution increases by this percentage.\n"
                "This models your growing income over time.\n\n"
                "TIP: As your career progresses, your income usually grows.\n"
                "A 5% increase means if you start at $30/month, next year\n"
                "you'll invest $31.50/month, then $33.08, and so on.\n\n"
                "EXAMPLE: 5% annual increase = small raises or side hustle growth\n"
                "Set to 0% if you want to keep contributions constant."
            ),
            "years": (
                "Investment Period\n\n"
                "How many years you'll keep investing before needing the money.\n\n"
                "TIP: The longer you invest, the more compound growth works\n"
                "its magic! Time is your biggest advantage.\n\n"
                "EXAMPLE:\n"
                "- 10 years = Good for medium-term goals\n"
                "- 20-30 years = Ideal for retirement/financial independence\n"
                "- 40 years = Maximum wealth building potential"
            ),
            "initial": (
                "Initial Investment\n\n"
                "Any lump sum you're starting with right now (can be $0).\n\n"
                "TIP: Don't worry if you're starting from zero! Most people do.\n"
                "Monthly contributions are what really matter long-term.\n\n"
                "EXAMPLE: If you have $500 saved up, put it here.\n"
                "If you're starting fresh, just leave it at $0."
            ),
            "withdrawal": (
                "Safe Withdrawal Rate\n\n"
                "The percentage of your portfolio you can withdraw yearly\n"
                "without running out of money. This determines your passive income.\n\n"
                "TIP: The '4% rule' is considered safe by financial experts.\n"
                "It means your money should last 30+ years while still growing.\n\n"
                "EXAMPLE: With $100,000 portfolio and 4% withdrawal:\n"
                "- Annual income: $4,000\n"
                "- Monthly income: $333\n\n"
                "Lower = safer, Higher = riskier"
            )
        }
        
        print("  -> Setting up investment strategies...")
        # Investment strategy variables
        self.strategies = {
            'High-Yield Savings': tk.BooleanVar(value=True),
            'Roth IRA': tk.BooleanVar(value=True),
            'Index Funds (S&P500)': tk.BooleanVar(value=True),
            'Robo-Advisor': tk.BooleanVar(),
            'Round-Up Apps': tk.BooleanVar(),
            'Certificates of Deposit': tk.BooleanVar(),
            'Treasury Bonds': tk.BooleanVar(),
            'Crypto (High Risk)': tk.BooleanVar(),
            'Real Estate Crowdfund': tk.BooleanVar()
        }
        
        # Return rates for each strategy (annual %)
        self.return_rates = {
            'High-Yield Savings': 4.5,
            'Roth IRA': 8.0,
            'Index Funds (S&P500)': 8.0,
            'Robo-Advisor': 7.5,
            'Round-Up Apps': 7.5,
            'Certificates of Deposit': 5.0,
            'Treasury Bonds': 4.0,
            'Crypto (High Risk)': 15.0,
            'Real Estate Crowdfund': 9.0
        }
        
        # Risk levels
        self.risk_levels = {
            'High-Yield Savings': 'Very Low',
            'Roth IRA': 'Medium',
            'Index Funds (S&P500)': 'Medium',
            'Robo-Advisor': 'Medium',
            'Round-Up Apps': 'Medium',
            'Certificates of Deposit': 'Very Low',
            'Treasury Bonds': 'Very Low',
            'Crypto (High Risk)': 'Very High',
            'Real Estate Crowdfund': 'Medium-High'
        }
        
        # Strategy tooltips
        self.strategy_tooltips = {
            'High-Yield Savings': (
                "HIGH-YIELD SAVINGS ACCOUNT (HYSA)\n\n"
                "WHAT IT IS: A savings account that pays 4-5% interest annually.\n"
                "Much better than regular savings accounts (0.01%).\n\n"
                "BEST FOR:\n"
                "- Emergency fund (always accessible)\n"
                "- Short-term savings goals\n"
                "- Money you might need soon\n\n"
                "PROS: Safe, FDIC insured, easy to access\n"
                "CONS: Lower returns than investing in stocks\n\n"
                "START HERE: Build 3-6 months of expenses first!"
            ),
            'Roth IRA': (
                "ROTH IRA (U.S. ONLY)\n\n"
                "WHAT IT IS: Special retirement account where profits grow\n"
                "TAX-FREE forever!\n\n"
                "HOW IT WORKS:\n"
                "- Contribute money you've already paid taxes on\n"
                "- It grows for decades\n"
                "- Withdraw in retirement with ZERO taxes!\n\n"
                "REQUIREMENTS: Must have earned income\n"
                "2024 limit: $7,000/year ($583/month max)\n\n"
                "POWER MOVE: This is one of the best wealth-building\n"
                "tools available. Start ASAP if you qualify!"
            ),
            'Index Funds (S&P500)': (
                "INDEX FUNDS (S&P 500)\n\n"
                "WHAT IT IS: A 'basket' of the 500 biggest U.S. companies.\n"
                "One investment = owns pieces of Apple, Microsoft, Amazon, etc.\n\n"
                "HISTORICAL RETURNS: ~8-10% per year average (since 1926)\n\n"
                "WHY IT'S AMAZING:\n"
                "- Super diversified (not all eggs in one basket)\n"
                "- Very low fees (0.03-0.1% per year)\n"
                "- Passive - no stock picking needed\n"
                "- Warren Buffett recommends this!\n\n"
                "BEGINNER TIP: This is the 'set and forget' strategy.\n"
                "Just invest monthly and don't check it constantly."
            ),
            'Robo-Advisor': (
                "ROBO-ADVISOR\n\n"
                "WHAT IT IS: Apps that invest your money automatically\n"
                "using algorithms. No thinking required!\n\n"
                "POPULAR OPTIONS:\n"
                "- Betterment\n"
                "- Wealthfront\n"
                "- SoFi Automated Investing\n\n"
                "WHAT THEY DO:\n"
                "- Ask about your goals and risk tolerance\n"
                "- Build a diversified portfolio for you\n"
                "- Auto-rebalance to keep you on track\n"
                "- Tax-loss harvesting (saves you money)\n\n"
                "FEES: Usually 0.25% per year\n\n"
                "PERFECT IF: You want 100% hands-off investing"
            ),
            'Round-Up Apps': (
                "ROUND-UP INVESTING APPS\n\n"
                "WHAT IT IS: Apps that round up your purchases and\n"
                "invest the spare change automatically.\n\n"
                "HOW IT WORKS:\n"
                "- Buy coffee for $3.60 -> App rounds to $4.00\n"
                "- The $0.40 gets invested automatically\n"
                "- Happens with every purchase!\n\n"
                "POPULAR APPS:\n"
                "- Acorns ($3-5/month)\n"
                "- Robinhood (free round-ups)\n"
                "- Chime (with their account)\n\n"
                "SECRET POWER: You don't 'feel' the money leaving,\n"
                "but you can easily add $50-100/month extra!"
            ),
            'Certificates of Deposit': (
                "CERTIFICATES OF DEPOSIT (CDs)\n\n"
                "WHAT IT IS: You lock money away for 6 months to 5 years\n"
                "and earn a guaranteed interest rate.\n\n"
                "HOW IT WORKS:\n"
                "- Put in $1,000 for 1 year at 5% APY\n"
                "- After 1 year, get back $1,050\n"
                "- Guaranteed - no risk!\n\n"
                "PROS:\n"
                "- Safe (FDIC insured)\n"
                "- Better rates than savings accounts\n"
                "- Predictable returns\n\n"
                "CONS:\n"
                "- Money is locked (penalty for early withdrawal)\n"
                "- Lower returns than stocks long-term\n\n"
                "GOOD FOR: Money you won't need for a while"
            ),
            'Treasury Bonds': (
                "U.S. TREASURY BONDS / I-BONDS\n\n"
                "WHAT IT IS: You loan money to the U.S. government,\n"
                "they pay you interest. Safest investment possible!\n\n"
                "TYPES:\n"
                "- I-Bonds: Adjust for inflation, lock for 1 year\n"
                "- T-Bills: Short term (4 weeks to 1 year)\n"
                "- T-Bonds: Long term (10-30 years)\n\n"
                "CURRENT RATES: ~4-5% depending on type\n\n"
                "PROS:\n"
                "- Safest investment on Earth\n"
                "- Tax advantages (no state/local tax)\n"
                "- Inflation protection (I-Bonds)\n\n"
                "PERFECT FOR: Ultra-safe portion of portfolio"
            ),
            'Crypto (High Risk)': (
                "CRYPTOCURRENCY (HIGH RISK!)\n\n"
                "WHAT IT IS: Digital currencies like Bitcoin (BTC) and\n"
                "Ethereum (ETH). Very volatile!\n\n"
                "POTENTIAL RETURNS: 15%+ average (but huge swings!)\n\n"
                "WARNING: Can drop 50-80% in a year, then\n"
                "recover and gain 200%. Not for the faint of heart!\n\n"
                "SAFE-ISH APPROACH:\n"
                "- Only invest 5-10% of your portfolio\n"
                "- Stick to major coins (BTC, ETH)\n"
                "- Auto-invest small amounts monthly\n"
                "- Never invest money you need soon\n\n"
                "RULE #1: Only invest what you can afford to LOSE!\n"
                "Crypto is speculative. Treat it as 'high risk, high reward'."
            ),
            'Real Estate Crowdfund': (
                "REAL ESTATE CROWDFUNDING\n\n"
                "WHAT IT IS: Pool money with other investors to buy\n"
                "real estate without buying a whole property yourself.\n\n"
                "PLATFORMS:\n"
                "- Fundrise (minimum $10)\n"
                "- RealtyMogul\n"
                "- DiversyFund\n\n"
                "HOW IT WORKS:\n"
                "- You invest small amounts ($10-1000)\n"
                "- Platform buys apartments, commercial buildings, etc.\n"
                "- You earn dividends from rent income\n"
                "- Property value (hopefully) appreciates\n\n"
                "TYPICAL RETURNS: 8-12% per year\n\n"
                "TIP: This lets you invest in real estate with\n"
                "pocket change instead of $100K+ down payments!"
            )
        }
        
        print("  -> Creating widgets...")
        self.create_widgets()
        print("  -> Setup complete!")
    
    def create_tooltip(self, widget, text):
        """Create a tooltip that shows on hover"""
        def on_enter(event):
            # Create tooltip window
            self.tooltip = tk.Toplevel()
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{event.x_root+15}+{event.y_root+10}")
            
            # Create styled frame
            frame = tk.Frame(self.tooltip, 
                           bg=self.bg_medium, 
                           relief='solid', 
                           borderwidth=2,
                           highlightbackground=self.accent_blue,
                           highlightthickness=1)
            frame.pack()
            
            # Add text
            label = tk.Label(frame, 
                           text=text,
                           justify='left',
                           font=('Arial', 9),
                           bg=self.bg_medium,
                           fg=self.text_color,
                           padx=12,
                           pady=10,
                           wraplength=400)
            label.pack()
        
        def on_leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                delattr(self, 'tooltip')
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
        
    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg=self.bg_medium, height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(header, 
                              text="WEALTH BUILDER PRO", 
                              font=('Arial', 24, 'bold'),
                              bg=self.bg_medium,
                              fg=self.accent_green)
        title_label.pack(pady=10)
        
        subtitle = tk.Label(header,
                          text="Your Journey to Financial Independence Starts Here",
                          font=('Arial', 11, 'italic'),
                          bg=self.bg_medium,
                          fg=self.text_dim)
        subtitle.pack()
        
        # Create main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left panel for inputs
        left_frame = ttk.LabelFrame(main_frame, text="INVESTMENT CONFIGURATION", padding=15)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        
        # Right panel for results
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        
        main_frame.columnconfigure(0, weight=1, minsize=450)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)
        
        # === LEFT PANEL ===
        
        # Input section with custom styled entries
        inputs = [
            ("Monthly Contribution ($):", "30", "monthly_var", "monthly"),
            ("Annual Increase (%):", "5", "increase_var", "increase"),
            ("Investment Period (years):", "30", "years_var", "years"),
            ("Initial Investment ($):", "0", "initial_var", "initial"),
            ("Safe Withdrawal Rate (%):", "4", "withdrawal_var", "withdrawal")
        ]
        
        for i, (label_text, default, var_name, tooltip_key) in enumerate(inputs):
            # Label with icon
            label = tk.Label(left_frame, 
                           text=label_text,
                           font=('Arial', 10, 'bold'),
                           bg=self.bg_dark,
                           fg=self.accent_blue,
                           anchor='w',
                           cursor='question_arrow')
            label.grid(row=i, column=0, sticky='w', pady=8, padx=(0, 10))
            
            # Bind tooltip
            self.create_tooltip(label, self.tooltips[tooltip_key])
            
            # Entry with dark theme
            var = tk.StringVar(value=default)
            setattr(self, var_name, var)
            entry = tk.Entry(left_frame, 
                           textvariable=var,
                           width=12,
                           font=('Arial', 11, 'bold'),
                           bg=self.bg_light,
                           fg=self.text_color,
                           insertbackground=self.accent_green,
                           relief='flat',
                           borderwidth=2,
                           highlightthickness=2,
                           highlightbackground=self.accent_blue,
                           highlightcolor=self.accent_green)
            entry.grid(row=i, column=1, sticky='ew', pady=8)
            
            # Add tooltip to entry too
            self.create_tooltip(entry, self.tooltips[tooltip_key])
        
        # Separator with style
        separator = tk.Frame(left_frame, height=2, bg=self.accent_blue)
        separator.grid(row=len(inputs), column=0, columnspan=2, sticky='ew', pady=15)
        
        # Strategy section header
        strategy_header = tk.Label(left_frame,
                                  text="SELECT YOUR INVESTMENT STRATEGIES",
                                  font=('Arial', 12, 'bold'),
                                  bg=self.bg_dark,
                                  fg=self.accent_gold)
        strategy_header.grid(row=len(inputs)+1, column=0, columnspan=2, sticky='w', pady=(10, 15))
        
        # Create scrollable frame for strategies
        canvas = tk.Canvas(left_frame, bg=self.bg_dark, highlightthickness=0, height=320)
        scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_dark)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=len(inputs)+2, column=0, columnspan=2, sticky='nsew', pady=5)
        scrollbar.grid(row=len(inputs)+2, column=2, sticky='ns', pady=5)
        
        # Strategy checkboxes with allocation sliders
        self.allocation_sliders = {}
        self.allocation_labels = {}
        
        for i, (strategy, var) in enumerate(self.strategies.items()):
            # Strategy container
            strategy_frame = tk.Frame(scrollable_frame, bg=self.bg_medium, relief='flat', bd=1)
            strategy_frame.pack(fill='x', pady=5, padx=2)
            
            # Checkbox with custom colors
            cb = tk.Checkbutton(strategy_frame,
                              text=strategy,
                              variable=var,
                              command=self.update_allocations,
                              font=('Arial', 10, 'bold'),
                              bg=self.bg_medium,
                              fg=self.text_color,
                              selectcolor=self.bg_light,
                              activebackground=self.bg_medium,
                              activeforeground=self.accent_green,
                              bd=0,
                              highlightthickness=0,
                              cursor='hand2')
            cb.pack(anchor='w', padx=10, pady=(8, 2))
            
            # Add tooltip to strategy
            self.create_tooltip(strategy_frame, self.strategy_tooltips[strategy])
            
            # Risk and return info
            info_frame = tk.Frame(strategy_frame, bg=self.bg_medium)
            info_frame.pack(fill='x', padx=10, pady=(0, 5))
            
            risk_label = tk.Label(info_frame,
                                text=f"Risk: {self.risk_levels[strategy]}",
                                font=('Arial', 8),
                                bg=self.bg_medium,
                                fg=self.text_dim)
            risk_label.pack(side='left')
            
            return_label = tk.Label(info_frame,
                                  text=f"Return: {self.return_rates[strategy]}%",
                                  font=('Arial', 8),
                                  bg=self.bg_medium,
                                  fg=self.accent_green)
            return_label.pack(side='right')
            
            # Allocation slider with percentage
            slider_container = tk.Frame(strategy_frame, bg=self.bg_medium)
            slider_container.pack(fill='x', padx=10, pady=(0, 8))
            
            slider = tk.Scale(slider_container,
                            from_=0, to=100,
                            orient='horizontal',
                            bg=self.bg_medium,
                            fg=self.text_color,
                            troughcolor=self.bg_light,
                            activebackground=self.accent_green,
                            highlightthickness=0,
                            sliderlength=20,
                            width=12,
                            showvalue=False)
            slider.set(33 if i < 3 else 0)
            slider.pack(side='left', fill='x', expand=True, padx=(0, 10))
            
            pct_label = tk.Label(slider_container,
                               text="33%",
                               font=('Arial', 10, 'bold'),
                               bg=self.bg_medium,
                               fg=self.accent_gold,
                               width=5)
            pct_label.pack(side='left')
            
            self.allocation_sliders[strategy] = slider
            self.allocation_labels[strategy] = pct_label
            
            slider.config(command=lambda v, lbl=pct_label: lbl.config(text=f"{int(float(v))}%"))
        
        left_frame.rowconfigure(len(inputs)+2, weight=1)
        
        # Calculate button with glow effect
        button_frame = tk.Frame(left_frame, bg=self.bg_dark)
        button_frame.grid(row=len(inputs)+3, column=0, columnspan=2, pady=20, sticky='ew')
        
        calc_button = tk.Button(button_frame,
                               text="CALCULATE MY WEALTH PATH",
                               command=self.calculate,
                               font=('Arial', 13, 'bold'),
                               bg=self.accent_green,
                               fg=self.bg_dark,
                               activebackground=self.accent_blue,
                               activeforeground='white',
                               relief='flat',
                               bd=0,
                               padx=20,
                               pady=12,
                               cursor='hand2')
        calc_button.pack(fill='x')
        
        # === RIGHT PANEL ===
        
        # Results section
        results_frame = ttk.LabelFrame(right_frame, text="RESULTS & PROJECTIONS", padding=12)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Custom text widget with dark theme
        text_frame = tk.Frame(results_frame, bg=self.bg_light, relief='flat', bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(text_frame,
                                   wrap=tk.WORD,
                                   font=('Consolas', 9),
                                   bg=self.bg_light,
                                   fg=self.text_color,
                                   insertbackground=self.accent_green,
                                   selectbackground=self.accent_blue,
                                   selectforeground='white',
                                   relief='flat',
                                   padx=10,
                                   pady=10)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=self.results_text.yview, bg=self.bg_dark)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        # Configure text tags for colored output
        self.results_text.tag_configure('header', foreground=self.accent_green, font=('Consolas', 10, 'bold'))
        self.results_text.tag_configure('subheader', foreground=self.accent_blue, font=('Consolas', 9, 'bold'))
        self.results_text.tag_configure('highlight', foreground=self.accent_gold, font=('Consolas', 9, 'bold'))
        self.results_text.tag_configure('success', foreground=self.accent_green)
        
        # Graph section
        self.graph_frame = ttk.LabelFrame(right_frame, text="WEALTH VISUALIZATION", padding=12)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)
        
    def update_allocations(self):
        """Update allocation display"""
        pass
        
    def calculate(self):
        try:
            monthly = float(self.monthly_var.get())
            annual_increase = float(self.increase_var.get()) / 100
            years = int(self.years_var.get())
            initial = float(self.initial_var.get())
            withdrawal_rate = float(self.withdrawal_var.get()) / 100
            
            selected_strategies = []
            allocations = []
            
            for strategy, var in self.strategies.items():
                if var.get():
                    allocation = self.allocation_sliders[strategy].get()
                    if allocation > 0:
                        selected_strategies.append(strategy)
                        allocations.append(allocation)
            
            if not selected_strategies:
                messagebox.showwarning("No Strategies", "Please select at least one investment strategy!")
                return
            
            total_allocation = sum(allocations)
            if total_allocation == 0:
                messagebox.showwarning("Zero Allocation", "Please set allocation percentages!")
                return
                
            allocations = [a / total_allocation for a in allocations]
            
            weighted_return = sum(self.return_rates[s] * a for s, a in zip(selected_strategies, allocations))
            monthly_rate = weighted_return / 100 / 12
            
            months = years * 12
            portfolio_values = [initial]
            contributions_total = [0]
            monthly_contribution = monthly
            
            for month in range(1, months + 1):
                if month % 12 == 0:
                    monthly_contribution *= (1 + annual_increase)
                
                previous_value = portfolio_values[-1]
                new_value = previous_value * (1 + monthly_rate) + monthly_contribution
                portfolio_values.append(new_value)
                contributions_total.append(contributions_total[-1] + monthly_contribution)
            
            final_value = portfolio_values[-1]
            total_contributed = contributions_total[-1] + initial
            total_gains = final_value - total_contributed
            annual_income = final_value * withdrawal_rate
            monthly_income = annual_income / 12
            
            # Display results with colored tags
            self.results_text.delete(1.0, tk.END)
            
            self.insert_colored(f"\n{'='*70}\n", 'header')
            self.insert_colored(f"  YOUR PATH TO FINANCIAL FREEDOM - {years} YEAR PROJECTION\n", 'header')
            self.insert_colored(f"{'='*70}\n\n", 'header')
            
            self.insert_colored("IMPORTANT NOTE:\n", 'highlight')
            self.results_text.insert(tk.END, "These projections assume all dividends and gains are REINVESTED\n")
            self.results_text.insert(tk.END, "automatically. This is the power of compound growth!\n\n")
            
            self.insert_colored("INVESTMENT CONFIGURATION\n", 'subheader')
            self.insert_colored("-" * 70 + "\n", 'subheader')
            self.results_text.insert(tk.END, f"Starting Monthly Investment:    ${monthly:,.2f}\n")
            self.results_text.insert(tk.END, f"Annual Contribution Increase:   {annual_increase*100:.1f}%\n")
            self.results_text.insert(tk.END, f"Initial Investment:             ${initial:,.2f}\n")
            self.results_text.insert(tk.END, f"Investment Period:              {years} years\n")
            self.insert_colored(f"Weighted Average Return:        {weighted_return:.2f}% per year\n\n", 'success')
            
            self.insert_colored("SELECTED STRATEGIES\n", 'subheader')
            self.insert_colored("-" * 70 + "\n", 'subheader')
            for strategy, allocation in zip(selected_strategies, allocations):
                self.results_text.insert(tk.END, f"  {strategy}\n")
                self.insert_colored(f"    -> Allocation: {allocation*100:.1f}%  |  ", 'highlight')
                self.results_text.insert(tk.END, f"Return: {self.return_rates[strategy]}%  |  ")
                self.results_text.insert(tk.END, f"Risk: {self.risk_levels[strategy]}\n")
            
            self.insert_colored(f"\n{'='*70}\n", 'header')
            self.insert_colored(f"FINAL RESULTS AFTER {years} YEARS\n", 'header')
            self.insert_colored(f"{'='*70}\n", 'header')
            self.results_text.insert(tk.END, f"Total Contributed:              ${total_contributed:,.2f}\n")
            self.insert_colored(f"Final Portfolio Value:          ${final_value:,.2f}\n", 'success')
            self.insert_colored(f"Total Investment Gains:         ${total_gains:,.2f}\n", 'success')
            self.insert_colored(f"Return on Investment:           {(total_gains/total_contributed)*100:.1f}%\n\n", 'highlight')
            
            self.insert_colored(f"PASSIVE INCOME (at {withdrawal_rate*100:.0f}% withdrawal rate)\n", 'header')
            self.insert_colored("=" * 70 + "\n", 'header')
            self.insert_colored(f"Annual Passive Income:          ${annual_income:,.2f}\n", 'success')
            self.insert_colored(f"Monthly Passive Income:         ${monthly_income:,.2f}\n\n", 'success')
            
            self.insert_colored("="*70 + "\n", 'header')
            self.insert_colored("STEP-BY-STEP ACTION PLAN FOR YOUR JOURNEY\n", 'header')
            self.insert_colored("="*70 + "\n\n", 'header')
            
            # Generate personalized action plan
            self.insert_colored("PHASE 1: Foundation (Months 1-6)\n", 'subheader')
            self.results_text.insert(tk.END, f"Month 1-3:\n")
            if 'High-Yield Savings' in selected_strategies:
                self.insert_colored(f"  1. Open a High-Yield Savings Account (you selected this!)\n", 'success')
                self.results_text.insert(tk.END, f"     - Deposit ${monthly:,.2f}/month\n")
                self.results_text.insert(tk.END, f"     - Build emergency fund to $500-1000\n")
            else:
                self.results_text.insert(tk.END, f"  1. Consider opening a High-Yield Savings Account first\n")
                self.results_text.insert(tk.END, f"     - Build a small safety net before investing\n")
            
            self.results_text.insert(tk.END, f"\nMonth 4-6:\n")
            if initial > 0:
                self.insert_colored(f"  2. You're starting with ${initial:,.2f} - great head start!\n", 'success')
                self.results_text.insert(tk.END, f"     - Invest this lump sum immediately\n")
            else:
                self.results_text.insert(tk.END, f"  2. Start your investment accounts\n")
            
            # Account opening recommendations
            self.results_text.insert(tk.END, f"  3. Open these accounts based on your selections:\n")
            account_providers = {
                'Roth IRA': 'Fidelity, Vanguard, or Schwab',
                'Index Funds (S&P500)': 'Vanguard (VFIAX), Fidelity (FXAIX), or Schwab (SWPPX)',
                'Robo-Advisor': 'Betterment or Wealthfront',
                'Round-Up Apps': 'Acorns or Robinhood',
                'Certificates of Deposit': 'Your bank or Ally Bank',
                'Treasury Bonds': 'TreasuryDirect.gov',
                'Crypto (High Risk)': 'Coinbase or Kraken (5-10% of portfolio MAX!)',
                'Real Estate Crowdfund': 'Fundrise or RealtyMogul'
            }
            
            for strategy in selected_strategies:
                if strategy in account_providers:
                    allocation_pct = allocations[selected_strategies.index(strategy)] * 100
                    self.insert_colored(f"     - {strategy} ({allocation_pct:.0f}%): ", 'highlight')
                    self.results_text.insert(tk.END, f"{account_providers[strategy]}\n")
            
            self.results_text.insert(tk.END, f"\n")
            self.insert_colored("PHASE 2: Automation (Months 6-12)\n", 'subheader')
            self.results_text.insert(tk.END, f"Month 6:\n")
            self.insert_colored(f"  1. Set up automatic investments of ${monthly:,.2f}/month\n", 'success')
            self.results_text.insert(tk.END, f"     - Choose the same day each month (e.g., payday)\n")
            self.results_text.insert(tk.END, f"     - Split across your strategies:\n")
            
            for strategy, allocation in zip(selected_strategies, allocations):
                monthly_amount = monthly * allocation
                self.results_text.insert(tk.END, f"       * {strategy}: ${monthly_amount:.2f}/month\n")
            
            self.results_text.insert(tk.END, f"\nMonth 7-12:\n")
            self.results_text.insert(tk.END, f"  2. DO NOT check your accounts daily!\n")
            self.results_text.insert(tk.END, f"     - Markets go up and down - this is normal\n")
            self.results_text.insert(tk.END, f"     - Review quarterly, not daily\n")
            self.results_text.insert(tk.END, f"  3. Focus on increasing your income\n")
            self.results_text.insert(tk.END, f"     - Side hustles, skills, promotions\n")
            
            self.results_text.insert(tk.END, f"\n")
            self.insert_colored("PHASE 3: Growth (Years 1-5)\n", 'subheader')
            
            if annual_increase > 0:
                year1_contribution = monthly * (1 + annual_increase)
                self.insert_colored(f"  With your {annual_increase*100:.0f}% annual increase:\n", 'highlight')
                self.results_text.insert(tk.END, f"  - Year 1: ${monthly:,.2f}/month\n")
                self.results_text.insert(tk.END, f"  - Year 2: ${year1_contribution:.2f}/month\n")
                self.results_text.insert(tk.END, f"  - Year 3: ${year1_contribution * (1+annual_increase):.2f}/month\n")
                self.results_text.insert(tk.END, f"  - Year 4: ${year1_contribution * (1+annual_increase)**2:.2f}/month\n")
                self.results_text.insert(tk.END, f"  - Year 5: ${year1_contribution * (1+annual_increase)**3:.2f}/month\n\n")
            else:
                self.results_text.insert(tk.END, f"  Goal: Increase your monthly contribution over time\n")
                self.results_text.insert(tk.END, f"  - Even adding $10-20 more per year makes a huge difference!\n\n")
            
            self.results_text.insert(tk.END, f"  Action items:\n")
            self.insert_colored(f"  - Invest any bonuses or tax refunds\n", 'success')
            self.insert_colored(f"  - Increase contribution with every raise\n", 'success')
            self.insert_colored(f"  - Build additional income streams\n", 'success')
            
            self.results_text.insert(tk.END, f"\n")
            self.insert_colored("PHASE 4: Milestone Celebrations\n", 'subheader')
            
            # Calculate key milestones - FIXED VERSION
            milestones_to_show = []
            milestone_targets = [1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
            
            for target in milestone_targets:
                found = False
                for month_idx in range(len(portfolio_values)):
                    if portfolio_values[month_idx] >= target and not found:
                        years_to_milestone = month_idx / 12.0
                        if years_to_milestone <= years:
                            milestones_to_show.append((target, years_to_milestone))
                            found = True
                        break
            
            if milestones_to_show:
                self.results_text.insert(tk.END, f"  Here's when you'll hit major milestones:\n\n")
                for target, years_to in milestones_to_show[:7]:  # Show first 7 milestones
                    if years_to <= years:
                        passive_at_milestone = (target * withdrawal_rate) / 12
                        
                        # Format years more precisely
                        if years_to < 1:
                            months_to = int(years_to * 12)
                            self.insert_colored(f"  ${target:,.0f} ", 'highlight')
                            self.results_text.insert(tk.END, f"in ~{months_to} months")
                        else:
                            years_whole = int(years_to)
                            months_remainder = int((years_to - years_whole) * 12)
                            self.insert_colored(f"  ${target:,.0f} ", 'highlight')
                            if months_remainder > 0:
                                self.results_text.insert(tk.END, f"in ~{years_whole} years {months_remainder} months")
                            else:
                                self.results_text.insert(tk.END, f"in ~{years_whole} years")
                        
                        if passive_at_milestone >= 100:
                            self.insert_colored(f" -> ${passive_at_milestone:.0f}/month passive\n", 'success')
                        else:
                            self.results_text.insert(tk.END, "\n")
            else:
                self.results_text.insert(tk.END, f"  Keep investing! Your milestones will come with time.\n")
                self.results_text.insert(tk.END, f"  First target: ${milestone_targets[0]:,.0f}\n")
            
            self.results_text.insert(tk.END, f"\n")
            self.insert_colored("PHASE 5: Stay The Course (Years 5+)\n", 'subheader')
            self.results_text.insert(tk.END, f"  The hardest part: PATIENCE\n\n")
            self.results_text.insert(tk.END, f"  DO:\n")
            self.insert_colored(f"  - Keep investing every single month\n", 'success')
            self.insert_colored(f"  - Reinvest all dividends automatically\n", 'success')
            self.insert_colored(f"  - Increase contributions when possible\n", 'success')
            self.insert_colored(f"  - Rebalance once or twice a year\n", 'success')
            
            self.results_text.insert(tk.END, f"\n  DON'T:\n")
            self.results_text.insert(tk.END, f"  - Panic sell during market crashes\n")
            self.results_text.insert(tk.END, f"  - Try to time the market\n")
            self.results_text.insert(tk.END, f"  - Stop investing during downturns\n")
            self.results_text.insert(tk.END, f"  - Touch the money before your goal\n\n")
            
            self.insert_colored("="*70 + "\n", 'header')
            self.insert_colored("YOUR FIRST WEEK ACTION CHECKLIST\n", 'header')
            self.insert_colored("="*70 + "\n", 'header')
            self.results_text.insert(tk.END, f"[ ] Day 1: Research and compare account providers\n")
            self.results_text.insert(tk.END, f"[ ] Day 2-3: Open your selected accounts\n")
            self.results_text.insert(tk.END, f"[ ] Day 4: Link your bank account\n")
            self.results_text.insert(tk.END, f"[ ] Day 5: Set up automatic transfers\n")
            if initial > 0:
                self.results_text.insert(tk.END, f"[ ] Day 6: Make initial ${initial:,.2f} investment\n")
            else:
                self.results_text.insert(tk.END, f"[ ] Day 6: Make your first ${monthly:,.2f} deposit\n")
            self.results_text.insert(tk.END, f"[ ] Day 7: Enable dividend reinvestment (DRIP)\n")
            self.results_text.insert(tk.END, f"[ ] Ongoing: Track progress monthly, stay consistent!\n\n")
            
            self.insert_colored("MILESTONE CHECKPOINTS\n", 'subheader')
            self.insert_colored("-" * 70 + "\n", 'subheader')
            
            # Show detailed milestone breakdown every 5 years, plus intermediate years
            milestones_years = []
            if years >= 5:
                milestones_years.extend([1, 3, 5])
            if years >= 10:
                milestones_years.extend([7, 10])
            if years >= 15:
                milestones_years.extend([12, 15])
            if years >= 20:
                milestones_years.extend([17, 20])
            if years >= 25:
                milestones_years.extend([22, 25])
            if years >= 30:
                milestones_years.extend([27, 30])
            if years >= 40:
                milestones_years.extend([35, 40])
            
            for milestone in sorted(set(milestones_years)):
                if milestone <= years:
                    milestone_months = milestone * 12
                    milestone_value = portfolio_values[milestone_months]
                    milestone_contributed = contributions_total[milestone_months] + initial
                    milestone_gains = milestone_value - milestone_contributed
                    milestone_income = milestone_value * withdrawal_rate / 12
                    milestone_annual_income = milestone_value * withdrawal_rate
                    roi = (milestone_gains / milestone_contributed * 100) if milestone_contributed > 0 else 0
                    
                    self.insert_colored(f"\n=== Year {milestone} ===\n", 'highlight')
                    self.results_text.insert(tk.END, f"  Portfolio Value:        ${milestone_value:,.2f}\n")
                    self.results_text.insert(tk.END, f"  Total Contributed:      ${milestone_contributed:,.2f}\n")
                    self.insert_colored(f"  Investment Gains:       ${milestone_gains:,.2f}\n", 'success')
                    self.results_text.insert(tk.END, f"  ROI:                    {roi:.1f}%\n")
                    self.insert_colored(f"  Monthly Passive Income: ${milestone_income:,.2f}\n", 'success')
                    self.results_text.insert(tk.END, f"  Annual Passive Income:  ${milestone_annual_income:,.2f}\n")
                    
                    # Show contribution rate at this point
                    if milestone > 0:
                        monthly_at_milestone = monthly * ((1 + annual_increase) ** milestone)
                        self.results_text.insert(tk.END, f"  Your Monthly Investment: ${monthly_at_milestone:,.2f}\n")
            
            if monthly_income < 2000:
                self.insert_colored(f"\n{'='*70}\n", 'header')
                self.insert_colored("ACCELERATE YOUR JOURNEY\n", 'header')
                self.insert_colored(f"{'='*70}\n", 'header')
                self.results_text.insert(tk.END, f"Current monthly passive income: ${monthly_income:,.2f}\n\n")
                self.insert_colored(f"To reach $2,000/month passive income:\n", 'highlight')
                self.results_text.insert(tk.END, f"  Portfolio needed: ${2000*12/withdrawal_rate:,.2f}\n\n")
                self.results_text.insert(tk.END, "STRATEGIES TO GET THERE FASTER:\n")
                self.insert_colored("  - Increase contributions as income grows\n", 'success')
                self.insert_colored("  - Invest windfalls (bonuses, tax returns)\n", 'success')
                self.insert_colored("  - Build additional income streams\n", 'success')
                self.insert_colored("  - Consider lower cost-of-living locations\n\n", 'success')
                self.insert_colored("Remember: Consistency beats perfection!\n", 'highlight')
            else:
                self.insert_colored(f"\n{'='*70}\n", 'header')
                self.insert_colored("CONGRATULATIONS!\n", 'header')
                self.insert_colored(f"{'='*70}\n", 'header')
                self.insert_colored(f"You're on track for ${monthly_income:,.2f}/month in passive income!\n\n", 'success')
                self.results_text.insert(tk.END, "This could support a comfortable lifestyle in many parts\n")
                self.results_text.insert(tk.END, "of the world. Keep building your empire!\n")
            
            self.create_graph(portfolio_values, contributions_total, years, withdrawal_rate)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields!")
    
    def insert_colored(self, text, tag):
        """Helper to insert colored text"""
        self.results_text.insert(tk.END, text, tag)
    
    def create_graph(self, portfolio_values, contributions_total, years, withdrawal_rate):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Set dark theme for matplotlib
        plt.style.use('dark_background')
        
        fig = plt.figure(figsize=(10, 9))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        fig.patch.set_facecolor(self.bg_light)
        
        months = len(portfolio_values) - 1
        time_array = np.arange(0, months + 1) / 12
        
        # Main portfolio growth (larger, top)
        ax1 = fig.add_subplot(gs[0, :])
        ax1.set_facecolor(self.bg_light)
        ax1.plot(time_array, portfolio_values, label='Portfolio Value', color='#00ff88', linewidth=2.5, zorder=3)
        ax1.plot(time_array, contributions_total, label='Total Contributed', color='#00d4ff', linewidth=2, linestyle='--', zorder=2)
        ax1.fill_between(time_array, contributions_total, portfolio_values, alpha=0.3, color='#00ff88', label='Investment Gains', zorder=1)
        
        # Add milestone markers
        milestone_targets = [10000, 25000, 50000, 100000, 250000, 500000, 1000000]
        for target in milestone_targets:
            for idx, val in enumerate(portfolio_values):
                if val >= target and (idx == 0 or portfolio_values[idx-1] < target):
                    year_at = idx / 12
                    if year_at <= years:
                        ax1.axvline(x=year_at, color='#ffd700', linestyle=':', alpha=0.3, linewidth=1)
                        ax1.text(year_at, val, f'${target/1000:.0f}K', 
                                fontsize=7, color='#ffd700', rotation=90, 
                                verticalalignment='bottom', horizontalalignment='right')
                    break
        
        ax1.set_xlabel('Years', fontsize=11, color=self.text_color, fontweight='bold')
        ax1.set_ylabel('Portfolio Value ($)', fontsize=11, color=self.text_color, fontweight='bold')
        ax1.set_title('Portfolio Growth Over Time (with Milestones)', fontsize=13, fontweight='bold', color=self.accent_gold, pad=15)
        ax1.legend(loc='upper left', fontsize=9, framealpha=0.9, facecolor=self.bg_medium, edgecolor=self.accent_blue)
        ax1.grid(True, alpha=0.2, color=self.text_dim)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K' if x >= 1000 else f'${x:.0f}'))
        ax1.tick_params(colors=self.text_dim)
        for spine in ax1.spines.values():
            spine.set_color(self.accent_blue)
        
        # Passive income growth (middle left)
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.set_facecolor(self.bg_light)
        monthly_income = [v * withdrawal_rate / 12 for v in portfolio_values]
        ax2.plot(time_array, monthly_income, label='Monthly Passive Income', color='#ffd700', linewidth=2.5, zorder=3)
        ax2.axhline(y=1000, color='#ff6b6b', linestyle='--', linewidth=1.5, label='$1K/month', zorder=2, alpha=0.7)
        ax2.axhline(y=2000, color='#ff6b6b', linestyle='--', linewidth=2, label='$2K/month', zorder=2)
        ax2.axhline(y=3000, color='#ff6b6b', linestyle='--', linewidth=1.5, label='$3K/month', zorder=2, alpha=0.7)
        ax2.set_xlabel('Years', fontsize=10, color=self.text_color, fontweight='bold')
        ax2.set_ylabel('Monthly Income ($)', fontsize=10, color=self.text_color, fontweight='bold')
        ax2.set_title('Passive Income Growth', fontsize=11, fontweight='bold', color=self.accent_gold, pad=10)
        ax2.legend(loc='upper left', fontsize=7, framealpha=0.9, facecolor=self.bg_medium, edgecolor=self.accent_blue)
        ax2.grid(True, alpha=0.2, color=self.text_dim)
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        ax2.tick_params(colors=self.text_dim, labelsize=8)
        for spine in ax2.spines.values():
            spine.set_color(self.accent_blue)
        
        # Gains vs Contributions breakdown (middle right)
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.set_facecolor(self.bg_light)
        gains = [portfolio_values[i] - contributions_total[i] for i in range(len(portfolio_values))]
        ax3.plot(time_array, contributions_total, label='Your Money', color='#00d4ff', linewidth=2, zorder=2)
        ax3.plot(time_array, gains, label='Investment Gains', color='#00ff88', linewidth=2.5, zorder=3)
        ax3.set_xlabel('Years', fontsize=10, color=self.text_color, fontweight='bold')
        ax3.set_ylabel('Value ($)', fontsize=10, color=self.text_color, fontweight='bold')
        ax3.set_title('Your Money vs. Compound Gains', fontsize=11, fontweight='bold', color=self.accent_gold, pad=10)
        ax3.legend(loc='upper left', fontsize=7, framealpha=0.9, facecolor=self.bg_medium, edgecolor=self.accent_blue)
        ax3.grid(True, alpha=0.2, color=self.text_dim)
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K' if x >= 1000 else f'${x:.0f}'))
        ax3.tick_params(colors=self.text_dim, labelsize=8)
        for spine in ax3.spines.values():
            spine.set_color(self.accent_blue)
        
        # Annual contribution growth (bottom left)
        ax4 = fig.add_subplot(gs[2, 0])
        ax4.set_facecolor(self.bg_light)
        annual_increase = float(self.increase_var.get()) / 100
        monthly_start = float(self.monthly_var.get())
        yearly_contributions = [monthly_start * 12 * ((1 + annual_increase) ** year) for year in range(years + 1)]
        year_markers = list(range(years + 1))
        ax4.bar(year_markers, yearly_contributions, color='#00d4ff', alpha=0.7, edgecolor=self.accent_blue, linewidth=1.5)
        ax4.set_xlabel('Year', fontsize=10, color=self.text_color, fontweight='bold')
        ax4.set_ylabel('Annual Contribution ($)', fontsize=10, color=self.text_color, fontweight='bold')
        ax4.set_title('How Your Contributions Grow', fontsize=11, fontweight='bold', color=self.accent_gold, pad=10)
        ax4.grid(True, alpha=0.2, color=self.text_dim, axis='y')
        ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        ax4.tick_params(colors=self.text_dim, labelsize=8)
        for spine in ax4.spines.values():
            spine.set_color(self.accent_blue)
        
        # ROI over time (bottom right)
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.set_facecolor(self.bg_light)
        roi_values = []
        for i in range(len(portfolio_values)):
            contributed = contributions_total[i] + float(self.initial_var.get())
            if contributed > 0:
                roi = ((portfolio_values[i] - contributed) / contributed) * 100
                roi_values.append(roi)
            else:
                roi_values.append(0)
        ax5.plot(time_array, roi_values, color='#ffd700', linewidth=2.5)
        ax5.axhline(y=0, color='#ff6b6b', linestyle='-', linewidth=1, alpha=0.5)
        ax5.fill_between(time_array, 0, roi_values, where=[r >= 0 for r in roi_values], 
                        alpha=0.3, color='#00ff88', interpolate=True)
        ax5.set_xlabel('Years', fontsize=10, color=self.text_color, fontweight='bold')
        ax5.set_ylabel('ROI (%)', fontsize=10, color=self.text_color, fontweight='bold')
        ax5.set_title('Return on Investment Over Time', fontsize=11, fontweight='bold', color=self.accent_gold, pad=10)
        ax5.grid(True, alpha=0.2, color=self.text_dim)
        ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0f}%'))
        ax5.tick_params(colors=self.text_dim, labelsize=8)
        for spine in ax5.spines.values():
            spine.set_color(self.accent_blue)
        
        canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

print("About to check if __name__ == '__main__'...")
print(f"__name__ is: {__name__}")

if __name__ == "__main__":
    print("YES! We're in main!")
    try:
        print("Creating main window...")
        root = tk.Tk()
        print("Main window created!")
        
        print("Initializing calculator...")
        app = InvestmentCalculator(root)
        print("Calculator initialized!")
        
        print("Starting main loop...")
        root.mainloop()
    except Exception as e:
        import traceback
        print("\n=== ERROR OCCURRED ===")
        print(traceback.format_exc())
        print("======================\n")
        input("Press Enter to exit...")