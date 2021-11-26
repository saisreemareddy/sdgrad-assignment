# sdgrad-assignment
Graduate assignment repo for software design class- UOH

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
