import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyAusIrjsAZ2CKqxHGLYDCKxkFd3xhBIZTI')

model = genai.GenerativeModel('gemini-pro')
question = ' This system will streamline categorization and retrieval processes by accurately extracting essential terms such as product company , product name, quantity, and price(only these are to be extracted). Follow this format for example : Parle biscuit: 5 packets, 10rs each.  Ensure high-level accuracy in recognizing crucial details to optimize inventory management workflows and facilitate seamless integration with inventory systems.'
response = model.generate_content(f'{question }Add 5 packets of biscuits of Parle of 10rs each, 3 packets of Maggi of 15rs each, 15 packets of Lays 10 rs each and 5 packets of 1 litre of Milk of 60rs each , 2 dazan vim saboon 5 wala, 1kg amul cheese cube 120 Rs , 2 litres of Coca Cola of 60 rs each')

print(response.text)