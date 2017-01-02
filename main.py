import os
import subprocess
import datetime
import argparse
from message_handler import MessageHandler

DUMMY_FILE = ".dummy_file"

# Using ISO 8601 format according to https://git-scm.com/docs/git-commit#_date_formats
# TODO - Add random time "jitter" if necessary
# TODO - Deal with branches
def forge_commit(date, count):
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    flip_file(count)
    subprocess.call(["git", "add", DUMMY_FILE])
    subprocess.call(["git", "commit", "--date", date_str, "-m", str(count)])
    count += 1

# TODO - raw byte stuff instead of str flipping
def flip_file(count):
    with open(DUMMY_FILE, "w") as f:
        f.write(str(count))

# https://stackoverflow.com/questions/13716658/how-to-delete-all-commit-history-in-github
# TODO - Only clear dummy file history, not whole history
def clear_git_repo(date):
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    subprocess.call("git checkout --orphan latest_branch".split(" "))
    subprocess.call("git add -A".split(" "))
    subprocess.call("git commit -a".split(" ") + ["--date", date_str, "-m 'reset'"])
    subprocess.call("git branch -D main".split(" "))
    subprocess.call("git branch -m main".split(" "))


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def main():
    #start_date = datetime.datetime.today() - datetime.timedelta(10)
    #end_date =  datetime.datetime.today()

    #for count, date in enumerate(daterange(start_date, end_date)):
        #forge_commit(date, count)

    h = MessageHandler("Do you think that git commit history is useful?")
    datelist = h.get_mlist()

    reset_date = datelist[0] - datetime.timedelta(seconds=10)
    clear_git_repo(reset_date)

    for count, date in enumerate(datelist):
        forge_commit(date, count)


    for x in h.get_console_out():
        print(''.join(x))

if __name__ == "__main__":
    main()

    #parser = argparse.ArgumentParser(description="Create random fill or message in git history")
    #subparsers = parser.add_subparsers()
    #parser_message = subparsers.add_parser("message")
    #parser_message.add_argument("text", nargs="*")

    #parser_random = subparsers.add_parser("random")
    #parser_random.add_argument("-s", "--start_date")
    #parser_random.add_argument("-e", "--end_date")
    #parser.parse_args()
