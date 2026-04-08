"""
Tip Calculator Application

This application helps users calculate tip amounts and split bills among multiple diners.
Built using Tkinter with modern styling for the graphical user interface.

Author: [Your Name]
Date: April 8, 2026

LEARNING OBJECTIVES:
- GUI development with Tkinter
- Event-driven programming
- Input validation and error handling
- Color schemes and modern UI design
- Mathematical calculations in Python
"""

# Import necessary modules for the GUI application
import tkinter as tk  # Main GUI library for creating windows and widgets
from tkinter import ttk, messagebox  # ttk for themed widgets, messagebox for dialogs

class ColorfulTipCalculator:
    """
    A colorful graphical tip calculator application using Tkinter with vibrant styling.

    This class creates a complete GUI application that:
    1. Takes user input for bill amount and tip percentage
    2. Calculates total bill with tip
    3. Splits the bill among multiple diners
    4. Updates calculations automatically when inputs change
    5. Provides a modern, colorful user interface

    Features:
    - Input for bill amount with validation (handles non-numeric input)
    - Radio buttons for tip percentage selection (10%, 15%, 20%)
    - Spinbox for number of diners (1-6 people)
    - Automatic calculation updates (no need to click calculate)
    - Colorful UI with distinct sections and emojis for visual appeal
    - Quit button and window close functionality
    """

    def __init__(self, root):
        """
        Initialize the Colorful Tip Calculator application.

        This constructor method sets up the entire application by:
        1. Configuring the main window properties
        2. Setting up the color scheme and styling
        3. Creating all the GUI widgets
        4. Setting up event bindings for automatic updates

        Args:
            root: The root Tkinter window (main application window)
        """
        # Store reference to the main window
        self.root = root

        # Configure the main window appearance and size
        self.root.title("💰 Colorful Tip Calculator")  # Window title with emoji
        self.root.geometry("450x400")  # Window size: 450px wide, 400px tall
        self.root.configure(bg='#e8f4f8')  # Light blue background color

        # Initialize ttk styling system for consistent widget appearance
        self.style = ttk.Style()

        # Configure basic styles for different widget types
        self.style.configure('TLabel', font=('Arial', 10))  # Default label font
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')  # Title style
        self.style.configure('TButton', font=('Arial', 10, 'bold'))  # Button font
        self.style.configure('Calculate.TButton', background='#3498db', foreground='white')  # Special button style
        self.style.configure('TRadiobutton', font=('Arial', 10))  # Radio button font
        self.style.configure('TSpinbox', font=('Arial', 10))  # Spinbox font

        # Define a comprehensive color scheme for the application
        # This dictionary stores all colors used throughout the UI for consistency
        self.colors = {
            'bg_main': '#e8f4f8',      # Light blue main background
            'bg_bill': '#fff3cd',     # Light yellow for bill input section
            'bg_tip': '#d1ecf1',      # Light cyan for tip selection section
            'bg_diners': '#d4edda',   # Light green for number of diners section
            'bg_results': '#f8d7da',  # Light pink for calculation results section
            'text_primary': '#2c3e50', # Dark blue for main text
            'text_success': '#28a745', # Green for positive results (total amount)
            'text_danger': '#dc3545',  # Red for per-person amounts
            'accent': '#007bff'       # Blue accent color for selections
        }

        # Create Tkinter StringVar and other variables to store user inputs and results
        # These variables automatically update the GUI when their values change
        self.bill_amount = tk.StringVar()  # Stores the bill amount entered by user
        self.tip_percentage = tk.DoubleVar(value=0.15)  # Stores tip % (default 15%)
        self.num_diners = tk.IntVar(value=1)  # Stores number of diners (default 1)

        # Variables for displaying calculation results in the GUI
        self.total_with_tip = tk.StringVar()  # Shows total bill + tip
        self.amount_per_person = tk.StringVar()  # Shows amount each person pays

        # Create all the GUI widgets and set up event bindings
        self.create_widgets()
        self.setup_bindings()

    def create_widgets(self):
        """
        Create and arrange all the GUI widgets with colorful modern styling.

        This method builds the entire user interface by:
        1. Creating a main container frame
        2. Adding a title label
        3. Creating four main sections: Bill input, Tip selection, Diners, and Results
        4. Adding interactive widgets (entry, radio buttons, spinbox, labels)
        5. Styling everything with colors and proper layout
        """
        # Create the main container frame that holds all other widgets
        # This frame has padding and uses the main background color
        main_frame = tk.Frame(self.root, bg=self.colors['bg_main'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)  # Fill entire window, expand if resized

        # Create the application title with emoji for visual appeal
        # Positioned at the top with extra spacing below
        title_label = tk.Label(main_frame, text="🍽️ Restaurant Bill Calculator",
                              font=('Arial', 18, 'bold'), fg=self.colors['text_primary'],
                              bg=self.colors['bg_main'])
        title_label.pack(pady=(0, 25))  # No top padding, 25px bottom padding

        # ===== BILL AMOUNT INPUT SECTION =====
        # Create a labeled frame (box with title) for bill input
        # Uses light yellow background to distinguish this section
        bill_frame = tk.LabelFrame(main_frame, text="💵 Bill Details", padx=15, pady=10,
                                  bg=self.colors['bg_bill'], fg=self.colors['text_primary'],
                                  font=('Arial', 11, 'bold'), relief='groove', bd=2)
        bill_frame.pack(fill=tk.X, pady=(0, 15))  # Fill width, 15px bottom margin

        # Label explaining what to enter in the bill amount field
        tk.Label(bill_frame, text="Bill Amount ($):", font=('Arial', 11),
                bg=self.colors['bg_bill'], fg=self.colors['text_primary']).grid(row=0, column=0, sticky="w", pady=5)

        # Text entry field where user types the bill amount
        # Connected to self.bill_amount variable for automatic updates
        self.bill_entry = tk.Entry(bill_frame, textvariable=self.bill_amount,
                                  font=('Arial', 11), width=20, relief='solid', bd=1)
        self.bill_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="ew")  # Expand to fill space

        # ===== TIP PERCENTAGE SELECTION SECTION =====
        # Create another labeled frame for tip selection with light cyan background
        tip_frame = tk.LabelFrame(main_frame, text="🎯 Tip Percentage", padx=15, pady=10,
                                 bg=self.colors['bg_tip'], fg=self.colors['text_primary'],
                                 font=('Arial', 11, 'bold'), relief='groove', bd=2)
        tip_frame.pack(fill=tk.X, pady=(0, 15))

        # Label for the tip selection area
        tk.Label(tip_frame, text="Select Tip Rate:", font=('Arial', 11),
                bg=self.colors['bg_tip'], fg=self.colors['text_primary']).grid(row=0, column=0, sticky="w", pady=5)

        # Container frame to hold the radio buttons horizontally
        tip_container = tk.Frame(tip_frame, bg=self.colors['bg_tip'])
        tip_container.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="w")

        # Create radio buttons for tip percentages (10%, 15%, 20%)
        # Each radio button connects to self.tip_percentage variable
        percentages = [("10%", 0.10), ("15%", 0.15), ("20%", 0.20)]
        for i, (text, value) in enumerate(percentages):
            rb = tk.Radiobutton(tip_container, text=text, variable=self.tip_percentage,
                               value=value, font=('Arial', 10), bg=self.colors['bg_tip'],
                               fg=self.colors['text_primary'], activebackground=self.colors['bg_tip'],
                               selectcolor=self.colors['accent'])  # Blue dot when selected
            rb.pack(side=tk.LEFT, padx=(0, 15))  # Pack horizontally with spacing

        # ===== NUMBER OF DINERS SECTION =====
        # Create labeled frame for diner count with light green background
        diners_frame = tk.LabelFrame(main_frame, text="👥 Split Bill", padx=15, pady=10,
                                    bg=self.colors['bg_diners'], fg=self.colors['text_primary'],
                                    font=('Arial', 11, 'bold'), relief='groove', bd=2)
        diners_frame.pack(fill=tk.X, pady=(0, 15))

        # Label for the number of diners input
        tk.Label(diners_frame, text="Number of People:", font=('Arial', 11),
                bg=self.colors['bg_diners'], fg=self.colors['text_primary']).grid(row=0, column=0, sticky="w", pady=5)

        # Spinbox widget allowing selection from 1-6 diners
        # Connected to self.num_diners variable
        self.diners_spinbox = tk.Spinbox(diners_frame, from_=1, to=6,
                                        textvariable=self.num_diners, width=8,
                                        font=('Arial', 10), relief='solid', bd=1)
        self.diners_spinbox.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="w")

        # ===== CALCULATION RESULTS SECTION =====
        # Create labeled frame for displaying results with light pink background
        results_frame = tk.LabelFrame(main_frame, text="📊 Calculation Results", padx=15, pady=15,
                                     bg=self.colors['bg_results'], fg=self.colors['text_primary'],
                                     font=('Arial', 11, 'bold'), relief='groove', bd=2)
        results_frame.pack(fill=tk.X, pady=(0, 20))

        # Frame for the total amount (bill + tip)
        total_frame = tk.Frame(results_frame, bg=self.colors['bg_results'])
        total_frame.pack(fill=tk.X, pady=(0, 12))

        # Label showing "Total with Tip:" on the left
        tk.Label(total_frame, text="💰 Total with Tip:", font=('Arial', 12, 'bold'),
                bg=self.colors['bg_results'], fg=self.colors['text_primary']).pack(side=tk.LEFT)

        # Label showing the calculated total amount in green on the right
        self.total_label = tk.Label(total_frame, textvariable=self.total_with_tip,
                                   font=('Arial', 14, 'bold'), fg=self.colors['text_success'],
                                   bg=self.colors['bg_results'])
        self.total_label.pack(side=tk.RIGHT)

        # Frame for the per-person amount
        person_frame = tk.Frame(results_frame, bg=self.colors['bg_results'])
        person_frame.pack(fill=tk.X)

        # Label showing "Each Person Pays:" on the left
        tk.Label(person_frame, text="🧾 Each Person Pays:", font=('Arial', 12, 'bold'),
                bg=self.colors['bg_results'], fg=self.colors['text_primary']).pack(side=tk.LEFT)

        # Label showing the per-person amount in red on the right
        self.person_label = tk.Label(person_frame, textvariable=self.amount_per_person,
                                    font=('Arial', 14, 'bold'), fg=self.colors['text_danger'],
                                    bg=self.colors['bg_results'])
        self.person_label.pack(side=tk.RIGHT)

        # ===== QUIT BUTTON =====
        # Create a red exit button at the bottom
        quit_button = tk.Button(main_frame, text="🚪 Exit Calculator", command=self.quit_app,
                               font=('Arial', 11, 'bold'), bg='#dc3545', fg='white',
                               activebackground='#c82333', activeforeground='white',
                               relief='raised', bd=2, padx=20, pady=8)
        quit_button.pack(pady=(10, 0))

        # Configure grid weights for proper resizing behavior
        # This ensures columns expand properly when window is resized
        bill_frame.columnconfigure(1, weight=1)
        tip_frame.columnconfigure(1, weight=1)
        diners_frame.columnconfigure(1, weight=1)

    def setup_bindings(self):
        """
        Set up event bindings for automatic calculation updates.

        This method connects the calculation function to changes in input variables,
        enabling real-time updates without requiring a "Calculate" button.

        Tkinter variables (StringVar, DoubleVar, IntVar) have a trace method that
        calls a function whenever the variable's value changes.
        """
        # Bind the calculate method to run whenever bill_amount changes
        # "w" means "write" - triggers when the variable is written to
        self.bill_amount.trace("w", self.calculate)

        # Bind to tip percentage changes
        self.tip_percentage.trace("w", self.calculate)

        # Bind to number of diners changes
        self.num_diners.trace("w", self.calculate)

        # Handle window close button (X button) to properly quit the application
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def calculate(self, *args):
        """
        Calculate the tip and split the bill among diners.
        Updates the result labels automatically.

        This method is called whenever any input changes (bill amount, tip %, or diners).
        It performs all the mathematical calculations and updates the display.

        Args:
            *args: Required by Tkinter's trace callback, but not used here
        """
        try:
            # Get the bill amount from the entry field as a string
            bill_text = self.bill_amount.get().strip()

            # Handle empty input - show $0.00 for both results
            if not bill_text:
                self.total_with_tip.set("$0.00")
                self.amount_per_person.set("$0.00")
                return

            # Convert string to float - this will raise ValueError if not a number
            bill = float(bill_text)

            # Validate that bill amount is not negative
            if bill < 0:
                raise ValueError("Bill amount cannot be negative")

            # Get the selected tip percentage (0.10, 0.15, or 0.20)
            tip_percent = self.tip_percentage.get()

            # Get the number of diners (1-6)
            diners = self.num_diners.get()

            # ===== PERFORM CALCULATIONS =====
            # Calculate the tip amount: bill * tip_percentage
            tip_amount = bill * tip_percent

            # Calculate total bill including tip: original bill + tip amount
            total = bill + tip_amount

            # Calculate amount each person pays: total bill divided by number of diners
            per_person = total / diners

            # ===== UPDATE DISPLAY =====
            # Format and display the total amount with 2 decimal places
            self.total_with_tip.set(f"${total:.2f}")

            # Format and display the per-person amount with 2 decimal places
            self.amount_per_person.set(f"${per_person:.2f}")

        except ValueError:
            # This catches both invalid number conversion and negative bill amounts
            # Display error messages in the result labels
            self.total_with_tip.set("Invalid input")
            self.amount_per_person.set("Invalid input")

    def quit_app(self):
        """
        Quit the application cleanly.

        This method is called when the user clicks the Quit button or closes the window.
        It properly terminates the Tkinter main loop.
        """
        self.root.quit()

def main():
    """
    Main function to run the Colorful Tip Calculator application.

    This function creates the main Tkinter window and starts the application.
    It follows the standard pattern for Tkinter applications:
    1. Create root window
    2. Create application instance
    3. Start the main event loop
    """
    # Create the main Tkinter window (root window)
    root = tk.Tk()

    # Create an instance of our ColorfulTipCalculator class
    # This initializes the entire application
    app = ColorfulTipCalculator(root)

    # Start the Tkinter event loop - this keeps the window open and responsive
    # The program will stay here until the user closes the window
    root.mainloop()

# This block ensures the application only runs when this file is executed directly
# (not when imported as a module by another script)
if __name__ == "__main__":
    main()