#!/usr/bin/env python 3.6
# Version 0.1.2018 - by TianqiW

# Search.py is the main program of this project. It can search the database and provide the information.
# Also, user can save entries to an output file.
# There are some color codes.

import sqlite3

connection = None
cursor = None
save_list = []
debug = False


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def select(command):
    global connection, cursor

    error = False
    segments = command.split()
    if len(segments) > 3:
        error = True

    if len(segments) == 2:
        if segments[0].isalpha() and segments[1].isalpha():
            segments[1] = segments[0] + ' ' + segments[1]
            segments = segments[1:]
    elif len(segments) == 3:
        if segments[0].isalpha() and segments[1].isalpha():
            segments[1] = segments[0] + ' ' + segments[1]
            segments = segments[1:]
        elif segments[1].isalpha() and segments[2].isalpha():
            segments[1] = segments[1] + ' ' + segments[2]
            segments = segments[:-1]
    if not command:
        confirm = input("\033[1;31;48m You are going to get the entire database! Are you sure? Y/N")
        if confirm == "Y" or confirm == "y":
            command = 'select * from listings'
        else:
            error = True
    else:
        if len(segments) == 1:
            if _istext(segments[0]):
                command = "select * from listings where prefix == '%s'" % segments[0].upper()
            elif segments[0].isdecimal():
                segments = int(segments[0])
                if segments < 1 or segments > 999:
                    error = True
                elif segments < 10:
                    segments *= 100
                    command = "select * from listings where num >= %d" % segments
                    command += " and num < %d" % (segments + 100)
                elif segments < 100:
                    segments *= 10
                    command = "select * from listings where num >= %d" % segments
                    command += " and num < %d" % (segments + 10)
                else:
                    command = "select * from listings where num == %d" % segments
            else:
                error = True
        elif len(segments) == 2:
            if _istext(segments[0]):
                command = "select * from listings where prefix == '%s'" % segments[0].upper()
                first = "alpha"
            elif segments[0].isdecimal():
                first = "dec"
                value = int(segments[0])
                if value < 1 or value > 999:
                    error = True
                elif value < 10:
                    value *= 100
                    command = "select * from listings where num >= %d" % value
                    command += " and num < %d" % (value + 100)
                elif value < 100:
                    value *= 10
                    command = "select * from listings where num >= %d" % value
                    command += " and num < %d" % (value + 10)
                else:
                    command = "select * from listings where num == %d" % value
            else:
                error = True
                first = "error"
            if not error:
                if _istext(segments[1]) and first == "dec":
                    command += " and prefix = '%s'" % segments[1].upper()
                elif segments[1].isdecimal() and first == "alpha":
                    value = int(segments[1])
                    if value < 1 or value > 999:
                        error = True
                    elif value < 10:
                        value *= 100
                        command += " and num >= %d" % value
                        command += " and num < %d" % (value + 100)
                    elif value < 100:
                        value *= 10
                        command += " and num >= %d" % value
                        command += " and num < %d" % (value + 10)
                    else:
                        command += "and num == %d" % value
            else:
                error = True
        else:
            error = True
    if error:
        print("\033[1;30;48m")
        print("Usage: [Prefix] [No.] ")
        print("Prefix can be left empty as 'all'. Examples: Int D, ENGL, mAth, |empty| ")
        print("Number is the number 'begin with'. Examples: 301, 3(300-399), 31(310-319) |empty|(100-999)")
        print("Some examples: ENGL, MATH 1, CMPUT 229, 101, |empty|")
        return None
    if debug:
        print(command)
    cursor.execute(command)
    result = cursor.fetchall()
    if not result:
        print("\033[1;31;48mNo results are found!")
    return result


def _istext(string):
    temp = string.split()
    if len(temp) == 1:
        return string.isalpha()
    elif len(temp) == 2:
        return temp[0].isalpha() and temp[1].isalpha()
    else:
        return False


def process(data):
    count = len(data)
    number = 10
    print("\033[1;34;48m%d results are found!" % count)
    valid = False
    while not valid:
        number = input("\033[1;32;48mHow many entries do you want in a page? \033[1;30;48m")
        try:
            number = int(number)
            valid = True
        except ValueError:
            print("\033[1;31;48mPlease enter an integer!")

    for i in range(0, count, number):
        pause = True
        while pause:
            index = 0
            for j in data[i:i + number]:
                index += 1
                print("\033[1;30;48m"+str(index), "\033[1;35;48m"+j[1]+"-"+str(j[2]), j[3])
            command = input('\033[1;32;48mEnter an \033[1;34;48mindex\033[1;32;48m to see the description,\n'
                            ' \033[1;34;48m"0"\033[1;32;48m to finish or any others to view the next page.')
            if command.isdecimal():
                if int(command) == 0:
                    return
                elif 0 < int(command) <= len(data[i:i + number]):
                    show_detail(data[i:i + number][int(command)-1])
                else:
                    pause = False
            else:
                pause = False


def show_detail(entry):
    print("\033[1;30;48mCourse:\033[1;33;48m %s - %d" % (entry[1], entry[2]))
    print("\033[1;30;48mTitle:\033[1;33;48m %s" % entry[3])
    print("\033[1;30;48mdescription: ")
    for i in range(0, len(entry[4]), 70):
        print("\t\033[1;33;48m"+entry[4][i:i + 70])
    command = input('\033[1;32;48mEnter \033[1;34;48m"+"\033[1;32;48m to save it in your cart for further export.\n'
                    ' Or others to go back.')
    if command == "+":
        save(entry)


def save(entry):
    global save_list
    temp = ""
    temp += "Course: %s - %d\n" % (entry[1], entry[2])
    temp += "Title: %s\n" % entry[3]
    temp += "description: \n"
    for i in range(0, len(entry[4]), 70):
        temp += "\t"+entry[4][i:i + 70]+"\n"
    temp += ("\n"+"="*70+"\n")
    save_list.append(temp)
    print("\033[1;34;48m Course Saved")


def main():
    connect("listings.db")
    command = input("\033[1;33;48mEnter command or 'quit' to quit.").lower()
    while command != "quit":
        result = select(command)
        if result:
            process(result)
        command = input("\033[1;33;48mEnter command or 'quit' to quit.").lower()
    if save_list:
        file = open("saved course.txt", "a+")
        for i in save_list:
            print(i)
            file.write(i.replace("★", "Credit"))  # unicode cannot be written
        file.close()
        print("Saved course has been kept to 'save course.txt'")


main()
