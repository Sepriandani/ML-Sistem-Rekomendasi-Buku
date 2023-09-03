# -*- coding: utf-8 -*-
"""MLT_Sistem Rekomendasi Buku_Collaboarative Filtering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_C9f5bphMiFe5DlPfS9qiOWM1DLM9fs3

# **Data Understanding**

## **Data Loading**

Dataset yang digunakan pada proyek ini, merupakan data yang tersedia pada situs penyedia data [Kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)

Disini saya mengunakan API untuk mendapatkan data
"""

!pip install kaggle

! mkdir ~/.kaggle

! cp kaggle.json ~/.kaggle/

! chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d arashnic/book-recommendation-dataset

"""Import library yang dibutuhkan"""

import zipfile
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

"""Karna data yang diperoleh dari API berupa file .zip, maka perlu de extrak terlebih dahulu"""

local_zip = '/content/book-recommendation-dataset.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content')
zip_ref.close()

"""Setelah di extrak terdapat 3 berkas csv diantaranya yaitu Books.csv , Ratings.csv , dan Users.csv

Selanjutnya kita akan buka dengan bantuan pandas untuk melihat isi dari masing-masing berkas csv tersebut.
"""

books = pd.read_csv('/content/Books.csv')
ratings = pd.read_csv('/content/Ratings.csv')
users = pd.read_csv('/content/Users.csv')

"""## **Exploratory Data Analysis**

Setelah dataset diperoleh, selajutnya perlu dilakukan explorasi pada data agar dapat memperoleh pemahaman terhadap data yang digunakan

#### **Books Dataset**

Explorasi data `Books.csv`
"""

books

"""Dari tabel diketahui bahwa dataset `Books.cvs` mempunyai 271.360 baris dan 8 kolom. untuk mendapat informasi yang lengkap kita perlu menjalankan fungsi `books.info()`"""

books.info()

"""Setelah fungsi `books.info()` dijalankan diketahui bahwa semua kolom mempunyai tipe data `object`. kolom tersbut terdiri dari:

- `ISBN` : berisi kode ISBN dari buku
- `Book-Title` : berisi judul buku
- `Book-Author` : berisi penulis buku
- `Year-Of-Publication` : tahun terbit buku
- `Publisher` : penerbit buku
- `Image-URL-S` : URL menuju gambar buku berukuran kecil
- `Image-URL-M` : URL menuju gambar buku berukuran sedang
- `Image-URL-L` : URL menuju gambar buku berukuran besar

Selanjutnya cek apakah terdapat missing value pada data
"""

books.isnull().sum()

"""Dari uraian diatas diketahui bahwa kolom `Book-Author` terdapat 1 missing value, `Publisher` terdapat 2 missing value, dan `Image-URL-L` terdapat 3 missing value

#### **Users Dataset**

Explorasi data `Users.csv`
"""

users

"""Dari tabel diketahui bahwa dataset `Books.cvs` mempunyai 278.858 baris dan 3 kolom. untuk mendapat informasi yang lengkap kita perlu menjalankan fungsi `users.info()`"""

users.info()

"""Setelah fungsi `users.info()` dijalankan diketahui bahwa kolom terdiri dari:

- `User-ID` : berisi ID unik pengguna (tipe data Integer)
- `Location` : berisi data lokasi pengguna (tipe data object)
- `Age` : berisi data usia pengguna (tipe data float)

Selanjutnya cek apakah terdapat missing value pada data
"""

users.isnull().sum()

"""Dari uraian diatas diketahui bahwa kolom `Age` terdapat missing value yang cukup banyak yaitu 110.762 missing value

#### **Ratings Dataset**

Explorasi data `Ratings.csv`
"""

ratings

"""Dari tabel diketahui bahwa dataset `Ratings.cvs` mempunyai 1.149.780 baris dan 3 kolom. untuk mendapat informasi yang lengkap kita perlu menjalankan fungsi `ratings.info()`"""

ratings.info()

"""Setelah fungsi `users.info()` dijalankan diketahui bahwa kolom terdiri dari:

- `User-ID` : berisi ID unik pengguna (tipe data Integer)
- `ISBN` : berisi kode ISBN buku yang diberi rating oleh pengguna (tipe data object)
- `Book-Rating` : erisi nilai rating yang diberikan oleh penggun (tipe data integer)

Selanjutnya cek apakah terdapat missing value pada data
"""

ratings.isnull().sum()

"""Dari uraian diatas tidak terdapat missing value pada data `Ratings.csv`

Karna pada proyek kali ini mengunakan metode **Collaborative Filtering**, kita akan berfokus pada dataset `ratings` oleh karna itu kita perlu melakukan explorasi lebih lanjut untuk benar-benar memahami informasi serta kualitas data.

kita perlu melihat berapa jumlah buku berdasarkan rating yang diberikan penguna
"""

ratings.groupby('Book-Rating').count()

"""Dari tabel diatas diketahui bahwa banyak penguna yang memberikan rating 0. untuk dapat memahami data lebih jelas, mari kita plot data tersebut pada bar chart"""

rating_counter = ratings.groupby('Book-Rating').count()
plt.figure(figsize=(10,5))
plt.title('Jumlah Rating Buku yang Diberikan Pengguna')
plt.xlabel('Rating')
plt.ylabel('Jumlah Buku')
plt.bar(rating_counter.index, rating_counter['ISBN'])
plt.grid(True)
plt.show()

"""Dapat dilihat pada bar chart bahwa terjadi ke tidak seimbangan pada data, jika hal ini tidak diatasi maka akan berpengaruh terhadap performa model nantinya. oleh karna itu kita akan melakukan Data Preparation terlebih dahulu

# **Data Preparation**

Sebelum data dimasukan ke dalam model, data harus melalui tahap Data Preparation terlebih dahulu agar data dapat diterima baik oleh model. berikut teknik yang digunakan :

## **Mengatasi data yang tidak seimbang**

Pada bar chart di atas dapat diketahui bahwa data tidak seimbang dan banyak pengguna yang memberikan rating 0, oleh karna itu kita akan menghapus data dengan rating 0
"""

ratings.drop(ratings[ratings["Book-Rating"] == 0].index, inplace=True)
ratings

"""Setelah data dengan `Book-Rating` 0 dihapus jumlah data yang tersedia yaitu 433.671.

Mari plot data mengunakan bar chart lagi, apakah data sudah lebih baik dari sebelumnya
"""

rating_counter = ratings.groupby('Book-Rating').count()
plt.figure(figsize=(10,5))
plt.title('Jumlah Rating Buku yang Diberikan Pengguna')
plt.xlabel('Rating')
plt.ylabel('Jumlah Buku')
plt.bar(rating_counter.index, rating_counter['ISBN'])
plt.grid(True)
plt.show()

"""## **Encoding Data**

Encoding dilakukan untuk menyandikan `User-ID` dan `ISBN` ke dalam indeks integer
"""

# Mengubah userID menjadi list tanpa nilai yang sama
user_ids = ratings['User-ID'].unique().tolist()
 
# Melakukan encoding userID
user_to_user_encoded = {x: i for i, x in enumerate(user_ids)}
 
# Melakukan proses encoding angka ke ke userID
user_encoded_to_user = {i: x for i, x in enumerate(user_ids)}

# Mengubah ISBN menjadi list tanpa nilai yang sama
isbn_list = ratings['ISBN'].unique().tolist()
 
# Melakukan encoding ISBN
isbn_to_isbn_encoded = {x: i for i, x in enumerate(isbn_list)}
 
# Melakukan proses encoding angka ke ISBN
isbn_encoded_to_isbn = {i: x for i, x in enumerate(isbn_list)}

"""Setelah itu hasil dari encoding akan dimapping ke dataframe `ratings`"""

# Mapping userID ke dataframe user
ratings['user'] = ratings['User-ID'].map(user_to_user_encoded)

# Mapping ISBN ke dataframe book
ratings['book'] = ratings['ISBN'].map(isbn_to_isbn_encoded)

ratings

"""Sekarang dataset `ratings` mempunya 5 kolom yaitu `User-ID`, `ISBN`, `Book-Rating`, `user`, dan `book`"""

ratings.info()

"""## **Randomize Dataset**

Pada tahap ini kita akan mengacak datanya terlebih dahulu agar distribusinya menjadi random.
"""

# Mengacak dataset
df = ratings.sample(frac=1, random_state=42)
df

"""## **Data Standardization and Splitting**

Setelah datanya diacak, lakukan standarisasi nilai rating yang sebelumnya berada di rentang 0 hingga 10 kini diubah ke rentang 0 hingga 1 untuk mempermudah dalam proses training
"""

# Mendapatkan jumlah user
num_users = len(user_to_user_encoded)
print(num_users)
 
# Mendapatkan jumlah resto
num_isbn = len(isbn_encoded_to_isbn)
print(num_isbn)
 
# Mengubah rating menjadi nilai float
df['Book-Rating'] = df['Book-Rating'].values.astype(np.float32)
 
# Nilai minimum Book-Rating
min_rating = min(df['Book-Rating'])
 
# Nilai maksimal Book-Rating
max_rating = max(df['Book-Rating'])
 
print('Number of User: {}, Number of ISBN: {}, Min Rating: {}, Max Rating: {}'.format(
    num_users, num_isbn, min_rating, max_rating
))

"""## **Membagi Data untuk Training dan Validasi**

kemudian dataset dibagi menjadi 2 bagian, yaitu data yang akan digunakan untuk melatih model (sebesar 90%) dan data untuk memvalidasi model (sebesar 10%).
"""

# Membuat variabel x untuk mencocokkan data user dan book menjadi satu value
x = df[['user', 'book']].values
 
# Membuat variabel y untuk membuat rating dari hasil 
y = df['Book-Rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
 
# Membagi menjadi 90% data train dan 10% data validasi
train_indices = int(0.9 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)
 
print(x, y)

"""Data telah siap untuk dimasukkan ke dalam model.

# **Model Development**

## **Membuat Kelas RecommenderNet**
"""

class RecommenderNet(tf.keras.Model):
 
  # Insialisasi fungsi
  def __init__(self, num_users, num_isbn, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_users = num_users
    self.num_isbn = num_isbn
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding( # layer embedding user
        num_users,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.user_bias = layers.Embedding(num_users, 1) # layer embedding user bias
    self.book_embedding = layers.Embedding( # layer embeddings book
        num_isbn,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.book_bias = layers.Embedding(num_isbn, 1) # layer embedding book bias
 
  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0]) # memanggil layer embedding 1
    user_bias = self.user_bias(inputs[:, 0]) # memanggil layer embedding 2
    book_vector = self.book_embedding(inputs[:, 1]) # memanggil layer embedding 3
    book_bias = self.book_bias(inputs[:, 1]) # memanggil layer embedding 4
 
    dot_user_book = tf.tensordot(user_vector, book_vector, 2) 
 
    x = dot_user_book + user_bias + book_bias
    
    return tf.nn.sigmoid(x) # activation sigmoid

"""## **Hyperparameter Tuning**

Agar mendapatkan hasil model yang optimal, maka dalam proyek ini menggunakan bantuan library `optuna` untuk melakukan hyperparameter tuning atau pencarian nilai hyperparameter yang terbaik, dalam hal ini adalah nilai `embedding_size`.
"""

!pip install optuna

import optuna
def objective(trial):
    tf.keras.backend.clear_session()
    model = RecommenderNet(num_users=num_users, num_isbn=num_isbn, embedding_size=trial.suggest_int('embedding_size', 1, 15))

    # model compile
    model.compile(
        loss = tf.keras.losses.BinaryCrossentropy(),
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        metrics=[tf.keras.metrics.RootMeanSquaredError()]
    )

    model.fit(
        x = x_train,
        y = y_train,
        batch_size=200,
        epochs = 1,
        validation_data = (x_val, y_val)
    )
    
    y_pred= model.predict(x_val)

    return mean_squared_error(y_val, y_pred, squared=False)

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=15, timeout=500)

print("Number of finished trials: {}".format(len(study.trials)))

print("Best trial:")
trial = study.best_trial

print("  Value: {}".format(trial.value))

print("  Params: ")
for key, value in trial.params.items():
    print("    {}: {}".format(key, value))

"""Hasil hypermeter turning menunjukan bahwa nilai `embedding_size` yang paling optimal yaitu 1

Model ini menggunakan Binary Crossentropy untuk menghitung loss function, Adam (Adaptive Moment Estimation) sebagai optimizer, dan root mean squared error (RMSE) sebagai metrics evaluation.
"""

tf.keras.backend.clear_session()

# Menerapkan nilai parameter paling optimal dari optuna
BEST_EMBEDDING_SIZE = 1

model = RecommenderNet(num_users, num_isbn, BEST_EMBEDDING_SIZE)

model.compile(
    loss = tf.keras.losses.BinaryCrossentropy(),
    optimizer = keras.optimizers.Adam(learning_rate=0.001),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

"""## **Training Model**"""

history = model.fit(
    x = x_train,
    y = y_train,
    batch_size=64,
    epochs = 10,
    validation_data = (x_val, y_val)
)

"""# **Evaluasi**

## **Visualisasi Metrik**

Untuk melihat visualisasi proses training, mari kita plot metrik evaluasi dengan matplotlib.
"""

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.grid(True)
plt.show()

"""Perhatikanlah, Dari proses ini, kita memperoleh nilai error akhir sebesar sekitar 0.14 dan error pada data validasi sebesar 0.18. Nilai tersebut cukup bagus untuk sistem rekomendasi. Mari kita cek, apakah model ini bisa membuat rekomendasi dengan baik?

## **Mendapatkan Rekomendasi**

Untuk mendapatkan rekomendasi buku, pertama kita ambil sampel user secara acak dan definisikan variabel book_not_read yang merupakan daftar buku yang belum pernah dikunjungi oleh pengguna. Anda mungkin bertanya-tanya, mengapa kita perlu menentukan daftar book_not_read? Hal ini karena daftar book_not_read inilah yang akan menjadi buku yang kita rekomendasikan.

Sebelumnya, pengguna telah memberi rating pada beberapa buku yang telah mereka kunjungi. Kita menggunakan rating ini untuk membuat rekomendasi buku yang mungkin cocok untuk pengguna. Nah, buku yang akan direkomendasikan tentulah buku yang belum pernah dikunjungi oleh pengguna. Oleh karena itu, kita perlu membuat variabel book_not_read sebagai daftar buku untuk direkomendasikan pada pengguna.

Variabel book_not_read diperoleh dengan menggunakan operator bitwise (~) pada variabel book_read_by_user.
"""

books_df = books
df = pd.read_csv('Ratings.csv')
 
# Mengambil sample user
user_id = df['User-ID'].sample(1).iloc[0]
book_read_by_user = df[df['User-ID'] == user_id]
 
# Operator bitwise (~), bisa diketahui di sini https://docs.python.org/3/reference/expressions.html 
book_not_read = books_df[~books_df['ISBN'].isin(book_read_by_user.ISBN.values)]['ISBN']
book_not_read = list(
    set(book_not_read)
    .intersection(set(isbn_to_isbn_encoded.keys()))
)
 
book_not_read = [[isbn_to_isbn_encoded.get(x)] for x in book_not_read]
user_encoder = user_to_user_encoded.get(user_id)
user_book_array = np.hstack(
    ([[user_encoder]] * len(book_not_read), book_not_read)
)

"""Selanjutnya, untuk memperoleh rekomendasi buku, gunakan fungsi model.predict() dari library Keras"""

ratings = model.predict(user_book_array).flatten()
 
top_ratings_indices = ratings.argsort()[-10:][::-1]
recommended_book_isbns = [
    isbn_encoded_to_isbn.get(book_not_read[x][0]) for x in top_ratings_indices
]
 
print('Showing recommendations for users: {}'.format(user_id))
print('===' * 9)
print('Books with high ratings from user')
print('----' * 8)
 
top_book_user = (
    book_read_by_user.sort_values(
        by = 'Book-Rating',
        ascending=False
    )
    .head(5)
    .ISBN.values
)
 
book_df_rows = books_df[books_df['ISBN'].isin(top_book_user)]
for row in book_df_rows.itertuples():
    print(row._3, "-", row._2)
 
print('----' * 8)
print('Top 10 book recommendation')
print('----' * 8)
 
recommended_books = books_df[books_df['ISBN'].isin(recommended_book_isbns)]
for row in recommended_books.itertuples():
    print(row._3, "-", row._2)

"""hasil di atas adalah rekomendasi untuk user dengan id 155027. Dari output tersebut, kita dapat membandingkan antara buku dengan rating tertinggi dari user dan Top 10 buku recommendation untuk user. """