file=open("Day 01\File analyzer.txt","r")

text=file.read()

lines=text.split("\n")
lines_count=len(lines)

words=text.split()
words_count=len(words)

print("Number of lines:",lines_count)
print("Number of words:",words_count)