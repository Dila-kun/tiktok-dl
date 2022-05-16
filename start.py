import tiktokdownloader as tkd

def main():
    archive_path = "./"
    usernames = getAllUsers("./data")
    for user in usernames:
        if tkd.downloadUser(archive_path, user) == -1:
            print("Error no downloader handler")


def getAllUsers(path_to_file):
    list_name = list(())
    f = open(path_to_file, "r")
    list_name = f.read().splitlines()
    f.close()
    return list_name

main()