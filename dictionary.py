from wordnik import *
import io
import random

def percent_vowels(word):
	if word.count('\'') == 0 or (word.count('\'') == 1 and random.random() > 0.6) or (word.count('\'') == 2 and random.random() > 0.95):
		return (word.count('a')+word.count('i')+word.count('u')+word.count('o'))/float(len(word))
	else:
		return 0;

def make_word():
	word = random.choice('aioubbbdffjnllkpppsttttttmaiobbbdffjnllkpppsttttttm')
	while random.randint(0,14-len(word)) != 0:
		if word[-1] == 'a':
			word += random.choice('bndkpstuxxxx')
		elif word[-1] == 'b':
			if len(word) > 2 and word[-2] != 'b': 
				word += random.choice('aioub\'x')
			else:	
				word += random.choice('aiou\'x')
		elif word[-1] == 'd':
			if len(word) > 2 and word[-2] != 'd': 
				word += random.choice('aioud\'xx')
			else:	
				word += random.choice('aiou\'xx')
		elif word[-1] == 'f':
			word += random.choice('aiol\'xx')
		elif word[-1] == 'j':
			word += random.choice('aio')
		elif word[-1] == 'i':
			word += random.choice('ibdfnlkptxxxxx')
		elif word[-1] == 'n':
			word += random.choice('aiudtks')
		elif word[-1] == 'l':
			if len(word) > 2 and word[-2] in 'aiou':
				word += random.choice('ioulktfp')
			else:
				word += random.choice('ioux')
		elif word[-1] == 'k':
			word += random.choice('iusx')
		elif word[-1] == 'p':
			word += random.choice('o\'x')
		elif word[-1] == 's':
			if len(word) > 2 and word[-2] in 'aiou':
				word += random.choice('tianslux\'')
			else:
				word += random.choice('tlia\'')
		elif word[-1] == 't':
			word += random.choice('aiouaiouaioutxxx')
		elif word[-1] == 'o':
			word += random.choice('fsnbdoklxxxx\'')
		elif word[-1] == 'u':
			word += random.choice('bpndxxx')
		elif word[-1] == '\'':
			word += random.choice('ntkl')
		elif word[-1] == 'm':
			word += random.choice('aiou\'')
		if word[-1] == 'x':
			word = word[:-1]
			break
	if percent_vowels(word) > 0.25 and percent_vowels(word) < 0.75 and len(word) > 3 and word[-1] != '\'':
		if random.random() > .99:
			return word + '-' + make_word()
		else:
			return word
	else:
		return make_word()

def unique_word():
	word = make_word()
	if words.count(word) == 0:
		return word
	else:
		return unique_word()
		
def check_definition(definition):
	for correction in correction_list:
		if definition[0:len(correction)] == correction:
			if random.random() > 0.6:
				return correction+make_word()+'.'
			else:
				return check_definition(get_def.getDefinitions(rand_word.getRandomWord().word,limit=1)[0].text)
	if definition[0:19] == 'The cardinal number':
		return 'The cardinal number equal to the sum of '+unique_word()+' and '+unique_word()+'.'
	return definition	
	
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '5a5dc229807e6f9ac7100019db5059207afa044bc21023efa'
client = swagger.ApiClient(apiKey, apiUrl)

rand_word = WordsApi.WordsApi(client)
get_def = WordApi.WordApi(client)
		
words = []
correction_list = ['Plural form of ','Alternative spelling of ','Alternative form of ','Common misspelling of ','Plural of ','Same as ','See ','Present participle of ','Third-person singular simple present indicative form of ','Simple past tense and past participle of ','Archaic form of ']

for i in range(0,8000):
	words.append(unique_word())

words.sort(cmp=lambda x,y: cmp("".join(l for l in x if l not in '\'-'), "".join(l for l in y if l not in '\'-')))

dictionary = "Selected Entries from the D'ksuban Dictionary\n2014 Edition"
cur_letter = ""

for word in words:
	try:
		if word[0] != cur_letter:
			cur_letter = word[0]
			dictionary += "\n\n"+cur_letter.capitalize()+":"+u"\u000A"
		definition = get_def.getDefinitions(rand_word.getRandomWord().word,limit=1)[0].text
		dictionary += u"\u000A"+word+": "
		dictionary+= check_definition(definition)
		print word
	except:
		print 'Took too long to respond'

file = io.open("Selected Entries from the D'ksuban Dictionary.txt",mode="w",encoding='utf-16')
file.write(dictionary)
file.close()
end_program = raw_input("Dictionary completed!")