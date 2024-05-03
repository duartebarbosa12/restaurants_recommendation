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

def clear_window(data, data2, data3):
    # Clear the entire window
    global root  # Access the global root variable
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg='#f0eae1')
    root.geometry('1300x900')

    # Add a new title
    title = tk.Label(root, text="Based on the information you provided, here's what we have found:", font=("Times New Roman", 24, 'italic'), bg='#f0eae1')
    title.pack(pady=(50,20))
    subtitle = tk.Label(root, text=data['restaurant_name'], font=("Times New Roman", 50, 'bold'), bg='#f0eae1')
    subtitle.pack(pady=10)
    text = tk.Label(root, text=data['expert_rating'], font=("Times New Roman", 36), bg='#f0eae1')
    text.pack(pady=10)
    text.place(x=1000, y=240)
    text2 = tk.Label(root, text="Our Expert Rating", font=("Times New Roman", 24), bg='#f0eae1')
    text2.pack(pady=10)
    text2.place(x=935, y=290)
    text3 = tk.Label(root, text=data['delivery_rating'], font=("Times New Roman", 36), bg='#f0eae1')
    text3.pack(pady=10)
    text3.place(x=810, y=240)
    text4 = tk.Label(root, text="Delivery Rating", font=("Times New Roman", 24), bg='#f0eae1')
    text4.pack(pady=10)
    text4.place(x=750, y=290)

    about = tk.Label(root, text="About", font=("Times New Roman", 28, 'bold', 'italic'), bg='#f0eae1')
    about.place(x=650, y=350)

    description = tk.Label(root, text=data['description'], font=("Times New Roman", 18), bg='#f0eae1', wraplength=500, justify='left', anchor='w')
    description.place(x=650, y=400)

    def open_link_1(url):
        import webbrowser
        webbrowser.open(url)

    link_label = tk.Label(root, text="Restaurant Location", font=("Helvetica", 18, 'underline'), fg="blue", bg='#f0eae1', cursor="hand2")
    link_label.place(x=650, y=600)
    link_label.bind("<Button-1>", lambda e: open_link_1(data['address']))

    time_label = tk.Label(root, text=data['operating_time'], font=("Times New Roman", 18), bg='#f0eae1')
    time_label.place(x=650, y=500)

    def open_link_2(url):
        import webbrowser
        webbrowser.open(url)

    link_label = tk.Label(root, text="View Restaurant on Zomato", font=("Helvetica", 18, 'underline'), fg="blue", bg='#f0eae1', cursor="hand2")
    link_label.place(x=650, y=650)
    link_label.bind("<Button-1>", lambda e: open_link_2(data['zomato_link']))
    
    response = requests.get(data['url1'])
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    max_size = (400, 550)
    img.thumbnail(max_size)
    img_tk = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=img_tk, borderwidth=1)
    img_label.image = img_tk  # Keep a reference to the image to prevent it from being garbage collected
    img_label.pack()
    img_label.place(x=150, y=250)
    
    response2 = requests.get(data['url2'])
    img_data2 = response2.content
    img2 = Image.open(BytesIO(img_data2))
    img2.thumbnail(max_size)
    img_tk2 = ImageTk.PhotoImage(img2)
    img_label2 = tk.Label(root, image=img_tk2, borderwidth=1)
    img_label2.image = img_tk2  # Keep a reference to the image to prevent it from being garbage collected
    img_label2.pack()
    img_label2.place(x=150, y=500)
    
    # Arrow
    empty = []
    canvas = tk.Canvas(root, width=60, height=50, bg='#f0eae1', highlightthickness=0)
    canvas.pack(pady=10, padx=40, anchor='se', side='bottom')
    canvas.create_line(10, 10, 50, 10, arrow=tk.LAST, fill="black", width=5)
    canvas.bind("<Button-1>", lambda e: clear_window(data2, data3, empty))


def get_restaurant_info(restaurant_name, data_frame):
    restaurant_row = data_frame[data_frame['res_name'] == restaurant_name]
    if not restaurant_row.empty:
        info = f"The restaurant {restaurant_row['res_name'].values[0]} is known for its {restaurant_row['bag_of_words'].values[0]}. "
        info += f"Located at {restaurant_row['res_loc'].values[0]}, it has a rating of {restaurant_row['actual_rating'].values[0]} "
        info += f"with {restaurant_row['total_no_reviews'].values[0]} reviews. Delivery rating is {restaurant_row['delivery_rating'].values[0]}."
        return info
    else:
        return "Restaurant information not available."
        
def search_restaurants():
    # This function can be expanded to actually perform a search
    global entry  # Access the global entry variable
    text = entry.get().strip()  # Get the text from the entry field
    if text:
        data_frame = pd.read_csv('restaurant_details.csv')
        search_query = text.split()
        restaurants, message = analyze_recommendation(data_frame, search_query)

        # First restaurant data
        restaurant_1_name = restaurants['res_name'].values[0]
        restaurant_1_rating = restaurants['actual_rating'].values[0]
        restaurant_1_location = restaurants['location_link'].values[0]
        restaurant_1_location = restaurant_1_location.replace("[", "").replace("]", "").replace("'", "")
        restaurant_1_time = restaurants['time'].values[0]
        restaurant_1_total_reviews = restaurants['total_no_reviews'].values[0]
        restaurant_1_link = restaurants['zomato_link'].values[0]
        restaurant_1_delivery_rating = restaurants['delivery_rating'].values[0]
        image_url_1 = restaurants['first_image'].values[0]
        image_url_2 = restaurants['second_image'].values[0]
        restaurant_info1 = get_restaurant_info(restaurant_1_name, data_frame)

        data = {
            'restaurant_name': restaurant_1_name,
            'expert_rating': restaurant_1_rating,
            'delivery_rating': restaurant_1_delivery_rating,
            'address': restaurant_1_location,
            'operating_time': restaurant_1_time,
            'total_reviews': restaurant_1_total_reviews,
            'zomato_link': restaurant_1_link,
            'url1': image_url_1,
            'url2': image_url_2,
            'description': restaurant_info1
        }
        
        # Second restaurant data
        restaurant_2_name = restaurants['res_name'].values[1]
        restaurant_2_rating = restaurants['actual_rating'].values[1]
        restaurant_2_location = restaurants['location_link'].values[1]
        restaurant_2_location = restaurant_2_location.replace("[", "").replace("]", "").replace("'", "")
        restaurant_2_time = restaurants['time'].values[1]
        restaurant_2_total_reviews = restaurants['total_no_reviews'].values[1]
        restaurant_2_link = restaurants['zomato_link'].values[1]
        restaurant_2_delivery_rating = restaurants['delivery_rating'].values[1]
        image_url_3 = restaurants['first_image'].values[1]
        image_url_4 = restaurants['second_image'].values[1]
        restaurant_info2 = get_restaurant_info(restaurant_2_name, data_frame)
        data2 = {
            'restaurant_name': restaurant_2_name,
            'expert_rating': restaurant_2_rating,
            'delivery_rating': restaurant_2_delivery_rating,
            'address': restaurant_2_location,
            'operating_time': restaurant_2_time,
            'total_reviews': restaurant_2_total_reviews,
            'zomato_link': restaurant_2_link,
            'url1': image_url_3,
            'url2': image_url_4,
            'description': restaurant_info2
        }
    
        # Third restaurant data
        restaurant_3_name = restaurants['res_name'].values[2]
        restaurant_3_rating = restaurants['actual_rating'].values[2]
        restaurant_3_location = restaurants['location_link'].values[2]
        restaurant_3_location = restaurant_3_location.replace("[", "").replace("]", "").replace("'", "")
        restaurant_3_time = restaurants['time'].values[2]
        restaurant_3_total_reviews = restaurants['total_no_reviews'].values[2]
        restaurant_3_link = restaurants['zomato_link'].values[2]
        restaurant_3_delivery_rating = restaurants['delivery_rating'].values[2]
        image_url_5 = restaurants['first_image'].values[2]
        image_url_6 = restaurants['second_image'].values[2]
        restaurant_info3 = get_restaurant_info(restaurant_3_name, data_frame)
        data3 = {
            'restaurant_name': restaurant_3_name,
            'expert_rating': restaurant_3_rating,
            'delivery_rating': restaurant_3_delivery_rating,
            'address': restaurant_3_location,
            'operating_time': restaurant_3_time,
            'total_reviews': restaurant_3_total_reviews,
            'zomato_link': restaurant_3_link,
            'url1': image_url_5,
            'url2': image_url_6,
            'description': restaurant_info3
        }
    clear_window(data, data2, data3)
    
def search_restaurants_not_knowing_what_to_eat():
    global entry  # Access the global entry variable
    text = entry.get().strip()
    data_frame = pd.read_csv('restaurant_details.csv')
    
    if text:
        restaurants = recommendation(data_frame, text)
        print(restaurants)
        
        # First restaurant data
        restaurant_1_name = restaurants['res_name'].values[0]
        restaurant_1_rating = restaurants['actual_rating'].values[0]
        restaurant_1_location = restaurants['location_link'].values[0]
        restaurant_1_location = restaurant_1_location.replace("[", "").replace("]", "").replace("'", "")
        restaurant_1_time = restaurants['time'].values[0]
        restaurant_1_total_reviews = restaurants['total_no_reviews'].values[0]
        restaurant_1_link = restaurants['zomato_link'].values[0]
        restaurant_1_delivery_rating = restaurants['delivery_rating'].values[0]
        image_url_1 = restaurants['first_image'].values[0]
        image_url_2 = restaurants['second_image'].values[0]
        description = get_restaurant_info(restaurant_1_name, data_frame)
        data = {
            'restaurant_name': restaurant_1_name,
            'expert_rating': restaurant_1_rating,
            'delivery_rating': restaurant_1_delivery_rating,
            'address': restaurant_1_location,
            'operating_time': restaurant_1_time,
            'total_reviews': restaurant_1_total_reviews,
            'zomato_link': restaurant_1_link,
            'url1': image_url_1,
            'url2': image_url_2,
            'description': description
        }
        
        # Second restaurant data
        restaurant_2_name = restaurants['res_name'].values[1]
        restaurant_2_rating = restaurants['actual_rating'].values[1]
        restaurant_2_location = restaurants['location_link'].values[1]
        restaurant_2_location = restaurant_2_location.replace("[", "").replace("]", "").replace("'", "")
        restaurant_2_time = restaurants['time'].values[1]
        restaurant_2_total_reviews = restaurants['total_no_reviews'].values[1]
        restaurant_2_link = restaurants['zomato_link'].values[1]
        restaurant_2_delivery_rating = restaurants['delivery_rating'].values[1]
        image_url_3 = restaurants['first_image'].values[1]
        image_url_4 = restaurants['second_image'].values[1]
        description = get_restaurant_info(restaurant_2_name, data_frame)
        data2 = {
            'restaurant_name': restaurant_2_name,
            'expert_rating': restaurant_2_rating,
            'delivery_rating': restaurant_2_delivery_rating,
            'address': restaurant_2_location,
            'operating_time': restaurant_2_time,
            'total_reviews': restaurant_2_total_reviews,
            'zomato_link': restaurant_2_link,
            'url1': image_url_3,
            'url2': image_url_4,
            'description': description
        }
        
        # Third restaurant data
        restaurant_3_name = restaurants['res_name'].values[2]
        restaurant_3_rating = restaurants['actual_rating'].values[2]
        restaurant_3_location = restaurants['location_link'].values[2]
        restaurant_3_location = restaurant_3_location.replace("[", "").replace("]", "").replace("'", "")
        restaurant_3_time = restaurants['time'].values[2]
        restaurant_3_total_reviews = restaurants['total_no_reviews'].values[2]
        restaurant_3_link = restaurants['zomato_link'].values[2]
        restaurant_3_delivery_rating = restaurants['delivery_rating'].values[2]
        image_url_5 = restaurants['first_image'].values[2]
        image_url_6 = restaurants['second_image'].values[2]
        description = get_restaurant_info(restaurant_3_name, data_frame)
        data3 = {
            'restaurant_name': restaurant_3_name,
            'expert_rating': restaurant_3_rating,
            'delivery_rating': restaurant_3_delivery_rating,
            'address': restaurant_3_location,
            'operating_time': restaurant_3_time,
            'total_reviews': restaurant_3_total_reviews,
            'zomato_link': restaurant_3_link,
            'url1': image_url_5,
            'url2': image_url_6,
            'description': description
        }
    clear_window(data, data2, data3)
        
        

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
    random_btn = tk.Button(text="Don't know what to eat?", command=search_restaurants_not_knowing_what_to_eat, font=("Arial", 12), bg='#c44536', fg='black', relief=tk.FLAT, padx=10, pady=5)
    random_btn.place(x=230,y=450)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()