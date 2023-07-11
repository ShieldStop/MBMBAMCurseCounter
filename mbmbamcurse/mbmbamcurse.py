import re
import pypdf
import codecs

#WARNING: THIS CODE IS INCREDIBLY UNOPTIMIZED DUE TO IT BEING WRITTEN BY A SELF TAUGHT 19 YEAR OLD IN 3 HOURS. EXPECT IT TO RUN FOR A WHILE.


#build new file if you want to go through every script PDF in folder and add to complete text file
buildnewfile = False

#point to the folder with script PDFs in it, make sure every script has been renamed with syntax "script (#)" with # being sequential
folderdir = "C:\\Users\\David\\Downloads\\mbmbamscripts"

#number of pdf files in directory
numberoffiles = 351

#choose which speaker to search for, only do one at a time because the program will die before finishing multiple
speachertosearch = "Justin"

file=open('text.txt', 'a')
if buildnewfile:
        for i in range(numberoffiles-1):
                  #starts by turning a PDF into strings
                  dir = folderdir + "\\script (" + str(i+1) + ").pdf"
                  pdf=open(dir, 'rb')
                  reader=pypdf.PdfReader(pdf, strict=False)
                  x= len(reader.pages)
                  print("done with file #" + str(i+1))

                  #then dumps those strings into a text file
                  for i in range(x):
                    if reader.pages[i]: #checks to make sure the page exists bc for some reason it will copy empty pages and python does not like that
                          page=reader.pages[i]
                          text=page.extract_text() #the last thing we use PyPDF for
                          #for some reason encoding and then decoding didn't work, so just add any unknown characters to this replace list
                          text= text.replace("\u201f", "'")
                          text= text.replace("\u2015", "-")
                          text= text.replace("\u2016", "|")
                          text= text.replace("\u2017", "_")
                          text= text.replace("\uf0e0", "?")
                          text= text.replace("\u014d", "o")
                          text= text.replace("\U0001d745", "pi")
                          text= text.replace("\u0100", "?")
                          text= text.replace("\u215b", "?")
                          text= text.replace("\u0101", "?")
                          file.writelines(text)
file.close #close it just because we want regex to open it in a different encoding (yes this is a dumb way to do it)

#regex code copied DIRECTLY from https://stackoverflow.com/questions/34040242/reading-only-the-words-of-a-specific-speaker-and-adding-those-words-to-a-list
#i THINK i understand what it does, but i won't risk looking like an idiot trying to comment it out and explain it.
speaker_words = {}
speaker_pattern = re.compile(r'^(\w+?):(.*)$')

with codecs.open("text.txt", 'r', encoding='utf-8',
                 errors='ignore') as f:
        lines = f.readlines()
        print("currently separating speakers...")
        current_speaker = None
        for line in lines:
                line = line.strip()
                match = speaker_pattern.match(line)
                if match is not None:
                        current_speaker = match.group(1)
                        line = match.group(2).strip()
                        if current_speaker not in speaker_words.keys():
                                speaker_words[current_speaker] = []
                if current_speaker:
                        words = [word.strip() for word in line.split(' ') if len(word.strip()) > 0]
                        speaker_words[current_speaker].extend(words)


file2 = open("mbmbamcurse\list.txt") #TODO make sure this works


script = file2.readlines() #this is probably the biggest timesaver

for i in range(len(script)):
       script[i] = (script[i][0:(len(script[i])-1)])
print(script)

def findswears(speaker): #so this just goes through every word in the speaker list and compares all of them to every swear. i know this is incredibly inefficient and i could use a dict as i go but that would take an hour of work for an idiot like me so i'm leaving it
    numcurses = 0
    cursesby = {}
    for i in range(len(speaker_words[speaker])):
        for j in range(len(script)):
                currentcount = 0
                if speaker_words[speaker][i] == (script[j]):
                        currentcount += 1
                numcurses += currentcount
                if currentcount > 0:
                        if not script[j] in cursesby.keys():
                                cursesby[script[j]] = 1
                        else:
                                cursesby[script[j]] += currentcount
        print("done with #" + str(i) + " of "+ str(len(speaker_words[speaker])))
    return ["Curses:" + str(numcurses), cursesby]


found = (findswears(speachertosearch))
print(found)
