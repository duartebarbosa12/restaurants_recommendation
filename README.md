# restaurants_recommendation
This project was developed for our AI Machine-Learning and Analytics class.

Recommendation algorithm for restaurants based on sentiment analysis and cosine similarity scores. The algorithm is designed to use the zomato API (although right now is only working with a small dataset mocking the API request), and recommend a restaurant to the user based on the inputs.

We have designed a small UI using tkinter to interact with the use to register the user's input and display the recommendation. The program uses a DistilBERT model to perform sentiment analysis on thousands of restaurant reviews to create a new rating for this restaurant. It then uses an encoder together with the cosine similarity to match what the user is looking for with the database, always ensuring a high-rating restaurant is recommended.

The following are the porpuses of the files:
- pipeline.py: from a zomate API request, process, compute the rating, and perform cosine similarity on restaurants, leaving the data ready and sorted for the user to display. All the more technical parts of the code are here.
- restaurant_details.json: the initial small dataset comprehending of 50 restaurants in Surat, India, that was used to mock the API, in raw format
- restaurant_details.csv: curated and ready to use dataset after being passed through pipeline.py
- restaurants2.ipynb: jupyter notebook where code was tried
- tinker.py: GUI design and implementation


To use, please download all files except from Notebook2.ipynb and run tinker.py through python
