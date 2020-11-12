import requests
from bs4 import BeautifulSoup

languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese',
             'Romanian', 'Russian', 'Turkish']

print("Hello, you're welcome to the translator. Translator supports:")
for i in range(len(languages)):
    print(f"{i + 1}. {languages[i]}")

source_language = languages[int(input("Type the number of your language:\n")) - 1]
target_language_choice = int(input("Type the number of language you want to translate to or '0' to translate to all "
                                   "langauges:\n"))
source_word = input("Type the word you want to translate:\n").lower()

if target_language_choice:
    target_language = languages[target_language_choice - 1]
    r = requests.get(
        f"https://context.reverso.net/translation/{source_language.lower()}-{target_language.lower()}/{source_word}",
        headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, 'html.parser')

    t_words_div = soup.find('div', id='translations-content')
    word_list = []
    for t_word in t_words_div.find_all():
        word = t_word.get_text()
        word = word.replace("          ", "")
        word = word.replace("\n", "")
        if len(word):
            word_list.append(word)

    t_sentences = soup.find_all(class_='example')
    sentence_list = []
    for t_sentence in t_sentences:
        for sentence in t_sentence.find_all('div', limit=2):
            sentence = sentence.get_text()
            sentence = sentence.replace("\n", "")
            sentence = sentence.replace("          ", "")
            sentence_list.append(sentence)

    print(f"{target_language} Translations:")
    if len(word_list) <= 5:
        for word in word_list:
            print(word)
    else:
        for i in range(5):
            print(word_list[i])

    print(f"\n{target_language} Examples:")
    if len(sentence_list) <= 10:
        for i in range(len(sentence_list)):
            if i % 2 == 0:
                print(sentence_list[i] + ":")
            else:
                print(sentence_list[i] + "\n")
    else:
        for i in range(10):
            if i % 2 == 0:
                print(sentence_list[i] + ":")
            else:
                print(sentence_list[i] + "\n")
else:
    file = open(f"{source_word}.txt", 'w', encoding='utf-8')
    for i in range(len(languages)):
        if languages[i].lower() == source_language.lower():
            continue
        r = requests.get(
            f"https://context.reverso.net/translation/{source_language.lower()}-{languages[i].lower()}/{source_word}",
            headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, 'html.parser')

        t_words_div = soup.find('div', id='translations-content')
        t_word = t_words_div.find_all()[0]
        word = t_word.get_text()
        word = word.replace("          ", "")
        word = word.replace("\n", "")

        print(f"{languages[i]} Translations:")
        print(word + '\n')
        file.write(f"{languages[i]} Translations:\n")
        file.write(word + "\n")
        file.write('\n')

        t_sentences = soup.find_all(class_='example')
        sentence_list = []
        t_sentence = t_sentences[0]
        for sentence in t_sentence.find_all('div', limit=2):
            sentence = sentence.get_text()
            sentence = sentence.replace("\n", "")
            sentence = sentence.replace("          ", "")
            sentence_list.append(sentence)

        print(f"{languages[i]} Example:")
        print(sentence_list[0] + ":")
        print(sentence_list[1])
        print()
        file.write(f"{languages[i]} Example:\n")
        file.write(sentence_list[0] + ":\n")
        file.write(sentence_list[1] + "\n")
        file.write("\n")

        sentence_list.clear()
        t_word.clear()
        t_sentence.clear()
    file.close()
