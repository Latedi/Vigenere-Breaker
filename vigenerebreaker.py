import itertools

#Put ciphertexts into the input variable, and the keylength into the keylegnth variable.
#This should (hopefully) produce the plaintexts if there is enough input and it's all
#in english A-Z including W. Otherwise this script can also create a list of other
#potential keys.

def printpretty(inputstr, blocksize=5, newline=65):
	index = 0
	totlen = len(inputstr)
	while(index < totlen):
		if(index + blocksize < totlen):
			print(inputstr[index:index+blocksize], end="")
			index += blocksize
		else:
			print(inputstr[index:totlen], end="")
			index = totlen
		if(index % newline == 0):
			print()
		else:
			print(" ", end="")
	
def frequency(inputstr):
	countarr = []
	if(len(inputstr) > 0):
		for i in range(0, ord('Z') - ord('A') + 1):
			currentchar = chr(ord('A') + i)
			c = inputstr.count(currentchar)
			countarr.append([currentchar, float("%.2f" % (c / len(inputstr) * 100))])
	return countarr
	
def runandprint(header, function, inputstr):
	print(header)
	arr = function(inputstr)
	arr.sort(key=getsortkey)
	arr.reverse()
	if(len(arr) > 0):
		for i in range(0, len(arr)):
			print(arr[i][0] + ": " + str(arr[i][1]))
	print()
	return arr

def getsortkey(tuple):
	return tuple[1]
	
def vigenere(inputstr, key, mode="decode"):
	ret = ""
	m = 0
	if(mode == "decode"):
		m = -1
	elif(mode == "encode"):
		m = 1
		
	for i in range(0, len(inputstr)):
		ret += chr(ord('A') + (ord(inputstr[i]) + m * ord(key[i % len(key)])) % 26)
	return ret;
	
def potentialkeys(frequencies, threshold):
	potentials = []
	for i in range(0, len(frequencies)):
		potentials.append([])
		for j in range(0, len(frequencies[i])):
			if(frequencies[i][j][1] > threshold):
				potentials[i].append(chr(((ord(frequencies[i][j][0]) - ord('E')) % 26) + ord('A'))) #Screw this statmenet
	keys = []
	for t in itertools.product(*potentials):
		keys.append("".join(t))
	return keys
		
	
input = ["","",""]
keylength = 5
ciphertexts = []
for i in range(0, keylength):
	ciphertexts.append([])
	for j in range(0, len(input)):
		for k in range(0, len(input[j])):
			if(k % keylength == i):
				ciphertexts[i].append(input[j][k])
arr = []
for i in range(0, len(ciphertexts)):
	arr.append(runandprint("CIPHER " + str(i + 1), frequency, ciphertexts[i]))
keys = potentialkeys(arr, 9)
for i in range(0, len(keys)):
	print(keys[i])
	printpretty(vigenere(input[0], keys[i]), 6, 60)
	print()
	
for i in range(0, len(input)):
	printpretty(vigenere(input[i], keys[0]), 6, 60)
