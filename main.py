from covid_data import  COVIDDataAnalyzer
from colorama import Fore, Style, init
import os

# Inisialisasi colorama
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_header():
    print(Fore.CYAN + "=" * 60)
    print("🦠 APLIKASI ANALISIS DATA COVID-19")
    print("📊 Menggunakan Python Package Management")
    print("=" * 60 + Style.RESET_ALL)


def show_menu():
    print(Fore.GREEN + "\n📋 MENU UTAMA")
    print("1. 📊 Analisis Data Online (Live Data)")
    print("2. 📂 Analisis Data Offline (Dari File)")
    print("3. 📦 Informasi Package Terinstal")
    print("4. 🚪 Keluar")
    print(Style.RESET_ALL)


def show_installed_packages():
    """Menampilkan package yang terinstal"""
    import subprocess
    try:
        result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
        print(Fore.BLUE + "\n📦 PACKAGE YANG TERINSTAL:" + Style.RESET_ALL)
        print(result.stdout)
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}" + Style.RESET_ALL)


def main():
    analyzer = COVIDDataAnalyzer()

    while True:
        clear_screen()
        show_header()
        show_menu()

        choice = input("Pilih menu (1-4): ")

        if choice == "1":
            print(Fore.YELLOW + "\n📡 MENGAMBIL DATA DARI INTERNET..." + Style.RESET_ALL)
            analyzer.run_analysis(use_online_data=True)
            input(Fore.CYAN + "\nTekan Enter untuk kembali ke menu..." + Style.RESET_ALL)

        elif choice == "2":
            print(Fore.YELLOW + "\n📂 MENGGUNAKAN DATA LOKAL..." + Style.RESET_ALL)
            analyzer.run_analysis(use_online_data=False)
            input(Fore.CYAN + "\nTekan Enter untuk kembali ke menu..." + Style.RESET_ALL)

        elif choice == "3":
            show_installed_packages()
            input(Fore.CYAN + "\nTekan Enter untuk kembali ke menu..." + Style.RESET_ALL)

        elif choice == "4":
            print(Fore.CYAN + "\n👋 Terima kasih telah menggunakan aplikasi!")
            print("Jangan lupa untuk menonaktifkan virtual environment:")
            print("deactivate")
            print(Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "❌ Pilihan tidak valid!" + Style.RESET_ALL)
            input(Fore.CYAN + "\nTekan Enter untuk kembali ke menu..." + Style.RESET_ALL)


if __name__ == "__main__":
    main()