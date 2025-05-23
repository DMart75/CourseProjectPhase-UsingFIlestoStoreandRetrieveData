#Douglas Martinez
#CIS261
#Course Project - Payroll Management System

import os
from datetime import datetime

# File to store employee data
EMPLOYEE_FILE = "employee_data.txt"

def display_heading():
    print("Employee Payroll Management System")
    print("=" * 40)

def validate_date(date_str):
    """Validate date format mm/dd/yyyy"""
    try:
        datetime.strptime(date_str, "%m/%d/%Y")
        return True
    except ValueError:
        return False

def get_date_input(prompt):
    """Get and validate date input"""
    while True:
        date_input = input(prompt).strip()
        if validate_date(date_input):
            return date_input
        else:
            print("Invalid date format. Please enter date as mm/dd/yyyy")

def get_float_input(prompt):
    """Get and validate float input"""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid number. Please try again.")

def get_int_input(prompt):
    """Get and validate integer input"""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid integer. Please try again.")

def add_employee():
    """Add employee data to file"""
    print("\nEnter Employee Information:")
    
    from_date = get_date_input("Enter From Date (mm/dd/yyyy): ")
    to_date = get_date_input("Enter To Date (mm/dd/yyyy): ")
    employee_name = input("Enter Employee Name: ").strip()
    hours_worked = get_float_input("Enter Hours Worked: ")
    pay_rate = get_float_input("Enter Pay Rate: ")
    income_tax_rate = get_float_input("Enter Income Tax Rate (as decimal, e.g., 0.20 for 20%): ")
    
    # Create pipe-delimited record
    record = f"{from_date}|{to_date}|{employee_name}|{hours_worked}|{pay_rate}|{income_tax_rate}\n"
    
    # Append to file
    with open(EMPLOYEE_FILE, "a") as file:
        file.write(record)
    
    print(f"Employee {employee_name} added successfully!")

def calculate_pay(hours, rate, tax_rate):
    """Calculate gross pay, income tax, and net pay"""
    gross_pay = hours * rate
    income_tax = gross_pay * tax_rate
    net_pay = gross_pay - income_tax
    return gross_pay, income_tax, net_pay

def display_employee_report(from_date, to_date, name, hours, rate, gross, tax_rate, tax, net):
    """Display individual employee report"""
    print(f"From Date: {from_date}")
    print(f"To Date: {to_date}")
    print(f"Employee Name: {name}")
    print(f"Hours Worked: {hours:.2f}")
    print(f"Hourly Rate: ${rate:.2f}")
    print(f"Gross Pay: ${gross:.2f}")
    print(f"Income Tax Rate: {tax_rate:.2%}")
    print(f"Income Taxes: ${tax:.2f}")
    print(f"Net Pay: ${net:.2f}")
    print("-" * 40)

def generate_report():
    """Generate payroll report based on from date"""
    if not os.path.exists(EMPLOYEE_FILE):
        print("No employee data found!")
        return
    
    print("\nPayroll Report")
    print("=" * 40)
    
    filter_date = input("Enter From Date for report (mm/dd/yyyy) or 'All' for all records: ").strip()
    
    if filter_date.lower() != "all" and not validate_date(filter_date):
        print("Invalid date format!")
        return
    
    # Initialize totals
    totals = {
        "total_employees": 0,
        "total_hours": 0.0,
        "total_gross": 0.0,
        "total_tax": 0.0,
        "total_net": 0.0
    }
    
    # Read and process records
    with open(EMPLOYEE_FILE, "r") as file:
        for line in file:
            if line.strip():
                parts = line.strip().split("|")
                if len(parts) == 6:
                    from_date, to_date, name, hours_str, rate_str, tax_rate_str = parts
                    
                    # Check if record matches filter
                    if filter_date.lower() == "all" or from_date == filter_date:
                        hours = float(hours_str)
                        rate = float(rate_str)
                        tax_rate = float(tax_rate_str)
                        
                        # Calculate pay
                        gross, tax, net = calculate_pay(hours, rate, tax_rate)
                        
                        # Display employee data
                        display_employee_report(from_date, to_date, name, hours, rate, gross, tax_rate, tax, net)
                        
                        # Update totals
                        totals["total_employees"] += 1
                        totals["total_hours"] += hours
                        totals["total_gross"] += gross
                        totals["total_tax"] += tax
                        totals["total_net"] += net
    
    # Display totals
    if totals["total_employees"] > 0:
        print("\nTOTALS:")
        print("=" * 40)
        print(f"Total Employees: {totals['total_employees']}")
        print(f"Total Hours: {totals['total_hours']:.2f}")
        print(f"Total Gross Pay: ${totals['total_gross']:.2f}")
        print(f"Total Income Tax: ${totals['total_tax']:.2f}")
        print(f"Total Net Pay: ${totals['total_net']:.2f}")
    else:
        print(f"No records found for the specified criteria.")

def main():
    display_heading()
    
    while True:
        print("\nMenu:")
        print("1. Add Employee")
        print("2. Generate Report")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            add_employee()
        elif choice == "2":
            generate_report()
        elif choice == "3":
            print("Thank you for using the Payroll Management System!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()