import tkinter as tk
import pandas as pd
from pipeline import pipeline
from pipeline import analyze_recommendation
from pipeline import recommendation
from PIL import Image, ImageTk
import requests
from io import BytesIO

entry = None  # Declare entry as a global variable
root = None  # Declare root as a global variable

def clear_window(data):
    # Clear the entire window
    global root  # Access the global root variable
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg='#f0eae1')
    root.geometry('1300x900')

    # Add a new title
    title = tk.Label(root, text="Here's what we found:", font=("Times New Roman", 24), bg='#f0eae1')
    title.pack(pady=20)
    subtitle = tk.Label(root, text=data['restaurant_name'], font=("Times New Roman", 30), bg='#f0eae1')
    subtitle.pack(pady=5)
    text = tk.Label(root, text=data['expert_rating'], font=("Times New Roman", 36), bg='#f0eae1')
    text.pack(pady=10)
    text.place(x=950, y=150)
    text2 = tk.Label(root, text="our expert rating", font=("Times New Roman", 24), bg='#f0eae1')
    text2.pack(pady=10)
    text2.place(x=900, y=200)
    text3 = tk.Label(root, text=data['delivery_rating'], font=("Times New Roman", 36), bg='#f0eae1')
    text3.pack(pady=10)
    text3.place(x=750, y=150)
    text4 = tk.Label(root, text="delivery rating", font=("Times New Roman", 24), bg='#f0eae1')
    text4.pack(pady=10)
    text4.place(x=700, y=200)
    
    response = requests.get(data['url1'])
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    max_size = (400, 550)
    img.thumbnail(max_size)
    img_tk = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=img_tk)
    img_label.image = img_tk  # Keep a reference to the image to prevent it from being garbage collected
    img_label.pack()
    img_label.place(x=150, y=200)
    
    response2 = requests.get(data['url2'])
    img_data2 = response2.content
    img2 = Image.open(BytesIO(img_data2))
    img2.thumbnail(max_size)
    img_tk2 = ImageTk.PhotoImage(img2)
    img_label2 = tk.Label(root, image=img_tk2)
    img_label2.image = img_tk2  # Keep a reference to the image to prevent it from being garbage collected
    img_label2.pack()
    img_label2.place(x=150, y=450)
    
    # canvas = tk.Canvas(root, width=500, height=600)
    # canvas.place(x=300, y=100)
    # canvas.create_rectangle(0, 0, 700, 500, fill="light grey")

def search_restaurants():
    # This function can be expanded to actually perform a search
    global entry  # Access the global entry variable
    text = entry.get().strip()  # Get the text from the entry field
    if text:
        data_frame = pd.read_csv('data_frame.csv')
        search_query = text.split()
        restaurants, message = analyze_recommendation(data_frame, search_query)
        restaurant_1_name = restaurants['res_name'].values[0]
        restaurant_1_rating = restaurants['actual_rating'].values[0]
        restaurant_1_location = restaurants['location_link'].values[0]
        restaurant_1_time = restaurants['time'].values[0]
        restaurant_1_total_reviews = restaurants['total_no_reviews'].values[0]
        restaurant_1_link = restaurants['zomato_link'].values[0]
        restaurant_1_delivery_rating = restaurants['delivery_rating'].values[0]
        image_url_1 = "https://b.zmtcdn.com/data/pictures/chains/3/18974473/f0836fde6e4064e73c632c5f638c1c25.jpg?output-format=webp&fit=around%7C771.75:416.25&crop=771.75:416.25;*,*"
        image_url_2 = "https://b.zmtcdn.com/data/pictures/chains/3/18974473/f0836fde6e4064e73c632c5f638c1c25.jpg?output-format=webp&fit=around%7C771.75:416.25&crop=771.75:416.25;*,*"
        data = {
            'restaurant_name': restaurant_1_name,
            'expert_rating': restaurant_1_rating,
            'delivery_rating': restaurant_1_delivery_rating,
            'address': restaurant_1_location,
            'operating_time': restaurant_1_time,
            'total_reviews': restaurant_1_total_reviews,
            'zomato_link': restaurant_1_link,
            'url1': image_url_1,
            'url2': image_url_2
        }
    clear_window(data)

def main():
    global entry, root # Access the global entry and root variables

    # Create the main window
    root = tk.Tk()
    root.title("dinefinder.com")
    # Adjusting the initial size of the window
    root.geometry('650x600')  # Width x Height
    root.configure(bg='#f0eae1')

    logo_image = Image.open('logo.png')  # Ensure 'logo.png' is in the correct path
    logo_tk = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(root, image=logo_tk, bg='#f0eae1')
    logo_label.image = logo_tk  # Keep a reference
    logo_label.pack(pady=20)

    # Create a frame for better organization of widgets
    frame = tk.Frame(root)
    frame.pack(pady=0, padx=0)
    frame.configure(bg='#f0eae1')

    # Title & Subtitle label
    title = tk.Label(frame, text="Welcome! Please search for a place to eat.", font=("Times New Roman", 24, 'bold'), bg='#f0eae1')
    title.pack(pady=10)

    subtitle = tk.Label(frame, text="Type a restaurant name or a set of keywords.", font=("Times New Roman", 14), bg='#f0eae1')
    subtitle.pack(pady=(0,5))  # Smaller vertical padding to keep it close to the title

    # Search entry widget
    entry = tk.Entry(width=45, font=("Arial", 14), bd=2, relief=tk.FLAT)  
    entry.place(x=110, y=380)
    # Search button
    search_btn = tk.Button(text="Search", command=search_restaurants, font=("Arial", 12, 'bold'), bg='#c44536', fg='black', relief=tk.FLAT, padx=10, pady=5)
    search_btn.place(x=490, y=379, width=60, height=29)

    # 'Don't know what to eat?' button
    random_btn = tk.Button(text="Don't know what to eat?", command=clear_window, font=("Arial", 12), bg='#c44536', fg='black', relief=tk.FLAT, padx=10, pady=5)
    random_btn.place(x=230,y=450)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()