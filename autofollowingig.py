import getpass
import os
import random
import sys
import time

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

def initial_checker():
    files = [hashtag_file, users_file, whitelist, blacklist, setting]
    try:
        for f in files:
            with open(f, 'r') as f:
                pass
    except BaseException:
        for f in files:
            with open(f, 'w') as f:
                pass
        print("""
        Selamat datang di bot auto following instagram, sepertinya ini adalah pertama kalinya anda menggunakan bot ini.
        Sebelum memulai, mari atur dasar-dasarnya, sehingga bot berfungsi seperti yang anda inginkan.
        """)
        setting_input()
        print("""
        Anda dapat menambahkan hashtag, daftar pesaing,
        whitelist, blacklist, dan juga menambahkan user di menu pengaturan.
        Bersenang-senanglah!
        """)
        time.sleep(5)
        os.system('cls')

def read_input(f, msg, n=None):
    if n is not None:
        msg += " (Enter untuk default: {})".format(n)
    print(msg)
    entered = sys.stdin.readline().strip() or str(n)
    if isinstance(n, int):
        entered = int(entered)
    f.write(str(entered) + "\n")

def setting_input():
    inputs = [("Berapa banyak follow yang ingin anda lakukan dalam sehari? ", 100),
              (("Followers akun maksimal yang ingin anda ikuti?\n"
                "Akun yang memiliki followers lebih besar dari nilai ini akan dilewati "), 2000),
              (("Followers minimum yang harus dimiliki akun sebelum anda ikuti?\n"
                "Akun yang memiliki followers lebih sedikit dari nilai ini akan dilewati "), 10),
              (("Maksimal following akun yang ingin anda ikuti?\n"
                "Akun yang memiliki followers lebih besar dari nilai ini akan dilewati "), 7500),
              (("Minimum akun yang ingin anda ikuti?\n"
                "Akun yang memiliki followers lebih sedikit dari nilai ini akan dilewati "), 10),
              ("Followers maksimal untuk rasio following ", 10),
              ("Following maksimal untuk rasio followers ", 10),
              ("Delay waktu dari follow akun satu ke akun lain ", 30)]

    with open(setting, "w") as f:
        while True:
            for msg, n in inputs:
                read_input(f, msg, n)
            break
        print("Selesai mengatur!")

def parameter_setting():
    settings = ["Maksimal follow per hari: ",
                "Maksimal followers untuk follow: ",
                "Minimal followers untuk follow: ",
                "Maksimal following untuk follow: ",
                "Minimal following untuk follow: ",
                "Maksimal followers untuk following rasio: ",
                "Maksimal following untuk followers rasio: ",
                "Follow delay: "]


    with open(setting) as f:
        data = f.readlines()

    print("Parameter saat ini\n")
    for s, d in zip(settings, data):
        print(s + d)
              

def username_adder():
    with open(SECRET_FILE, "a") as f:
        print("Masukkan akun instagram.")
        print("Jangan khawatir, rahasia akun aman.")
        while True:
            print("Username: ")
            f.write(str(sys.stdin.readline().strip()) + ":")
            print("Password: (password tidak akan ditampilkan atas alasan keamanan)")
            f.write(getpass.getpass() + "\n")
            print("Apakah ingin menambahkan akun lain? (y/n)")
            if "y" not in sys.stdin.readline():
                break


def get_adder(name, fname):
    def _adder():
        print("Database:")
        print(bot.read_list_from_file(fname))
        with open(fname, "a") as f:
            print('Menambahkan {} ke database'.format(name))
            while True:
                print("Enter {}: ".format(name))
                f.write(str(sys.stdin.readline().strip()) + "\n")
                print("Apakah anda ingin menambahkan akun lain {}? (y/n)\n".format(name))
                if "y" not in sys.stdin.readline():
                    print('Selesai menambahkan {} ke database'.format(name))
                    break
    return _adder()

def hashtag_adder():
    return get_adder('hashtag', fname=hashtag_file)


def competitor_adder():
    return get_adder('username', fname=users_file)


def blacklist_adder():
    return get_adder('username', fname=blacklist)


def whitelist_adder():
    return get_adder('username', fname=whitelist)


def userlist_maker():
    return get_adder('username', fname=userlist)

def menu():
    ans = True
    while ans:
        print("=========================================================")
        print("---[1] Follow---")
        print("---[2] Setting---")
        print("=========================================================")
        ans = input("Masukkan angka menu\n").strip()
        if ans == "1":
            menu_follow()
        elif ans == "2":
            menu_setting()
        else:
            print("\n Input tidak valid.")
            
def menu_follow():
    ans = True
    while ans:
        print("""
        1. Follow dari hashtag
        2. Follow followers
        3. Follow following
        4. Follow berdasarkan like postingan
        5. Main menu
        """)
        ans = input("Bagaimana anda ingin mengikuti?\n").strip()

        if ans == "1":
            print("""
            1.Masukkan hashtag
            2.Gunakan database hashtag
            """)
            hashtags = []
            if "1" in sys.stdin.readline():
                hashtags = input("Masukkan hashtag yang dipisah dengan spasi \nContoh: kucing anjing\nApa hashtag nya?\n").strip().split(' ')
            else:
                hashtags = bot.read_list_from_file(hashtag_file)
            for hashtag in hashtags:
                print("Mulai following: " + hashtag)
                users = bot.get_hashtag_users(hashtag)
                bot.follow_users(users)
            menu()

        elif ans == "2":
            print("""
            1.Masukkan username
            2.Gunakan database username
            """)
            if "1" in sys.stdin.readline():
                user_id = input("siapa?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.follow_followers(user_id)
            menu()

        elif ans == "3":
            print("""
            1.Masukkan username
            2.Gunakan database username
            """)
            if "1" in sys.stdin.readline():
                user_id = input("Siapa?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.follow_following(user_id)
            menu()

        elif ans == "4":
            print("""
            1.Masukkan username
            2.Gunakan database username
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            medias = bot.get_user_medias(user_id, filtration=False)
            if len(medias):
                likers = bot.get_media_likers(medias[0])
                for liker in tqdm(likers):
                    bot.follow(liker)

        elif ans == "5":
            menu()

        else:
            print("Input tidak valid.")
            menu()

def menu_setting():
    ans = True
    while ans:
        print("""
        1. Setting bot parameter
        2. Menambahkan user akun
        3. Menambahkan database pesaing
        4. Menambahkan database hashtag 
        5. Menambahkan blacklist
        6. Menambahkan whitelist
        7. Hapus semua database
        8. Main menu
        """)
        ans = input("Apa setting yang diperlukan?\n").strip()

        if ans == "1":
            parameter_setting()
            change = input("Ingin mengubahnya? y/n\n").strip()
            if change == 'y' or change == 'Y':
                setting_input()
            else:
                menu_setting()
        elif ans == "2":
            username_adder()
        elif ans == "3":
            competitor_adder()
        elif ans == "4":
            hashtag_adder()
        elif ans == "5":
            blacklist_adder()
        elif ans == "6":
            whitelist_adder()
        elif ans == "7":
            print(
                "Tindakan ini akan menghapus semua database kecuali user akun dan pengaturan parameter")
            time.sleep(5)
            open(hashtag_file, 'w')
            open(users_file, 'w')
            open(whitelist, 'w')
            open(blacklist, 'w')
            print("Selesai, anda bisa menambahkan lagi!")
        elif ans == "8":
            menu()
        else:
            print("Input tidak valid.")
            menu_setting()


# Cek kompatibilitas input
try:
    input = raw_input
except NameError:
    pass

# Lokasi file
hashtag_file = "hashtagsdb.txt"
users_file = "usersdb.txt"
whitelist = "whitelist.txt"
blacklist = "blacklist.txt"
userlist = "userlist.txt"
setting = "setting.txt"
SECRET_FILE = "secret.txt"

#Cek setting
initial_checker()

if os.stat(setting).st_size == 0:
    print("Sepertinya setting belum ditetapkan.")
    print("Setting sesuai keinginan!")
    setting_input()

f = open(setting)
lines = f.readlines()
setting_0 = int(lines[0].strip())
setting_1 = int(lines[1].strip())
setting_2 = int(lines[2].strip())
setting_3 = int(lines[3].strip())
setting_4 = int(lines[4].strip())
setting_5 = int(lines[5].strip())
setting_6 = int(lines[6].strip())
setting_7 = int(lines[7].strip())

bot = Bot(
    max_follows_per_day=setting_0,
    max_followers_to_follow=setting_1,
    min_followers_to_follow=setting_2,
    max_following_to_follow=setting_3,
    min_following_to_follow=setting_4,
    max_followers_to_following_ratio=setting_5,
    max_following_to_followers_ratio=setting_6,
    follow_delay=setting_7,
    whitelist_file=whitelist,
    blacklist_file=blacklist)

bot.login()

while True:
    try:
        menu()
    except Exception as e:
        bot.logger.info("Error, baca keterangan dibawah.")
        bot.logger.info(str(e))
    time.sleep(1)
