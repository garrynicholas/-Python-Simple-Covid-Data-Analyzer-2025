import requests
import pandas as pd
import json
import os
from datetime import datetime
from colorama import  Fore, Style, init

# Inisialisasi colorama
init()


class COVIDDataAnalyzer:
    def __init__(self):
        self.base_url = "https://disease.sh/v3/covid-19"
        self.data_file = "covid_data.json"
        self.df_global = None
        self.df_countries = None

    def fetch_global_data(self):
        """Mengambil data global COVID-19"""
        try:
            print(Fore.YELLOW + "📡 Mengambil data global..." + Style.RESET_ALL)
            response = requests.get(f"{self.base_url}/all")
            if response.status_code == 200:
                data = response.json()
                print(Fore.GREEN + "✅ Data global berhasil diambil!" + Style.RESET_ALL)
                return data
            else:
                print(Fore.RED + f"❌ Error: Status code {response.status_code}" + Style.RESET_ALL)
                return None
        except Exception as e:
            print(Fore.RED + f"❌ Error mengambil  {e}" + Style.RESET_ALL)
            return None

    def fetch_countries_data(self):
        """Mengambil data COVID-19 per negara"""
        try:
            print(Fore.YELLOW + "📡 Mengambil data per negara..." + Style.RESET_ALL)
            response = requests.get(f"{self.base_url}/countries?sort=cases")
            if response.status_code == 200:
                data = response.json()
                print(Fore.GREEN + "✅ Data per negara berhasil diambil!" + Style.RESET_ALL)
                return data
            else:
                print(Fore.RED + f"❌ Error: Status code {response.status_code}" + Style.RESET_ALL)
                return None
        except Exception as e:
            print(Fore.RED + f"❌ Error mengambil  {e}" + Style.RESET_ALL)
            return None

    def save_data_to_file(self, global_data, countries_data):
        """Menyimpan data ke file JSON"""
        try:
            data_to_save = {
                "timestamp": datetime.now().isoformat(),
                "global": global_data,
                "countries": countries_data
            }

            with open(self.data_file, 'w') as file:
                json.dump(data_to_save, file, indent=4)
            print(Fore.GREEN + f"✅ Data berhasil disimpan ke {self.data_file}" + Style.RESET_ALL)
            return True
        except Exception as e:
            print(Fore.RED + f"❌ Error menyimpan data: {e}" + Style.RESET_ALL)
            return False

    def load_data_from_file(self):
        """Memuat data dari file JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                print(Fore.GREEN + f"✅ Data berhasil dimuat dari {self.data_file}" + Style.RESET_ALL)
                return data
            else:
                print(Fore.YELLOW + f"⚠️  File {self.data_file} tidak ditemukan" + Style.RESET_ALL)
                return None
        except Exception as e:
            print(Fore.RED + f"❌ Error memuat data: {e}" + Style.RESET_ALL)
            return None

    def create_dataframes(self, global_data, countries_data):
        """Membuat DataFrame pandas dari data"""
        try:
            # DataFrame global
            self.df_global = pd.DataFrame([global_data])

            # DataFrame countries
            countries_list = []
            for country in countries_data[:20]: # Top 20 negara
                countries_list.append({
                    'Country': country['country'],
                    'Cases': country['cases'],
                    'Deaths': country['deaths'],
                    'Recovered': country['recovered'],
                    'Active': country['active'],
                    'CasesPerMillion': country['casesPerOneMillion']
                })

            self.df_countries = pd.DataFrame(countries_list)
            print(Fore.GREEN + "✅ DataFrame berhasil dibuat!" + Style.RESET_ALL)
            return True
        except Exception as e:
            print(Fore.RED + f"❌ Error membuat DataFrame: {e}" + Style.RESET_ALL)
            return False

    def display_global_summary(self, global_data):
        """Menampilkan ringkasan data global"""
        print(Fore.CYAN + "\n🌍 RINGKASAN DATA GLOBAL COVID-19" + Style.RESET_ALL)
        print("=" * 50)
        print(f"📊 Total Kasus     : {global_data['cases']:,}")
        print(f"💀 Total Kematian  : {global_data['deaths']:,}")
        print(f"💚 Total Sembuh    : {global_data['recovered']:,}")
        print(f"🏥 Kasus Aktif     : {global_data['active']:,}")
        print(f"📈 Kasus Hari Ini  : {global_data['todayCases']:,}")
        print(f"📉 Kematian Hari Ini: {global_data['todayDeaths']:,}")
        print(f"📅 Terakhir Update : {datetime.fromtimestamp(global_data['updated']/1000).strftime('%Y-%m-%d %H:%M:%S')}")

    def display_top_countries(self, df_countries):
        """Menampilkan top negara dengan kasus tertinggi"""
        print(Fore.BLUE + "\n🏆 TOP 10 NEGARA DENGAN KASUS TERTINGGI" + Style.RESET_ALL)
        print("=" * 80)

        # Format data untuk tampilan yang lebih rapi
        top_countries = df_countries.head(10).copy()
        top_countries['Cases'] = top_countries['Cases'].apply(lambda  x: f"{x:,}")
        top_countries['Deaths'] = top_countries['Deaths'].apply(lambda x: f"{x:,}")
        top_countries['Recovered'] = top_countries['Recovered'].apply(lambda x: f"{x:,}")

        from tabulate import tabulate
        print(tabulate(top_countries, headers='keys', tablefmt='grid', showindex=False))

    def analyze_data(self, df_countries):
        """Melakukan analisis sederhana"""
        print(Fore.MAGENTA + "\n🔍 ANALISIS DATA" + Style.RESET_ALL)
        print("=" * 50)

        total_countries = len(df_countries)
        avg_cases = df_countries['Cases'].mean()
        max_cases_country = df_countries.loc[df_countries['Cases'].idxmax(), 'Country']
        max_cases = df_countries['Cases'].max()

        print(f"🌍 Jumlah Negara yang Dianalisis: {total_countries}")
        print(f"📈 Rata-rata Kasus per Negara: {avg_cases:,.0f}")
        print(f"🏆 Negara dengan Kasus Tertinggi: {max_cases_country} ({max_cases:,} kasus)")

        # Analisis tingkat kematian
        df_countries['DeathRate'] = (df_countries['Deaths'] / df_countries['Cases'] * 100).round(2)
        avg_death_rate = df_countries['DeathRate'].mean()
        print(f"💀 Rata-rata Tingkat Kematian: {avg_death_rate:.2f}%")

    def create_simple_chart(self, df_countries):
        """Membuat chart sederhana menggunakan matplotlib"""
        try:
            import matplotlib.pyplot as plt

            # Ambil top 10 negara
            top_10 = df_countries.head(10)

            # buat bar chart
            plt.figure(figsize=(12, 6))
            plt.bar(top_10['Country'], top_10['Cases'], color='skyblue')
            plt.title('Top 10 Negara dengan Kasus COVID-19 Tertinggi')
            plt.xlabel('Negara')
            plt.ylabel('Jumlah Kasus')
            # Putar nama negara 45 derajat agar tidak tabrakan.
            plt.xticks(rotation=45, ha='right')
            # Otomatis atur jarak agar tidak terpotong.
            plt.tight_layout()

            # Simpan chart
            chart_file = 'covid_chart.png'
            plt.savefig(chart_file)
            print(Fore.GREEN + f"✅ Chart disimpan sebagai {chart_file}" + Style.RESET_ALL)

            # Tampilkan chart (opsional)
            # plt.show()

        except ImportError:
            print(Fore.YELLOW + "⚠️  Matplotlib tidak tersedia untuk membuat chart" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"❌ Error membuat chart: {e}" + Style.RESET_ALL)

    def run_analysis(self, use_online_data=True):
        """Menjalankan analisis lengkap"""
        print(Fore.CYAN + "🚀 MEMULAI ANALISIS DATA COVID-19" + Style.RESET_ALL)

        # Di covid_data.py, fungsi run_analysis() dimulai:
        # Ini adalah penampung kosong untuk dua data penting
        global_data = None
        countries_data = None

        if use_online_data:
            # Ambil data dari API
            global_data = self.fetch_global_data()
            countries_data = self.fetch_countries_data()

            if global_data and countries_data:
                # Simpan data
                self.save_data_to_file(global_data, countries_data)
            else:
                print(Fore.RED + "❌ Gagal mengambil data online, mencoba data lokal..." + Style.RESET_ALL)
                use_online_data = False

        if not use_online_data:
            # Gunakan data lokal
            local_data = self.load_data_from_file()
            if local_data:
                global_data = local_data['global']
                countries_data = local_data['countries']
            else:
                print(Fore.RED + "❌ Tidak ada data tersedia!" + Style.RESET_ALL)
                return

        if global_data and countries_data:
            # Buat DataFrame
            if self.create_dataframes(global_data, countries_data):
                # Tampilkan hasil
                self.display_global_summary(global_data)
                self.display_top_countries(self.df_countries)
                self.analyze_data(self.df_countries)
                self.create_simple_chart(self.df_countries)
                print(Fore.GREEN + "\n✅ ANALISIS SELESAI!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "❌ Gagal membuat DataFrame" + Style.RESET_ALL)
        else:
            print(Fore.RED + "❌ Data tidak lengkap untuk analisis" + Style.RESET_ALL)