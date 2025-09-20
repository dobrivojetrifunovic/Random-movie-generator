
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from random import choice

try:
    movies = pd.read_csv("movies.csv")
except FileNotFoundError:
    print("Fajl movies.csv nije pronadjen.")
    exit()

print(len(movies))

# print(movies.describe())
# print(movies.isnull().sum().sum())


#movies2 = movies.fillna(value = 0)
#print(movies2.isnull().sum().sum())

#movies3 = movies.fillna(value=5)
#print(movies3)

#Filling Null Values
# Filling Null values with a previous value

#movies4 = movies.fillna(method = 'bfill') #pad or bfill
#print(movies4.isnull().sum())

#movies5 = movies.fillna(value = movies['popularity'].mean()) #max,min, mean
#print(movies5)

#-----------------------

#movies6 = movies.dropna(how='any')
#print(movies6)

#movies7 = movies.replace(to_replace = np.nan, value=875465)

#interpolate
#movies['popularity'] = movies['popularity'].interpolate(method = 'linear')

#print(movies['release_date'].head())
#print(movies.columns)
#print(movies['year'].head())
#print(movies.describe())


#Odbacivanje kolone koje ne zelim da analiziram
movies = movies.drop(columns=['homepage', 'id', 'keywords', 'original_language', 
'revenue', 'index', 'original_title', 'production_companies', 'production_countries', 'spoken_languages', 'overview', 'status', 'crew', 'tagline'])


#prikazuje broj redova
#print(movies.shape[0])
#print(movies['genres'].head())


movies = movies.dropna(subset=['runtime'])
movies = movies.dropna(subset=['release_date'])
movies['genres'] = movies['genres'].fillna('Unknown')
movies['cast'] = movies['cast'].fillna("Unknown")
movies['director'] = movies['director'].fillna("Unknown")
#Dodavanje kolone za godinu u kojoj je izasao odredjeni film
movies['year'] = movies['release_date'].str[:4]
movies['year'] = movies['year'].astype(int)

#print(movies.size)

movies = movies[movies["vote_average"] > 0.0]
movies = movies[movies["runtime"] > 0.0]

print(len(movies))

#print(movies['vote_average'].min())

#print(movies.info())

#print(movies['cast'].head())
#print(movies.isnull().sum())
#print(movies.isnull().sum().sum())

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

axs[0, 0].hist(movies['vote_average'], bins=20, color='blue', edgecolor='black')
axs[0, 0].set_title('Distribucija ocena filmova')
axs[0, 0].set_xlabel('Ocena')
axs[0, 0].set_ylabel('Broj filmova')

axs[0, 1].hist(movies['runtime'], bins=30, color='green', edgecolor='black')
axs[0, 1].set_title('Distribucija trajanja filmova')
axs[0, 1].set_xlabel('Trajanje (min)')
axs[0, 1].set_ylabel('Broj filmova')

movies_by_year = movies['year'].value_counts().sort_index()
axs[1, 0].plot(movies_by_year.index, movies_by_year.values, color='orange')
axs[1, 0].set_title('Broj filmova po godinama')
axs[1, 0].set_xlabel('Godina')
axs[1, 0].set_ylabel('Broj filmova')
axs[1, 0].grid(True)

avg_rating_by_year = movies.groupby('year')['vote_average'].mean()
axs[1, 1].plot(avg_rating_by_year.index, avg_rating_by_year.values, color='purple')
axs[1, 1].set_title('Prosecna ocena po godini')
axs[1, 1].set_xlabel('Godina')
axs[1, 1].set_ylabel('Prosecna ocena')


# avg_rating_by_year
# axs[1, 1].plot(movies)


plt.tight_layout()
plt.show()


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
        self.output.delete('1.0', tk.END)  # Ocistimo prethodne rezultate

        try:
            #Citamo unos korisnika
            genre = self.genre_entry.get('1.0', tk.END).strip()
            rating = float(self.rating_entry.get('1.0', tk.END).strip())
            duration = int(self.duration_entry.get('1.0', tk.END).strip())


            #Pretrazujemo odgovarajuce filmove
            filtered_movies = movies[
                (movies['vote_average'] >= rating) &
                (movies['runtime'] <= duration) &
                (movies['genres'].astype(str).str.contains(genre, na=False))
            ]

            #Proveravamo da li je uopste odgovarajuci film pronadjen
            if not filtered_movies.empty:
                movie = filtered_movies.sample(n=1).iloc[0]
                self.output.insert(tk.END, f"{movie['title']} ({movie['year']}) - {movie['vote_average']}\n")
            else:
                self.output.insert(tk.END, "No movies found matching criteria.\n")
            
        except ValueError:
            self.output.insert(tk.END, "Unos mora biti broj za ocenu i trajanje filma.")
        except Exception as e:
            self.output.insert(tk.END, f"Neocekivana greska: {str(e)}\n")


MyGUI()