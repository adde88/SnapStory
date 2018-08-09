import requests
import urllib.request
import sys
import argparse
import os

api = "https://storysharing.snapchat.com/v1/fetch/{}?request_origin=ORIGIN_WEB_PLAYER"


def valid_username(username):
    """
    Checks if the username has a
    public story. If it does, then
    it is a valid username
    """

    url = "https://story.snapchat.com/s/{}"
    url = url.format(username)
    r = requests.get(url)

    if r.status_code == 200:
        return True

    else:
        return False


def download(username):

    url = api.format(username)
    response = requests.get(url)

    data = response.json()
    print("\033[92m[+] Fetched data\033[0m")

    # Making a directory with given username
    # to store the images of that user
    os.makedirs(username, exist_ok=True)

    story_arr = data.get("story").get("snaps") # Using dict.get() will return None when there are no snaps instead of throwing a KeyError

    if story_arr:
        print("\33[93m[!] Downloading from",
            str(data["story"]["metadata"]["title"]),
            str(data["story"]["metadata"]["emoji"]),
            "(\033[91m{}\33[93m)\33[0m".format(username))
        for index, media in enumerate(story_arr):
            try:
                file_url = media["media"]["mediaUrl"]

                if media["media"]["type"] == "IMAGE":
                    file_ext = ".jpg"

                    # This is name of the dir where these types
                    # of files will be stored
                    filetype = "IMAGE"

                elif media["media"]["type"] == "VIDEO":
                    file_ext = ".mp4"
                    filetype = "VIDEO"

                elif media["media"]["type"] == "VIDEO_NO_SOUND":
                    file_ext = ".mp4"
                    filetype = "VIDEO_NO_SOUND"


                dir_name = username+"/"+filetype+"/"

                os.makedirs(dir_name, exist_ok=True)

                path = dir_name+str(media["id"])+file_ext

                if not os.path.exists(path):
                    urllib.request.urlretrieve(file_url, path)
                    print("\033[92m[+] Downloaded file {:d} of {:d}:\033[0m {:s}".format(index+1, len(story_arr), path.replace(dir_name, "")))
                else:
                    print("\033[91m[!] File {:d} of {:d} already exists:\033[0m {:s}".format(index+1, len(story_arr), path.replace(dir_name, "")))
            except KeyError as e:
                print("\033[91m[-] Could not get file data: \033[0m{:s}".format(str(e)))
            except KeyboardInterrupt:
                print("\033[91m[!] Download cancelled")
                break

    else:
        print("\033[91m[!] No stories available")


def main():
    parser = argparse.ArgumentParser(description = "A public SnapChat story downloader")
    parser.add_argument('username', action="store",
    help="Username of the user with a public story")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    else:
        if valid_username(args.username):
            print("\033[92m[+] Valid username\033[0m")
            download(args.username)

        else:
            print("\033[91m[-] Invalid username\033[0m")

if __name__=="__main__":
    main()
