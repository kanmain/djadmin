#!/usr/bin/env python3

from utils import create_django_project, config_settings


def main():
        
    while True:
        print("\n=== MENU DJANGO ADMIN ===")
        print("1. Start Django project")
        # print("2. Memodifikasi file config/settings.py")
        # print("3. Membuat aplikasi")
        print("0. Quit")
        print("=========================")
        choice = input("Pilih menu: ")

        if choice == "1":
            # create_django_project()
            config_settings()

        # elif choice == "2":
        #     modify_settings_and_move_secret_key()

        elif choice == "0":
            # print("Terima kasih telah menggunakan DJ Admin. Sampai jumpa!\n")
            break
        else:
            print("Not valid menu, try again.")

        input("Press enter to continue...")


if __name__ == "__main__":
    main()
