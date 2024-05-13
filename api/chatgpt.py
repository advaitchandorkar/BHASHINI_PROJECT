data = """
Vimbar: 12 pieces, 5rs each
Agarbatti: 2 packets, 35rs each
Amul Milk: 2 litres, 36rs
"""



# Split data by lines
items = data.strip().split('\n')

# Initialize a 2D list to store product information
product_info = []

# Extract information from each item
for item in items:
    # Split item into product name, quantity, and price
    name_quantity_price = item.split(': ')
    
    # Extract product name
    product_name = name_quantity_price[0].split()[-1]  # Extract the last word as product name
    
    # Extract quantity and price
    quantity_price = name_quantity_price[1].split(', ')
    quantity = quantity_price[0].split()[0]
    price = quantity_price[1].split()[0]
    
    # Remove 'rs' or 'rupees' from price if present
    if price.endswith('rs') or price.endswith('rupees'):
        price = price[:-2]

    # Append product information to the 2D list
    product_info.append([product_name, quantity, price])

# Print the 2D list
for item in product_info:
    print(item)
