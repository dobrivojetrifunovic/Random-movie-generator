
import pandas as pd
import tkinter as tk
from random import choice


movies = pd.read_csv("movies.csv")

#print(movies['release_date'].head())
#print(movies.columns)
#print(movies['year'].head())
#print(movies.describe())


movies = movies.drop(columns=['homepage', 'id', 'keywords', 'original_language', 
'revenue', 'index', 'original_title', 'production_companies', 'production_countries', 'spoken_languages', 'overview', 'status', 'crew'])

#print(movies.shape[0])
movies['year'] = movies['release_date'].str[:4]

class MyGUI:

    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("650x500")
        self.root.title("Random movie generator")

        self.title = tk.Label(self.root, text="Welcome to random movie generator", font=('Arial', 25))
        self.title.pack(padx=10,pady=10)


        self.genre_label = tk.Label(self.root, text="Enter genre you want to watch", font=('Arial', 18))
        self.genre_label.pack(padx=40,pady=10)
        self.genre_entry = tk.Text(self.root, height=1, font=('Arial', 18))
        self.genre_entry.pack(padx=40,pady=10)


        self.rating_label = tk.Label(self.root, text="Enter minimal rating", font=('Arial', 18))
        self.rating_label.pack(padx=40,pady=10)
        self.rating_entry = tk.Text(self.root, height=1, font=('Arial', 18))
        self.rating_entry.pack(padx=40,pady=10)


        self.duration_label = tk.Label(self.root, text="Enter maximal duration", font=('Arial', 18))
        self.duration_label.pack(padx=40,pady=10)
        self.duration_entry = tk.Text(self.root, height=1, font=('Arial', 18))
        self.duration_entry.pack(padx=40,pady=10)


        self.button = tk.Button(self.root, text="Randomize", font=('Arial', 18), command = self.randomize)
        self.button.pack()


        self.output = tk.Text(self.root, font=('Arial', 18))
        self.output.pack(padx=10,pady=10)

        self.root.mainloop()


    def randomize(self):

        #Citamo unos korisnika
        genre = self.genre_entry.get('1.0', tk.END).strip()
        rating = float(self.rating_entry.get('1.0', tk.END).strip())
        duration = int(self.duration_entry.get('1.0', tk.END).strip())


        #Pretrazujemo odgovarajuce filmove
        filtered_movies = movies[
            (movies['vote_average'] > rating) &
            (movies['runtime'] < duration) &
            (movies['genres'].astype(str).str.contains(genre, na=False))
        ]

        self.output.delete('1.0', tk.END)  # Ocistimo prethodne rezultate

        #Proveravamo da li je uopste odgovarajuci film pronadjen
        if not filtered_movies.empty:
            movie = filtered_movies.sample(n=1).iloc[0]
            self.output.insert(tk.END, f"{movie['title']} ({movie['year']}) - {movie['vote_average']}\n")
        else:
            self.output.insert(tk.END, "No movies found matching criteria.\n")



MyGUI()