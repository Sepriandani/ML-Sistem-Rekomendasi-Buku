# Laporan Proyek Machine Learning - Seprian Dani
# _Sistem Rekomendasi Buku dengan Colaborative Filtering_

## Project Overview

### Latar Belakang
Membaca buku merupakan salah satu cara bagi setiap orang untuk mendapatkan ilmu pengetahuan dan wawasan baru mengenai banyak hal. Informasi mengenai beragam jenis buku saat ini telah tersebar luas di internet sehingga dapat diakses oleh banyak orang. Meski informasi mengenai beragam jenis buku telah beredar di internet, namun minat baca di Indonesia masih tergolong rendah. Menurut data riset bertajuk World’s Most Literate Nations Ranked yang dilakukan oleh Central Connecticut State Univesity pada tahun 2016, Indonesia dinyatakan menduduki peringkat ke-60 dari 61 negara soal minat membaca (Devega, 2017). Hasil riset ini menunjukkan bahwa minat baca di Indonesia masih terbilang cukup rendah dibandingkan dengan negara lain termasuk dari Singapura dan Malaysia. Kondisi ini tentu akan berpengaruh terhadap pemahaman dalam ilmu pengetahuan serta teknologi untuk dapat menghasilkan produk-produk berkualitas. Selain itu, efek yang lebih besar atas keengganan untuk minat membaca pada generasi muda ini akan merugikan negara yang dapat kehilangan aset penyumbang dari segi sumber daya manusia untuk kemajuan bangsa yang berkualitas dan mempunyai produktifitas yang tinggi.
Salah satu upaya untuk dapat meningkatkan minat baca kepada masyarakat adalah dengan menyediakan bahan bacaan yang variatif, sehingga mendukung pembelajaran dan mendorong kepada masyarakat untuk menyukai buku. Hingga saat ini, terdapat banyak sekali media yang menyediakan layanan kepada masyarakat untuk mendapatkan bacaan buku yang variatif, seperti Gramedia, Togamas, Berdikari dan lain sebagainya. Masyarakat dapat mengakses beragam jenis buku yang tersedia pada penyedia layanan buku tersebut. Dengan banyaknya informasi buku yang tersebar luas dan untuk memudahkan pembaca buku dalam menemukan buku yang sesuai dengan kriteria yang diinginkan, penerapan sistem rekomendasi dapat dimanfaatkan. Sehingga pengguna dapat dengan mudah mendapatkan referensi baru mengenai buku yang bisa dibaca sesuai dengan kategori buku yang diminati oleh pembaca sebelumnya. Selain itu, sistem rekomendasi juga memiliki peran penting pada banyak layanan aplikasi online. Performa sistem rekomendasi dapat berdampak pada kesuksesan komersial pada banyak perusahaan dalam hal pendapatan dan kepuasan para pengguna. Dengan itu penulis akan membuat sebuah sistem rekomendasi buku dengan metode Collaborative Filtering

## Business Understanding

### Problem Statements

Berdasarkan pada latar belakang di atas, permasalahan yang dapat diselesaikan pada proyek ini adalah sebagai berikut:
- Dengan data yang tersedia, bagaimana agar dapat memberikan rekomendasi buku yang mungkin akan dibaca atau dibeli oleh pengguna menggunakan metode Collaborative Filtering?
- Fitur apa yang paling baik dipakai untuk metode Collaborative Filtering ?

### Goals

Tujuan dibuatnya proyek ini adalah sebagai berikut:
- Menghasilkan rekomendasi buku kepada pengguna berdasarkan rating buku yang telah diberikan sebelumnya oleh pengguna dengan metode Collaborative Filtering.
- Melakukan explorasi data agar mendapatkan mengetahui fitur yang paling baik dipakai untuk metode Collaborative Filtering

### Solution statements

Solusi yang akan diterapkan pada proyek ini adalah menggunakan metode Collaborative Filtering. Agar goals diatas terpenuhi dilakukan beberapa tahapan sebagai berikut:

- Melakukan analisa, eksplorasi, dan pemrosesan pada data agar dapat memahami bagaimana struktur data tersebut
- Melakukan pemrosesan pada data agar data dapat diterima baik oleh model
    * Mengatasi missing value
    * Encoding data
    * Randomize Dataset
    * Data Standardization
    * Data Splitting
- Membangun model agar dapat memberikan rekomendasi yang baik pada user
- Melakukan evaluasi pada model untuk mengetahui performa model
- Melakukan pengujian Agar dapat mengetahui apakah model ini bisa membuat rekomendasi dengan baik

## Data Understanding
Dataset yang digunakan pada proyek ini merupakan **Book Recommendation Dataset** yang didapat kan dari situs penyedia data [Kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)

### Deskripsi Variabel
Setelah dilakukan dilakukan **Explorasi Data Analysis** diketahui bahwa terdapat tiga berkas .csv yaitu :
1. Books.csv
2. Ratings.cvs
3. Users.csv

#### 1. Dataset Books.csv
Pada berkas `Books.csv` terdiri dari 271.360 baris dan memiliki 8 kolom, diantaranya adalah :  

- `ISBN` : berisi kode ISBN dari buku  
- `Book-Title` : berisi judul buku
- `Book-Author` : berisi penulis buku
- `Year-Of-Publication` : tahun terbit buku  
- `Publisher` : penerbit buku  
- `Image-URL-S` : URL menuju gambar buku berukuran kecil
- `Image-URL-M` : URL menuju gambar buku berukuran sedang
- `Image-URL-L` : URL menuju gambar buku berukuran besar

diketahui bahwa kolom `Book-Author` terdapat 1 missing value, `Publisher` terdapat 2 missing value, dan `Image-URL-L` terdapat 3 missing value

#### 2. Dataset Users.csv

Pada berkas `Users.csv` memuat data pengguna. Data ini terdiri dari 278.858 baris dan memiliki 3 kolom, yaitu : 

- `User-ID` : berisi ID unik pengguna
- `Location` : berisi data lokasi pengguna
- `Age` : berisi data usia pengguna

diketahui bahwa kolom `Age` terdapat missing value yang cukup banyak yaitu 110.762 missing value

#### 3. Dataset Ratings
Pada berkas `Ratings.csv` memuat data rating buku yang diberikan oleh pengguna. Data ini memiliki 1.149.780 baris dan memiliki 3 kolom, yaitu :  

 - `User-ID` : berisi ID unik pengguna
 - `ISBN` : berisi kode ISBN buku yang diberi rating oleh pengguna
 - `Book-Rating` : berisi nilai rating yang diberikan oleh pengguna berkisar antara 0-10

Diketahui bahwa tidak terdapat missing value pada data `Ratings.csv`

Karna pada proyek kali ini mengunakan metode **Collaborative Filtering**, kita akan berfokus pada dataset `ratings` oleh karna itu kita perlu melakukan explorasi lebih lanjut untuk benar-benar memahami informasi serta kualitas data.

kita perlu melihat berapa jumlah buku berdasarkan rating yang diberikan penguna. setelah dilakukan pengelompokan berdasarkan `Book-Rating` didapatkan hasil seperti pada *Tabel 1*

*Tabel 1. Jumlah buku berdasarkan rating yang diberikan penguna*

| Book-Rating | User-ID |   ISBN |
|------------:|--------:|-------:|
|      0      |  716109 | 716109 |
|      1      |    1770 |   1770 |
|      2      |    2759 |   2759 |
|      3      |    5996 |   5996 |
|      4      |    8904 |   8904 |
|      5      |   50974 |  50974 |
|      6      |   36924 |  36924 |
|      7      |   76457 |  76457 |
|      8      |  103736 | 103736 |
|      9      |   67541 |  67541 |
|      10     |   78610 |  78610 |

Dari Tabel 1 diatas diketahui bahwa banyak penguna yang memberikan rating 0. untuk dapat memahami data lebih jelas, mari kita lihat visualisasi data mengunakan bar chart seperti pada *Gambar 1*

*Gambar 1. Bar-chart jumlah buku berdasarkan rating yang diberikan penguna*

![bar-chart-ratings](https://user-images.githubusercontent.com/79014522/205957792-19ae8e6f-984f-4b77-a017-408db2c94bdf.png)

Dapat dilihat pada Gambar 1 bahwa terjadi ke tidak seimbangan pada data, jika hal ini tidak diatasi maka akan berpengaruh terhadap performa model nantinya.

## Data Preparation
Teknik yang digunakan dalam penyiapan data *(Data Preparation)* yaitu:
- **Mengatasi data yang tidak seimbang** : Seperti yang telah diketahui sebelumnya bahwa jumlah rating tidak seimbang (imbalance) yang mana sebagian besar user memberikan rating 0 pada buku. Hal ini dapat mengakibatkan model memiliki kinerja yang buruk. Untuk mengatasi hal tersebut, pada proyek ini data dengan rating 0 akan dihapus *(di-drop)*. Walaupun jumlah data saat ini berkurang drastis namun distribusi data menjadi lebih seimbang seperti yang terlihat pada *Gambar 2* dan diharapkan memiliki kinerja yang lebih baik.

    *Gambar 2. Bar-chart distribusi data yang telah seimbang*

    ![bar-chart-ratings-bersih](https://user-images.githubusercontent.com/79014522/205957885-dfbb551d-d73f-4a67-82af-1860f163c0d9.png)


- **Encoding** : dilakukan untuk menyandikan `User-ID` dan `ISBN` ke dalam indeks integer. Tahapan ini diperlukan karena kedua data tersebut berisi integer yang tidak berurutan (acak) dan gabungan string. Untuk itu perlu diubah ke dalam bentuk indeks.

- **Randomize Dataset** : pengacakan data agar distribusi datanya menjadi random. Pengacakan data bertujuan untuk mengurangi varians dan memastikan bahwa model tetap umum dan *overfit less*. Pengacakan data juga memastikan bahwa data yang digunakan saat validasi merepresentasikan seluruh distribusi data yang ada.

- **Data Standardization** : Pada data rating yang digunakan pada proyek ini berada pada rentang 0 hingga 10. Penerapan standarisasi menjadi rentang 0 hingga 1 dapat mempermudah saat proses training. Hal ini dikarenakan variabel yang diukur pada skala yang berbeda tidak memberikan kontribusi yang sama pada model fitting & fungsi model yang dipelajari dan mungkin berakhir dengan menciptakan bias jika data tidak distandarisasi terlebih dulu.

- **Data Splitting and Splitting** : dataset dibagi menjadi 2 bagian, yaitu data yang akan digunakan untuk melatih model (sebesar 90%) dan data untuk memvalidasi model (sebesar 10%). Tujuan dari pembagian data uji dan validasi tidak lain adalah untuk proses melatih model serta mengukur kinerja model yang telah didapatkan.

## Modeling and Result
Solusi yang akan diterapkan pada proyek ini adalah menggunakan metode Collaborative Filtering.

Metode ini akan menghasilkan rekomendasi sejumlah buku yang sesuai dengan preferensi pengguna berdasarkan rating yang telah diberikan sebelumnya. Dari data rating pengguna dapat digunakan untuk mengidentifikasi buku-buku yang mirip dan belum pernah diberi rating oleh pengguna untuk direkomendasikan.

#### Kelebihan
- Tidak diperlukan pengetahuan domain karena embeddings mempelajarinya secara otomatis.
- Dapat membantu pengguna menemukan minat baru
- Sistem hanya membutuhkan matriks umpan balik (feedback, misalnya berup rating) untuk melatih model faktorisasi matriks. Secara khusus, sistem tidak memerlukan fitur kontekstual.

#### Kekurangan
- Model tidak dapat memberikan rekomendasi kepada pengguna baru karena sistem ini bergantung pada preferensi atau umpan balik yang ada (cold-start problem).
- Sulit untuk mengikutsertakan fitur lain (side-features) pada kueri atau item

Pada tahap ini, model menghitung skor kecocokan antara pengguna dan buku dengan teknik embedding. 

Beberapa properti yang digunakan dalam kelas RecommenderNet dan menjadi parameter pada layer embedding untuk menghasilkan model diantaranya:
- `num_users` : jumlah data pengguna
- `num_isbn` : jumlah data buku, dihitung berdasarkan ISBN
- `embedding_size` : ukuran atau dimensi yang digunakan dalam embedding pada data user dan buku

Pertama, kita melakukan proses embedding terhadap data user dan buku. Jumlah user dan buku yang didefinisikan pada `num_users` dan `num_isbn` bertujuan sebagai input untuk membuat vektor embedding keduanya. Sedangkan `embedding_size` menentukan ukuran atau dimensi embedding yang dibuat. Semakin besar nilai dari `embedding_size` akan membuat model semakin akurat, namun jika berlebihan akan mengakibatkan model menjadi overfit. Untuk itu pada proyek ini juga menggunakan `optuna` untuk mencari nilai yang optimal. Selanjutnya, dilakukan operasi perkalian *dot product* antara embedding user dan buku. Selain itu, kita juga dapat menambahkan bias untuk setiap user dan buku. Skor kecocokan ditetapkan dalam skala [0,1] dengan fungsi aktivasi sigmoid.

Model ini juga di-compile dengan fungsi loss binarycrossentropy, menggunakan Adam sebagai optimizer dengan learning rate sebesar 0.001 dan root mean squared error (RMSE) sebagai metrics evaluation.

Agar dapat mengetahui apakah model ini bisa membuat rekomendasi dengan baik, maka dilakukan pungujian menggunakan data sampel user secara acak pada dataseat `Ratings.csv` dan diperoleh hasil seperti pada *Tabel 2 dan Tabel 3*

*Tabel 2. Books with high ratings from user*

| No | Author         | Title                                                                                                               |
|----|----------------|---------------------------------------------------------------------------------------------------------------------|
| 1  | Jerry Beck     | Looney Tunes and Merrie Melodies: A Complete Illustrated Guide to the Warner Bros. Cartoons                         |
| 2  | Debra Baycura  | Patchwork Math 2 (Grades 4-6)                                                                                       |
| 3  | L. Frank Baum  | Oz-story 6                                                                                                          |
| 4  | A. A. Milne    | Winnie-The-Pooh and Some Bees (Dutton Easy Reader)                                                                  |
| 5  | Esther Averill | Jenny and the Cat Club: A Collection of Favorite Stories About Jenny Linsky (New York Review Children's Collection) |

*Tabel 3. Top 10 book recommendation*

| No | Author           | Title                                                     |
|----|------------------|-----------------------------------------------------------|
| 1  | J.R.R. TOLKIEN   | The Return of the King (The Lord of the Rings, Part 3)    |
| 2  | Dr. Seuss        | Fox in Socks (I Can Read It All by Myself Beginner Books) |
| 3  | J. R. R. Tolkien | The Return of the King (The Lord of The Rings, Part 3)    |
| 4  | J. R. R. Tolkien | The Two Towers (The Lord of the Rings, Part 2)            |
| 5  | Shel Silverstein | The Giving Tree                                           |
| 6  | Bill Watterson   | Calvin and Hobbes                                         |
| 7  | Jodi Picoult     | My Sister's Keeper : A Novel (Picoult, Jodi)              |
| 8  | Dr. Seuss        | The Lorax                                                 |
| 9  | Scott Adams      | Dilbert: A Book of Postcards                              |
| 10 | J. K. Rowling    | Harry Potter and the Chamber of Secrets Postcard Book     |


hasil di atas adalah rekomendasi untuk user dengan id 155027. Dari output tersebut, kita dapat membandingkan antara buku dengan rating tertinggi dari user dan Top 10 buku recommendation untuk user. 

## Evaluation

Pada proyek ini menggunakan metrik RMSE (Root Mean Square Error) untuk mengevaluasi kinerja model yang dihasilkan. RMSE adalah cara standar untuk mengukur kesalahan model dalam memprediksi data kuantitatif.
Root Mean Squared Error (RMSE) mengevaluasi model regresi linear dengan mengukur tingkat akurasi hasil perkiraan suatu model. RMSE dihitung dengan mengkuadratkan error (prediksi – observasi) dibagi dengan jumlah data (= rata-rata), lalu diakarkan. Perhitungan RMSE ditunjukkan pada rumus berikut ini.

$$RMSE = \sqrt{{\sum_{i=1}^n}{{(ŷ_i - y_i)^2} \over n}}$$

`RMSE` = nilai root mean square error

`y`  = nilai hasil observasi

`ŷ`  = nilai hasil prediksi

`i`  = urutan data

`n`  = jumlah data

Nilai RMSE rendah menunjukkan bahwa variasi nilai yang dihasilkan oleh suatu model prakiraan mendekati variasi nilai obeservasinya. RMSE menghitung seberapa berbedanya seperangkat nilai. Semakin kecil nilai RMSE, semakin dekat nilai yang diprediksi dan diamati.

Berikut ini adalah plot metrik RMSE setelah proses pelatihan model.

*Gambar 3. Grafik evaluasi model*

![grafik-evaluasi](https://user-images.githubusercontent.com/79014522/205958044-115f4ca3-dd28-46d7-8b12-3d409703b0f8.png)

Perhatikanlah, Dari proses ini, kita memperoleh nilai error akhir sebesar sekitar 0.14 dan error pada data validasi sebesar 0.18. Nilai tersebut cukup bagus untuk sistem rekomendasi

## Kesimpulan
1. Hasil evaluasi dari model yang telah dibuat diperoleh nilai error akhir sebesar sekitar 0.14 dan error pada data validasi sebesar 0.18. Nilai tersebut cukup bagus untuk sistem rekomendasi
2. Dataset dibagi menjadi 2 bagian, yaitu data yang akan digunakan untuk melatih model (sebesar 90%) dan data untuk memvalidasi model (sebesar 10%)


## Referensi
1. E. Uko, B. O., dan P. O., “An Improved Online Book Recommender System using Collaborative Filtering Algorithm,” Int. J. Comput. Appl., vol. 179, no. 46, hlm. 41–48, Jun 2018, doi: 10.5120/ijca2018917193.
2. A. B. Kartiko, “Perancangan Sistem Rekomendasi Buku Pada Aplikasi Pembelajaran Elektronik (E- Learning) Berbasis Website Menggunakan Collaborative Filtering,” hlm. 14.
3. A. H. Ritdrix dan P. W. Wirawan, “Sistem Rekomendasi Buku Menggunakan Metode Item-Based Collaborative Filtering,” J. Masy. Inform., vol. 9, no. 2, hlm. 24–32, Nov 2018, doi: 10.14710/jmasif.9.2.31482.

