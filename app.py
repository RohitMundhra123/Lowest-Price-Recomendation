from matplotlib import pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Read the dataset
df = pd.read_csv("dataset.csv")

# Convert the item name to uppercase for consistency
df['Item Name'] = df['Item Name'].str.upper()

# Create the GUI
root = tk.Tk()
root.geometry("600x400")
root.title("Lowest Price Recommendation System")

# Label for the item name input
item_label = ttk.Label(root, text="Enter the product name:")
item_label.pack(pady=10)

# Entry field for the item name input
item_entry = ttk.Entry(root, width=30)
item_entry.pack()

def show_graph(amazon_price, flipkart_price, nykaa_price):
    c = ['red', 'yellow', 'green']
    fig = Figure(figsize=(4,4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(['Amazon', 'Flipkart', 'Nykaa'], (amazon_price, flipkart_price, nykaa_price), color=c, width=0.3)
    ax.set_title("Price Comparison")
    ax.set_xlabel("Platforms")
    ax.set_ylabel("Price (in Rs)")
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


# Function to handle the button click event
def get_lowest_price():
    item = item_entry.get().upper()
    filtered_df = df[df['Item Name'] == item]

    # check if any rows were returned
    if len(filtered_df) == 0:
        result_label.config(text=f"No data found for {item}")
    else:
        # initialize variables to store minimum price and platform
        min_price = 999999999.9
        min_platforms = []

        # iterate through each row of the filtered dataframe
        for index, row in filtered_df.iterrows():
            amazon_price = row['Amazon Price']
            flipkart_price = row['Flipkart Price']
            nykaa_price = row['Nykaa Price']
        
            show_graph(amazon_price, flipkart_price, nykaa_price)

            # check if current platform has the minimum price for the current product
            if amazon_price <= flipkart_price and amazon_price <= nykaa_price:
                if amazon_price < min_price:
                    min_price = amazon_price
                    min_platforms = ['Amazon']

            elif flipkart_price <= amazon_price and flipkart_price <= nykaa_price:
                if flipkart_price < min_price:
                    min_price = flipkart_price
                    min_platforms = ['Flipkart']

            elif nykaa_price <= amazon_price and nykaa_price <= flipkart_price:
                if nykaa_price < min_price:
                    min_price = nykaa_price
                    min_platforms = ['Nykaa']

        # display the result
        if len(min_platforms) == 1:
            result_label.config(text=f"{min_platforms[0]} has the lowest price for {item}")
        else:
            platforms = ' and '.join(min_platforms)
            result_label.config(text=f"{platforms} have the lowest price for {item}")
       
# Button to trigger the price check
check_button = ttk.Button(root, text="Check Lowest Price", command=get_lowest_price)
check_button.pack(pady=10)

# Frame to display the result
result_frame = tk.Frame(root)
result_frame.pack(pady=20)

# Label to display the result
result_label = ttk.Label(result_frame, text="")
result_label.pack()

# Start the GUI event loop
root.mainloop()
