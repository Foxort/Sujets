import re
import sys
import os

good = ""
txt_trace = ""
test_names = []
stud = ""
exos = ["my_name", "digits", "revalpha", "alandroit", "alanver", "countoc",
        "repeat_alpha", "hidentf", "rot_42", "last_word", "r_capitalize", "pgcd", "fprime"]


def print_green(text):
    print("\033[92m" + text + "\033[0m")


def print_red(text):
    print("\033[91m" + text + "\033[0m")


def print_blue(text):
    print("\033[94m" + text + "\033[0m")


def print_orange(text):
    print("\033[93m" + text + "\033[0m")


def hard_check_name(elem):
    if len(elem) > 1:
        return 1
    return 0


def check_cheat(name):
    try:
        text_file = open(name + "/" + name + ".c", "r")
        stdc = text_file.read()
        text_file.close()

        if " printf(" in stdc or " puts(" in stdc or " sprintf(" in stdc or " dprintf(" in stdc or " atoi(" in stdc:
            return 1
        return 0
    except:
        return 0


def get_trace_f():
    ret = os.system("timeout 2s ./a.out > trace")

    try:
        text_file = open("trace", "r")
        trace = text_file.read()
        trace = [e for e in trace.split('$') if len(e) > 0]
        text_file.close()
    except:
        print_red("Drole d'erreur appelle un cobra")
        exit(84)
    os.system("rm trace a.out")
    return trace


def parse_output(data):
    tek = 0

    i = 0
    for elem in data:
        elem = [e for e in elem.split('%') if len(e) > 0]
        test_names.append(elem[0])
        data[i] = data[i][len(elem[0]) + 1:]
        i += 1
    return data


def get_trace(name):
    try:
        correc = "correcs/" + name + "/" + name + ".c"
        main = "mains/" + name + ".c"
        studt = name + "/" + name + ".c"
        os.system("gcc " + main + " " + correc + " > /dev/null")
        good = get_trace_f()
        good = parse_output(good)
        os.system("gcc " + main + " " + studt + " > /dev/null")
        stud = get_trace_f()
        stud = parse_output(stud)
    except:
        compile = 1
    return good, stud


def check_tests(good, stud, test_names, elem):
    i = 0
    if elem == "my_name":
        if len(stud[i]) <= 1:
            print("\033[91m" + test_names[i] + " =/> FAILED\n" + "\033[0m", end="")
            print_orange("Expected a name with a length > 1")
        else:
            print_green(test_names[i] + " => PASSED")
        test_names = []
        return
    while i < len(good):
        if good[i] != stud[i]:
            print("\033[91m" + test_names[i] + " =/> FAILED\n" + "\033[0m", end="")
            print_orange("     GOT: " + stud[i] + "EXPECTED: " + good[i])
        else:
            print_green(test_names[i] + " => PASSED")
        i += 1
    test_names = []


def mouli():
    for elem in exos:
        test_names.clear()
        good = ""
        stud = ""
        print_blue("=============== Test on " + elem + "===============")
        if not os.path.isdir(elem) or not os.path.isfile(elem + "/" + elem + ".c"):
            print_red("Missing directory or file for " + elem + " !\n")
            continue
        if check_cheat(elem):
            print_red("CHEAT detected banned function :(\n")
            continue
        good, stud = get_trace(elem)
        check_tests(good, stud, test_names, elem)
        print()


mouli()
