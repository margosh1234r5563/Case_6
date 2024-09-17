# Part of case-study #6: Textwork
# Developer: Rusakova Margarita
#            Gulakova Yulia
#            Timofeev Ilia

from textblob import TextBlob
from translate import Translator

import ru_local as ru


def main():
    """
       Main function.
       :return: None
    """

    def proposal(s):
        """
        This function counts the number of propose
        :param s: text
        :return: counter
        """
        counter = 0
        counter += s.count('...')
        s = s.replace('...', '')
        counter += s.count('.')
        s = s.split()
        counter += len([i[-1] for i in s if i[-1] in '?!'])
        return counter

    def words(s):
        """
        This function counts the amount of words
        :param s: text
        :return: amount words
        """
        s = s.strip()
        return s.count(' ') + 1

    def syllables(s):
        """
        This function counts the amount of syllables
        :param s: text
        :return: counter
        """
        counter = 0
        alh = ru.SUBSTRING
        for i in s.lower():
            if i in alh:
                counter += 1
        return counter

    def includes_1(s):
        """
        This function counts the average sentence length in words
        :param s: text
        :return: average sentence length in words
        """
        return words(s) / proposal(s)

    def includes_2(s):
        """
         This function counts the average word length in syllables
         :param s: text
         :return: average word length in syllables
         """
        return syllables(s) / words(s)

    def identify_language(st):
        """
         This function is identify_language
         :param st: text
         :return: language
         """
        for symbol in st.lower():
            if ord(symbol) >= ord('a') and ord(symbol) <= ord('z'):
                return 'en'
            elif ord(symbol) >= ord('а') and ord(symbol) <= ord('я'):
                return 'ru'
            else:
                return 'undefined language'

    def polar_name(index):
        """
         This function is tone style
         :param index: amount of tonality
         :return: text style
         """
        if -1 < index < -0.3333:
            tone = ru.NEGATIVE
        elif -0.3333 < index < 0.3333:
            tone = ru.NEUTRAL
        elif 0.3333 < index < 1:
            tone = ru.POSITIVE
        return tone

    def polar(lang):
        """
         This function is identify the tone
         :param lang: text language
         :return: tonality
         """
        if lang == 'en':
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            tonal = polar_name(polarity)
        elif lang == 'ru':
            tr = Translator(from_lang='ru', to_lang='en')
            new_text = TextBlob(tr.translate(text))
            polarity = new_text.sentiment.polarity
            tonal = polar_name(polarity)
        return tonal

    def obj(lang):
        """
         This function is identify the objective
         :param lang: text language
         :return: objective
         """
        if lang == 'en':
            blob = TextBlob(text)
            sub = blob.sentiment.subjectivity
            sub = 1 - sub
            obj = '{:.1%}'.format(sub)
        elif lang == 'ru':
            tr = Translator(from_lang='ru', to_lang='en')
            new_text = TextBlob(tr.translate(text))
            sub = new_text.sentiment.subjectivity
            sub = 1 - sub
            obj = '{:.1%}'.format(sub)
        return obj

    def index_of_flesch(language, asl, asw):
        """
         This function is count Flesh index
         :param language: text's language
         :param asl: the average sentence length in words
         :param asw: the average word length in syllables
         :return: index of Flesh and text's level
         """
        if language == 'en':
            index = 206.835 - 1.015 * asl - 84.6 * asw
        elif language == 'ru':
            index = 206.835 - 1.3 * asl - 60.1 * asw
        else:
            print(language)
            return
        print(f'{ru.INDEX} {index}')
        if index > 80:
            print(ru.EASY)
        elif index > 50:
            print(ru.SIMPLE)
        elif index > 25:
            print(ru.MIDDLE)
        else:
            print(ru.DIFFICULT)

    text = input()
    test = identify_language(text)
    print(f'{ru.PROPOSAL} {proposal(text)}')
    print(f'{ru.WORDS} {words(text)}')
    print(f'{ru.SYLLABLES} {syllables(text)}')
    print(f'{ru.MIDDLE_LEGHT_1} {includes_1(text)}')
    print(f'{ru.MIDDLE_LEGHT_2} {includes_2(text)}')
    index_of_flesch(test, includes_1(text), includes_2(text))
    print(f'{ru.TON} {polar(test)}')
    print(f'{ru.OBJECTIVE} {obj(test)}')


if __name__ == '__main__':
    main()
