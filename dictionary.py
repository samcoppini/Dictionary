import io
import os
import random
import sys

from wordnik import *

def randchance(n):
	return random.randint(0, n - 1) == 0

def percent_vowels(word):
	num_vowels = 0
	for char in word:
		if char in 'aeiou':
			num_vowels += 1
	return num_vowels / len(word)

def make_word():
	letter_chances = {
		" ": "aabbbbbddffffiijjkkllllmmnnoopppppsstttttttttttu",
		"a": "bdknpstuxxxx",
		"b": "abiou'x",
		"d": "adiou'xx",
		"f": "ailo'xx",
		"i": "bdfiklnptxxxxx",
		"j": "aio",
		"k": "isux",
		"l": "fikloptu",
		"m": "aiou'",
		"n": "adikstu",
		"o": "bdfklnos'xxxx",
		"p": "o'x",
		"s": "ailnstu'x",
		"t": "ailnstu'x",
		"u": "bdnpxxx",
		"'": "klnt"
	}
	word = ""
	while not word:
		word = random.choice(letter_chances[" "])

		while not randchance(14 - len(word)) and word[-1] != 'x':
			word += random.choice(letter_chances[word[-1]])

		if 0.25 < percent_vowels(word) < 0.75 and len(word) > 3:
			if word[-1] == "'":
				word = word[:-1]
			if random.random() > .99:
				return word + '-' + make_word()
			else:
				return word
		else:
			word = ""

def unique_word():
	word = make_word()
	if words.count(word) == 0:
		return word
	else:
		return unique_word()

def get_random_definition():
	definition = word_api.getDefinitions(words_api.getRandomWord().word,limit=1)[0].text
	for correction in correction_list:
		if definition[:len(correction)] == correction:
			if random.random() > 0.6:
				return correction + make_word() + '.'
			else:
				return get_random_definition()
	if definition[:19] == 'The cardinal number':
		return ('The cardinal number equal to the sum of ' +
		        unique_word() + ' and ' + unique_word() + '.')
	return definition

apiUrl = 'http://api.wordnik.com/v4'
apiKey = os.getenv('API_KEY')
client = swagger.ApiClient(apiKey, apiUrl)

words_api = WordsApi.WordsApi(client)
word_api = WordApi.WordApi(client)

words = []
correction_list = [
	'Plural form of ',
	'Alternative spelling of ',
	'Alternative form of ',
	'Common misspelling of ',
	'Plural of ',
	'Same as ',
	'See ',
	'Present participle of ',
	'Third-person singular simple present indicative form of ',
	'Simple past tense and past participle of ',
	'Archaic form of ',
	'Variant of ',
    'Of or relating to ',
    'Of or pertaining to ',
]

if len(sys.argv) > 1:
	num_words = int(sys.argv[1])
else:
	num_words = 100

for i in range(num_words):
	words.append(unique_word())

words.sort(key=lambda s: ''.join(c for c in s if c not in '\'-'))

dictionary = ["Selected Entries from the D'ksuban Dictionary\n2014 Edition"]
cur_letter = ""

for word in words:
	if word[0] != cur_letter:
		cur_letter = word[0]
		dictionary += ["\n\n", cur_letter.capitalize(), ":\n"]
	dictionary += ["\n", word, ": "]
	dictionary.append(get_random_definition())
	print(word)

filename = "Selected Entries from the D'ksuban Dictionary.txt"
with io.open(filename, mode="w",encoding='utf-16') as file:
	file.write("".join(dictionary))

print("Dictionary completed!")
