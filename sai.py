#READ-ME
# Input format is taken as in cmd args: 'git-url' 'path-to-clone-git' 'output1 file path' 'output2 file path'
# example:  C:\Users\Student\Documents\sd\grad-ass\sai.py https://github.com/shiiva-surya/saisss2 C:\Users\Student\Documents\os C:\Users\Student\Documents\os\out1.txt C:\Users\Student\Documents\os\out2.txt
# NOTE: if a git repo is cloned already, please DELETE it before you run this program or else this will throw an error that the repo already exists.
# output-1 has all instances of identifiers and locations in format:
    # file path in git repo
        # identifier-name  location: start point, end point
# output-2 has invalid rules broke by identifiers
# NOTE: if some identifers are not recognised as dictionary words, then it might now show its invalidity in capitalisation anamoly, excessive words and like wise rules.
# As these rules need separation of words which can't be done if they are not in Camel case. I am using camel case notation to separate words in a given identifier name.
# Used gitpython to read files in a git repo by cloning it into local machine.

from tree_sitter import Language, Parser
import enchant
import re
import os
import sys
import git


def find_ident(node, lis_ident):
    if node.type == "identifier":
        return [node.start_point, node.end_point]
    elif len(node.children) != 0:
        count = 0
        while count != len(node.children):
            l = find_ident(node.children[count], lis_ident)
            count += 1
            if l == "0" or l == lis_ident:
                continue
            if len(l) != 0:
                lis_ident.append(l)
        return lis_ident
    return "0"


def token(a, abd,n):
    Language.build_library(
        # Store the library in the `build` directory
        'build/my-languages.so',

        # Include one or more languages
        [
            'vendor/tree-sitter-go',
            'vendor/tree-sitter-javascript',
            'vendor/tree-sitter-python',
            'vendor/tree-sitter-ruby'
        ]
    )

    PY_LANGUAGE = Language('build/my-languages.so', 'python')
    JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
    GO_LANGUAGE = Language('build/my-languages.so', 'go')
    RUBY_LANGUAGE = Language('build/my-languages.so', 'ruby')
    parser = Parser()
    if n=="p":
        parser.set_language(PY_LANGUAGE)
    elif n=="g":
        parser.set_language(GO_LANGUAGE)
    elif n=="j":
        parser.set_language(JS_LANGUAGE)
    elif n=="r":
        parser.set_language(RUBY_LANGUAGE)

    tree = parser.parse(bytes(a, "utf8"))
    root_node = tree.root_node
    i = len(root_node.children)
    count = 1
    l = []
    # print(root_node)
    while i != count:
        n = root_node.children[count]  # n- expression statement
        if len(n.children) > 0:
            m = 0
            while m != len(n.children):
                l1 = find_ident(n.children[m], [])
                m += 1
                if len(l1) == 0 or l1 == "0":
                    continue
                l.append(l1)
        count += 1
    a = a.split('\n')
    sl = []
    check = []

    # print(l)
    for i in l:
        if not re.match(r'\[\[(.)*\]\]', str(i)):
            s = a[i[0][0]][i[0][1]:i[1][1]]
            sl.append([s, i[0][0], i[0][1], i[1][1]])
            if s not in check:
                check.append(s)
            # print(s+" [" + str(i[0][0]) + "," + str(i[0][1]) + "] - [" + str(i[0][0]) + "," + str(i[1][1]) + "]"+"-----------word1")
            continue
        for j in i:
            # print(j)
            s = a[j[0][0]][j[0][1]:j[1][1]]
            sl.append([s, j[0][0], j[0][1], j[1][1]])
            if s not in check:
                check.append(s)
            # print(s+" [" + str(j[0][0]) + "," + str(j[0][1]) + "] - [" + str(j[0][0]) + "," + str(j[1][1]) + "]"+"-----------word")
    out1 = open(sys.argv[3], "a")
    out1.write(abd + "\n\n\n")
    for i in sl:
        out1.write(i[0] + "  Location: [" + str(i[1]) + "," + str(i[2]) + "] - [" + str(i[1]) + "," + str(i[3]) + "]\n")
    out1.write("\n\n\n")
    out1.close()

    """first part of output is done----need to include filepath"""

    l1 = []
    for word in check:
        wordErr = []

        lis = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', word)
        # Dicitionary words
        d = enchant.Dict("en_US")
        if len(lis) > 0:
            # Excessive words
            if len(lis) > 4:
                wordErr.append("Excessive Words")
            for k in lis:
                if not d.check(k):
                    wordErr.append("Dictionary words")
        elif not d.check(word):
            wordErr.append("Dictionary words")

        # consecutive underscores
        if "__" in word:
            wordErr.append("Consecutive Underscores")

        # external underscores
        if word.startswith("_") or word.endswith("_"):
            wordErr.append("External Underscores")

        # capitalization anamoly
        if not re.match(r'[A-Za-z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', word):
            wordErr.append("Capitalization Anamoly")

        # short Identifier
        k = ["c", "d", "e", "g", "i", "in", "inOut", "j", "k", "m", "n", "o", "out", "t", "x", "y", "z"]
        if not word in k and len(word) < 4:
            wordErr.append("Short Identifier")

        # Long Identifier Name
        if (len(word) > 15):
            wordErr.append("Long Identifier")

        # Identifier encoding
        ty = ["int", "str", "float", "complex", "list", "tuple", "range", "dict", "set", "frozenset", "bool", "bytes",
              "bytearray", "memoryview"]
        for k in ty:
            s1 = k + " "
            s2 = " " + k
            s3 = "_" + k
            s4 = k + "_"
            if s1 in word or s2 in word or s3 in word or s4 in word:
                wordErr.append("Identifier Encoding")
                break
        # Enumeration Identification Decalaration Order
        for k in a:
            if "enum" in k and word in k and "{" in k and "}" in k:
                k2 = k.split("{")
                k3 = k2[1]
                k3 = k3[:-1]
                k3 = k3.split(",")
                k1 = k3
                k3.sort()
                if k3 != k1:
                    wordErr.append("Enumeration Identification Decalaration Order")
                    break
        # Naming Convention Anamoly
        if not re.match(r'[A - Za-z][a - z]*([A-Za-z][a-z]*)*', word) and not re.match(
                r'[A - Za-z][a - z]*(_)[A-Z]*[a-z]*', word):
            wordErr.append("Naming convention Anamoly")
        # need to check this
        # Numeric Identifier name
        num = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
               "thirteen", "fourteen", "fifiteen", "sixteen", "seventeen", "eighteen", "ninteen", "twenty", "thirty",
               "forty", "fifty", "sixty", "seventy", "eighty", "nintey", "hundred", "thousand", "lakh"]
        w = []
        if "_" in word:
            w = word.split("_")
        elif len(lis) > 0:
            w = lis
        if len(w) > 0:
            if w in num:
                wordErr.append("Numeric Identifier name")

        if len(wordErr) > 0:
            l1.append([word, wordErr])

    out2 = open(sys.argv[4], "a")
    out2.write(abd + "\n\n\n")
    for i in l1:
        out2.write(str(i[0]) + "==" + str(i[1]) + "\n")
    out2.write("\n\n\n")
    out2.close()


url = sys.argv[1]
path = sys.argv[2]
git.Git(path).clone(url)

dir_list = os.listdir(path)
# print("Files and directories in '", path, "' :")
# print(dir_list)
filelist = []
for root, dirs, files in os.walk(path):
    for file in files:
        filelist.append(os.path.join(root, file))
for name in filelist:
    if name[-3:] == ".py":
        fi = open(name, 'r')
        f2 = fi.read()
        # print(name)
        # print(f2)
        token(f2, name,"p")
        fi.close()
        os.remove(name)
    elif name[-3:] == ".js":
        fi = open(name, 'r')
        f2 = fi.read()
        # print(name)
        # print(f2)
        token(f2, name,"j")
        fi.close()
        os.remove(name)
    elif name[-3:] == ".go":
        fi = open(name, 'r')
        f2 = fi.read()
        # print(name)
        # print(f2)
        token(f2, name,"g")
        fi.close()
        os.remove(name)
    elif name[-3:] == ".rb":
        fi = open(name, 'r')
        f2 = fi.read()
        # print(name)
        # print(f2)
        token(f2, name,"r")
        fi.close()
        os.remove(name)
