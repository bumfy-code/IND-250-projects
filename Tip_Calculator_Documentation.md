# Tip Calculator Application Documentation

## GitHub Repository
**Note:** This project is currently a local development project. To create a GitHub repository:
1. Initialize git: `git init`
2. Add files: `git add .`
3. Commit: `git commit -m "Initial commit"`
4. Create GitHub repo and push

Repository URL: [To be added after GitHub setup]

## Development Process

### Project Overview
This project implements a graphical tip calculator application using Python's built-in Tkinter library. The application allows users to calculate tip amounts and split bills among multiple diners with an intuitive GUI interface.

### Development Steps
1. **Planning**: Analyzed requirements and designed the GUI layout with necessary components:
   - Bill amount input field
   - Tip percentage selection (radio buttons)
   - Number of diners selection (spinbox)
   - Result display areas
   - Quit functionality

2. **Implementation**:
   - Created the main `TipCalculator` class to organize the application
   - Implemented input validation for bill amounts
   - Added automatic calculation updates using Tkinter variable tracing
   - Designed the GUI layout with proper spacing and alignment
   - Added error handling for invalid inputs

3. **Testing**:
   - Verified syntax compilation
   - Tested GUI launch
   - Validated calculation logic

### Key Features Implemented
- **Input Validation**: Handles non-numeric bill amounts gracefully
- **Automatic Updates**: Calculations refresh immediately when inputs change
- **User-Friendly Interface**: Clear labels and logical widget arrangement
- **Flexible Tip Selection**: Radio buttons for 10%, 15%, 20% tips
- **Diner Splitting**: Spinbox for 1-6 diners
- **Clean Exit**: Quit button and window close handling

### Code Structure
- `TipCalculator` class: Main application logic
- Widget creation and layout methods
- Event binding for automatic updates
- Calculation method with error handling
- Main function for application startup

## Application Screenshot

[Insert screenshot here - GUI showing bill input, tip selection, diner count, and calculated results]

The GUI consists of:
- Bill Amount entry field at the top
- Tip percentage radio buttons (10%, 15%, 20%)
- Number of diners spinbox (1-6)
- Results section showing total with tip and amount per person
- Quit button at the bottom

## Usage Instructions
1. Run `python tip_calculator.py`
2. Enter the bill amount in dollars
3. Select desired tip percentage
4. Choose number of diners
5. View calculated totals (updates automatically)
6. Click Quit or close window to exit

## Technical Details
- **Language**: Python 3.x
- **GUI Library**: Tkinter (built-in)
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Dependencies**: None (uses only standard library)