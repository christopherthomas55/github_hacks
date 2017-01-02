import datetime
from char_map import char_map


"""
 The github structure appears to be pretty simple. The first col is, then it
 repeats 51 more times. The first of the year is


Sun   ... ...
Mon   ... ...
Tues  ... ...
Wed   ... ...
Thurs ... ...
Fri   ... ...
Sat   ... ...


I say characters are 5 wide, 5 tall. I will skip weekends

That means each year can hold approximately 10 characters
"""

# Auto starts on previous year
class MessageHandler():
    # On my github, this is the "dark" color. May need to edit
    commits_per_day = 10

    def __init__(self, message):
        self.message = message

        # Start on previous year for now
        year = datetime.date.today().year - 1
        mlist = self.message.split(" ")

        # Storing as tuple (year, message_chunk)
        self.year_chunks = []

        chunk = ""

        # No fancy logic in chunking so far
        for word in mlist:
            if chunk:
                chunk = chunk + " " + word
            else:
                chunk = chunk + word

            if len(chunk) >= 10:
                self.year_chunks.append((year, chunk[:10]))
                chunk = chunk[10:]
                year -= 1

            # 7 close enough to just full send
            elif len(chunk) > 7:
                self.year_chunks.append((year, chunk))
                chunk = ""
                year -= 1

        if chunk:
            self.year_chunks.append((year, chunk))

        self.outlist = []
        self._set_outlist()

    # Read char_map description to get a sense of how to read the bitmap
    @classmethod
    def char_2_grid(cls, char):
        code = ord(char.upper())
        try:
            assert(5*(code + 1) < len(char_map))
        except:
            raise Exception("Char %s not in char map"%char)

        out = []
        for y in range(5):
            out_x = []
            for x in range(5):
                # Fun byte manipulation!
                grid_val  = char_map[code*5 + y] & (1 << x) == (1 << x)
                out_x.append(grid_val)
            out.append(out_x)
        return out

    def _set_outlist(self):
        for year, message in self.year_chunks:
            # weekday returns 0 for monday to 6 for sunday
            # Here if weekday is 7, year start is 1
            # If weekday is 0 (monday) it is 7. So we're good
            # Indicates sunday that is the first full column
            first_sunday = 7 - datetime.date(year, 1, 1).weekday()
            start_date = datetime.datetime(year, 1, first_sunday)

            for count, char in enumerate(message):
                start = 7*5*count+1
                grid = self.char_2_grid(char)
                for county, y in enumerate(grid):
                    for countx, x in enumerate(y):
                        if x:
                            for ctime in range(self.commits_per_day):
                                self.outlist.append(start_date + datetime.timedelta(days=start + county + 7*countx, seconds=ctime))

        # Sort list so that first is oldest
        # Inefficient, should be done in above
        # Remember - sorting defaults to ascending
        self.outlist = sorted(self.outlist)

    def get_mlist(self):
        return self.outlist

    def get_console_out(self):
        all_out = []
        for year, message in self.year_chunks:
            print(year)

            out = [[],[],[],[],[]]
            for char in message:
                for count, x in enumerate(MessageHandler.char_2_grid(char)):
                    out[count].extend(["O" if y else "-" for y in x])
            all_out.extend(out)
        return all_out


if __name__ == "__main__":
    e = MessageHandler("Hi. Do you like my git history? It's kinda funny!")
    for x in e.get_console_out():
        print(''.join(x))
