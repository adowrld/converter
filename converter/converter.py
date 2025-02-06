import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from dotenv import load_dotenv
import os

load_dotenv()

currency_names = {
    "USD": "United States Dollar",
    "EUR": "Euro",
    "GBP": "British Pound Sterling",
    "JPY": "Japanese Yen",
    "INR": "Indian Rupee",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "TRY": "Turkish Lira"
}

def convert_currency(amount, from_currency, to_currency, api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}/{amount}"
    response = requests.get(url)

    if response.status_code == 200:
        response_data = response.json()
        if response_data["result"] == "success":
            return response_data["conversion_result"]
        else:
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def on_convert_button_click():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_combobox.get()
        to_currency = to_currency_combobox.get()
        
        if from_currency == to_currency:
            messagebox.showerror("Error", "Source and target currencies cannot be the same.")
            return
        
        result = convert_currency(amount, from_currency, to_currency, api_key)

        if result:
            result_label.config(text=f"Converted Amount: {result:.2f} {to_currency}")
        else:
            messagebox.showerror("Error", "Unable to fetch exchange rates. Please check your API key.")
    
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for the amount.")

def show_currency_info():
    from_currency = from_currency_combobox.get()
    to_currency = to_currency_combobox.get()

    if from_currency in currency_names and to_currency in currency_names:
        info_message = f"{from_currency}: {currency_names[from_currency]}\n{to_currency}: {currency_names[to_currency]}"
    else:
        info_message = "Invalid currency code selected."
    
    messagebox.showinfo("Currency Information", info_message)

def show_converter_frame():
    initial_frame.pack_forget()  # Hide the initial frame
    converter_frame.pack(fill="both", expand=True)  # Show the currency converter frame

root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x300")

api_key = "e6fcd3f0cf5fc11af139724a"


initial_frame = tk.Frame(root)

welcome_label = tk.Label(initial_frame, text="Welcome to the Currency Converter App!", font=("Arial", 13, "bold"))
welcome_label.pack(pady=40)
welcome_label.pack(padx=10)

start_button = tk.Button(initial_frame, text="Go to Converter", command=show_converter_frame, width=15, height=5, font=("Arial", 10, "bold"), fg="red", activeforeground="yellow", activebackground="red")
start_button.pack(pady=20,)

me_label = tk.Label(initial_frame, text="developed by ado", font=("Arial", 10, "italic"))
me_label.pack(pady=20)

initial_frame.pack(fill="both", expand=True)  # Show the initial frame first

# Currency converter frame
converter_frame = tk.Frame(root)

amount_label = tk.Label(converter_frame, text="Enter Amount:")
amount_label.pack(pady=5)
amount_entry = tk.Entry(converter_frame)
amount_entry.pack(pady=5)

from_currency_label = tk.Label(converter_frame, text="From Currency:")
from_currency_label.pack(pady=5)

currency_list = ["", "USD", "EUR", "GBP", "JPY", "INR", "AUD", "CAD", "CHF", "CNY", "TRY"]
from_currency_combobox = ttk.Combobox(converter_frame, values=currency_list, state="readonly")
from_currency_combobox.set("")
from_currency_combobox.pack(pady=5)

to_currency_label = tk.Label(converter_frame, text="To Currency:")
to_currency_label.pack(pady=5)

to_currency_combobox = ttk.Combobox(converter_frame, values=currency_list, state="readonly")
to_currency_combobox.set("")
to_currency_combobox.pack(pady=5)

convert_button = tk.Button(converter_frame, text="Convert", command=lambda: on_convert_button_click())
convert_button.pack(pady=20)

result_label = tk.Label(converter_frame, text="Converted Amount: ")
result_label.pack(pady=5)

info_button = tk.Button(converter_frame, text="Info", command=show_currency_info)
info_button.place(x=350, y=10)  # Position the button in the top-right corner

root.mainloop()
