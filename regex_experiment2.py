import re
import webbrowser
from bs4 import BeautifulSoup
from pprint import pprint
import requests
import csv
import queue
import time
import random
from requests_html import HTMLSession
import os
from openai import OpenAI
from itertools import chain

#Errors:
# Broken at 1567
#
#
#5682
for i in chain(range(5, 1858), range(3675, 5683)):
    i = str(i)
    url = "http://byu-studies-frontend.s3-website-us-west-2.amazonaws.com/article/"+i
    #webbrowser.open(url)

#scrapes the page
    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render(sleep=.50)

        soup = BeautifulSoup(response.html.html, 'html.parser')
        article = soup.find(class_='text-lg article lg:min-w-[700px] pb-10')
        article_text = article.text
    except Exception as e:
            print(f"An error occurred: {str(e)}")
    finally:
        session.close()

    def pattern_matching(article_text):
        all_matches = []
        patterns = [
            r'Bible',
            r'[bB]ooks of [A-Za-z]+ and [A-Za-z]+',
            r'Genesis (?:50|[1-4][0-9]|[1-9])|Genesis(?!\s*\d)',
            r'Gen\. (?:50|[1-4][0-9]|[1-9])|Gen\. (?!\s*\d)',
            r'Exodus (?:40|[1-3][0-9]|[1-9])|Exodus(?!\s*\d)',
            r'Ex\. (?:40|[1-3][0-9]|[1-9])|Ex\.(?!\s*\d)',
            r'Leviticus (?:27|[1-2][0-9]|[1-9])|Leviticus\. (?!\s*\d)',
            r'Lev\. (?:27|[1-2][0-9]|[1-9])|Lev\.(?!\s*\d)',
            r'Numbers (?:36|[1-3][0-9]|[1-9])|Numbers(?!\s*\d)',
            r'Num\. (?:36|[1-3][0-9]|[1-9])|Num\.(?!\s*\d)',
            r'Deuteronomy (?:34|[1-3][0-9]|[1-9])|Deuteronomy(?!\s*\d)',
            r'Joshua (?:24|[1-2][0-9]|[1-9])',
            r'Josh\. (?:24|[1-2][0-9]|[1-9])|Josh\.(?!\s*\d)',
            r'Judges (?:21|[1-2][0-9]|[1-9])|Judges(?!\s*\d)',
            r'Judg\. (?:21|[1-2][0-9]|[1-9])|Judg\.(?!\s*\d)',
            r'Ruth (?:[1-4])',
            r'Rut\. (?:[1-4])|Rut\.(?!\s*\d)',
            r'1 Samuel (?:31|[12][0-9]|[1-9])|1 Samuel(?!\s*\d)',
            r'1 Sam\. (?:31|[12][0-9]|[1-9])|1 Sam\.(?!\s*\d)',
            r'2 Samuel (?:24|[1-2][0-9]|[1-9])|2 Samuel(?!\s*\d)',
            r'2 Sam\. (?:24|[1-2][0-9]|[1-9])|2 Sam\.(?!\s*\d)',
            r'1 Kings (?:22|[1-2][0-9]|[1-9])|1 Kings(?!\s*\d)',
            r'2 Kings (?:25|[1-2][0-9]|[1-9])|2 Kings(?!\s*\d)',
            r'1 Chronicles (?:29|[1-2][0-9]|[1-9])|1 Chronicles(?!\s*\d)',
            r'2 Chronicles (?:36|[1-3][0-9]|[1-9])|2 Chronicles(?!\s*\d)',
            r'1 Chr. (?:29|[1-2][0-9]|[1-9])|1 Chr.(?!\s*\d)',
            r'2 Chr. (?:36|[1-3][0-9]|[1-9])|2 Chr.(?!\s*\d)',
            r'Ezra (?:10|[1-9])',#removed Ezra
            r'Nehemiah (?:13|[1-9]|1[0-2])|Nehemiah(?!\s*\d)',
            r'Neh\. (?:13|[1-9]|1[0-2])|Neh(?!\s*\d)',
            r'Esther (?:10|[1-9])',#removed Esther
            r'Job (?:42|[1-3][0-9]|[1-9])',#removed job
            r'Psalms (?:150|1[0-4][0-9]|[1-9][0-9]|[1-9])|Psalms(?!\s*\d)',
            r'Psalm (?:150|1[0-4][0-9]|[1-9][0-9]|[1-9])|Psalm(?!\s*\d)',
            r'Ps\. (?:150|1[0-4][0-9]|[1-9][0-9]|[1-9])|Ps\. (?!\s*\d)',
            r'Proverbs (?:31|[1-2][0-9]|[1-9])|Proverbs(?!\s*\d)',
            r'Prov\. (?:31|[1-2][0-9]|[1-9])|Prov\.(?!\s*\d)',
            r'Ecclesiastes (?:12|[1-9]|10|11)|Ecclesiastes(?!\s*\d)',
            r'Song of Solomon (?:[1-8])|Song of Solomon(?!\s*\d)',
            r'Song\. (?:[1-8])|Song(?!\s*\d)',
            r'Isaiah (?:66|[1-5][0-9]|[1-9])|',#removed Isaiah
            r'Isa\. (?:66|[1-5][0-9]|[1-9])|Isa\.(?!\s*\d)',
            r'Jeremiah (?:52|[1-4][0-9]|[1-9])',#removed Jeremiah
            r'Jer\. (?:52|[1-4][0-9]|[1-9])|Jer\. (?!\s*\d)',
            r'Lamentations (?:[1-5])|Lamentations(?!\s*\d)',
            r'Lam\. (?:[1-5])|Lam\.(?!\s*\d)',
            r'Ezekiel (?:48|[1-3][0-9]|[1-9])|Ezekiel(?!\s*\d)',
            r'Ezek\. (?:48|[1-3][0-9]|[1-9])|Ezek(?!\s*\d)',
            r'Daniel (?:12|[1-9]|10|11)',#removed Daniel
            r'Dan\. (?:12|[1-9]|10|11)|Dan\.(?!\s*\d)',
            r'Hosea (?:14|[1-9]|10|11|12|13)|Hosea(?!\s*\d)',
            r'Joel (?:[1-3])',#removed Joel
            r'Amos (?:[1-9])|Amos(?!\s*\d)',
            r'Jonah (?:[1-4])',#removed Jonah
            r'Micah (?:[1-7])|Micah(?!\s*\d)',
            r'Nahum (?:[1-3])|Nahum(?!\s*\d)',
            r'Habakkuk (?:[1-3])|Habakkuk(?!\s*\d)',
            r'Hab\. (?:[1-3])|Hab\. (?!\s*\d)',
            r'Zephaniah (?:[1-3])|Zephaniah(?!\s*\d)',
            r'Zeph\. (?:[1-3])|Zeph\.(?!\s*\d)',
            r'Haggai (?:[1-2])|Haggai(?!\s*\d)',
            r'Hag\. (?:[1-2])|Hag\.(?!\s*\d)',
            r'Zechariah (?:14|[1-9]|10|11|12|13)|Zechariah(?!\s*\d)',
            r'Zech\. (?:14|[1-9]|10|11|12|13)|Zech\.(?!\s*\d)',
            r'Malachi (?:[1-4])|Malachi(?!\s*\d)',
            r'Mal\. (?:[1-4])|Mal\.(?!\s*\d)',
            r'1 Nephi (?:22|[12][0-9]|[1-9])|1 Nephi(?!\s*\d)',
            r'1 Ne\. (?:22|[12][0-9]|[1-9])|1 Ne\.(?!\s*\d)',
            r'2 Nephi (?:3[0-3]|[12][0-9]|[1-9])|2 Nephi(?!\s*\d)',
            r'2 Ne\. (?:3[0-3]|[12][0-9]|[1-9])|2 Ne\. (?!\s*\d)',
            r'Jacob (?:[1-7])',#removed Jacob
            r'Enos 1',#removed Enos
            r'Jarom 1',#removed Jarom
            r'Omni 1',#removed Omni
            r'Words of Mormon',
            r'W of M',
            r'Mosiah (?:2[0-9]|[1-9])',#removed Mosiah
            r'Alma (?:6[0-3]|[1-5][0-9]|[1-9])',#removed Alma
            r'Helaman (?:1[0-6]|[1-9])|Helaman(?!\s*\d)',#remove Helaman
            r'Hel\. (?:1[0-6]|[1-9])|Hel\.(?!\s*\d)',
            r'3 Nephi (?:30|[12][0-9]|[1-9])|3 Nephi(?!\s*\d)',
            r'3 Ne\. (?:30|[12][0-9]|[1-9])|3 Ne\.(?!\s*\d)',
            r'4 Nephi',
            r'4 Ne.',
            #r'Book of Mormon|Mormon (?:[1-9])|Mormon(?!\s+Church\b)(?!\s*\d)',
            ##removed Mormon for future code
            r'Book of Mormon',
            r'Morm\. (?:[1-9])|Morm\.(?!\s*\d)',
            r'Ether (?:1[0-5]|[1-9])',#removed Ether
            r'Moro\. (?:10|[1-9])|Moro\.(?!\s*\d)',
            r'Moroni (?:10|[1-9])',#removed Moroni
            r'New Testament',
            r'Epistles of [A-Za-z]+,? [A-Za-z]+,? and [A-Za-z]+',
            r'Matthew (?:2[0-8]|1[0-9]|[1-9])',#remove Matthew
            r'Matt\. (?:2[0-8]|1[0-9]|[1-9])|Matt\.(?!\s*\d)',
            r'Mark (?:1[0-6]|[1-9])',#removed Mark
            r'Luke (?:2[0-4]|1[0-9]|[1-9])',# removed Luke
            r'Gospels of John',
            r'John (?:2[0-1]|1[0-9]|[1-9])',#removed John
            r'Acts (?:2[0-8]|1[0-9]|[1-9])|Acts(?!\s*\d)',
            r'Epistles of Paul',
            r'Romans (?:1[0-6]|[1-9])|Romans (?!\s*\d)',#removed Romans
            r'Rom\. (?:1[0-6]|[1-9])|Rom\. (?!\s*\d)',
            r'1 Corinthians (?:1[0-6]|[1-9])|1 Corinthians(?!\s*\d)',
            r'1 Cor\. (?:1[0-6]|[1-9])|1 Cor\.(?!\s*\d)',
            r'2 Corinthians (?:1[0-3]|[1-9])|2 Corinthians(?!\s*\d)',
            r'2 Cor\. (?:1[0-3]|[1-9])|2 Cor\.(?!\s*\d)',
            r'Galatians (?:[1-6])|Galatians(?!\s*\d)',
            r'Gal\. (?:[1-6])|Gal\.(?!\s*\d)',
            r'Ephesians (?:[1-6])|Ephesians(?!\s*\d)',
            r'Eph\. (?:[1-6])|Eph\.(?!\s*\d)',
            r'Philippians (?:[1-4])',#removed Philippians
            r'Philip\. (?:[1-4])',#removed Philip
            r'Colossians (?:[1-4])|Colossians(?!\s*\d)',
            r'Col\. (?:[1-4])|Col\.(?!\s*\d)',
            r'1 Thessalonians (?:[1-5])|1 Thessalonians(?!\s*\d)',
            r'1 Thes\. (?:[1-5])|1 Thes\.(?!\s*\d)',
            r'2 Thessalonians (?:[1-3])|2 Thessalonians(?!\s*\d)',
            r'2 Thes\. (?:[1-3])|2 Thes\. (?!\s*\d)',
            r'1 Timothy (?:[1-6])|1 Timothy(?!\s*\d)',
            r'1 Tim\. (?:[1-6])|1 Tim\.(?!\s*\d)',
            r'2 Timothy (?:[1-4])|2 Timothy(?!\s*\d)',
            r'2 Tim\. (?:[1-4])|2 Tim\.(?!\s*\d)',
            r'Titus (?:[1-3])|Titus(?!\s*\d)',
            r'Philemon',
            r'Philem.',
            r'Hebrews (?:1[0-3]|[1-9])|Hebrews(?!\s*\d)',
            r'Heb\. (?:1[0-3]|[1-9])|Heb\.(?!\s*\d)',
            #r'(?<!King\s)James (?:[1-5])|(?<!King\s)James(?!\s*\d)',
            #removed James
            r'(?<!King\s)James (?:[1-5])',
            r'Epistles of Peter',
            r'1 Peter (?:[1-5])|1 Peter(?!\s*\d)',
            r'1 Pet\. (?:[1-5])|1 Pet\. (?!\s*\d)',
            r'2 Peter (?:[1-3])|2 Peter(?!\s*\d)',
            r'2 Pet\. (?:[1-3])|2 Pet\.(?!\s*\d)',
            r'Epistles of John',
            r'1 John (?:[1-5])|1 John(?!\s*\d)',
            r'1 Jn\. (?:[1-5])|1 Jn\. (?!\s*\d)',
            r'2 John',
            r'2 Jn.',
            r'3 John',
            r'3 Jn.',
            r'Jude 1',#removed Jude
            r'Revelation (?:2[0-2]|1[0-9]|[1-9])|Revelation(?!\s*\d)',
            r'Rev\. (?:2[0-2]|1[0-9]|[1-9])|Rev\. (?!\s*\d)',
            r'Doctrine and Covenants (?:1[0-3][0-8]|[1-9][0-9]|[1-9])|Doctrine and Covenants(?!\s*\d)',
            r'D&C (?:1[0-3][0-8]|[1-9][0-9]|[1-9])|D&C (?!\s*\d)',
            r'Moses (?:[1-8])|Moses\. (?!\s*\d)',#removed Moses
            r'Abraham (?:[1-5])',#removed Abraham
            r'Abr\. (?:[1-5])|Abr\. (?!\s*\d)',
            r'Facsimile (?:[1-3])|Facsimile (?!\s*\d)',
            r'Joseph Smith-Matthew',
            r'JS-M',
            r'Joseph Smith History',
            r'Joseph Smith—History',
            r'Articles of Faith',
            r'A of F',
            r'Joseph Smith Translation',
            r'JST',
            r'Ten Commandments',
            r'10 Commandments',
            r'Title Page of the Book of Mormon',
            r'Testimony of the Twelve Apostles from the Book of Mormon'
            ]
        for pattern in patterns:
            matches = re.findall(pattern, article_text)
            if matches:
                #print(matches)
                all_matches.extend(matches)
        if matches == False:
                all_matches = ["No scriptures"]
        #print(all_matches)
        return all_matches
    

    def abreviation_remover(unique_items):
        replaced_unique_items = []
        patterns_abreviation = r'\b([1-3]?\s*[A-Za-z]+\s?[A-Za-z]+?\s?+[A-Za-z]+\.?\s?\d*?)$'
        #print(unique_items)
        for unique_item in unique_items:
            unique_item = unique_item.strip()
            #print(unique_item)
            matches_abreviation = re.findall(patterns_abreviation, unique_item)
            #print(matches_abreviation)
            if matches_abreviation:
                unique_item = unique_item.replace("Gen.", "Genesis")
                unique_item = unique_item.replace("Ge.", "Genesis")
                unique_item = unique_item.replace("Gn.", "Genesis")
                unique_item = unique_item.replace("Exod.", "Exodus")
                unique_item = unique_item.replace("Exo.", "Exodus")
                unique_item = unique_item.replace("Ex.", "Exodus")
                unique_item = unique_item.replace("Lev.", "Leviticus")
                unique_item = unique_item.replace("Le.", "Leviticus")
                unique_item = unique_item.replace("Lv.", "Leviticus")
                unique_item = unique_item.replace("Num.", "Numbers")
                unique_item = unique_item.replace("Nu.", "Numbers")
                unique_item = unique_item.replace("Nm.", "Numbers")
                unique_item = unique_item.replace("Nb.", "Numbers")
                unique_item = unique_item.replace("Deut.", "Deuteronomy")
                unique_item = unique_item.replace("De.", "Deuteronomy")
                unique_item = unique_item.replace("Dt.", "Deuteronomy")
                unique_item = unique_item.replace("Josh.", "Joshua")
                unique_item = unique_item.replace("Jos.", "Joshua")
                unique_item = unique_item.replace("Jsh.", "Joshua")
                unique_item = unique_item.replace("Josh.", "Joshua")
                unique_item = unique_item.replace("Rth.", "Ruth")
                unique_item = unique_item.replace("Ru.", "Ruth")
                unique_item = unique_item.replace("1 Sam.", "1 Samuel")
                unique_item = unique_item.replace("1 Sa.", "1 Samuel")
                unique_item = unique_item.replace("1 S.", "1 Samuel")
                unique_item = unique_item.replace("1 Sm.", "1 Samuel")
                unique_item = unique_item.replace("2 Sam.", "2 Samuel")
                unique_item = unique_item.replace("2 Sa.", "2 Samuel")
                unique_item = unique_item.replace("2 S.", "2 Samuel")
                unique_item = unique_item.replace("2 Sm.", "2 Samuel")
                unique_item = unique_item.replace("1 Kgs.", "1 Kings")
                unique_item = unique_item.replace("1Kgs.", "1 Kings")
                unique_item = unique_item.replace("1 Ki.", "1 Kings")
                unique_item = unique_item.replace("1Ki.", "1 Kings")
                unique_item = unique_item.replace("1Kin.", "1 Kings")
                unique_item = unique_item.replace("1K.", "1 Kings")
                unique_item = unique_item.replace("2 Kgs.", "2 Kings")
                unique_item = unique_item.replace("2Kgs.", "2 Kings")
                unique_item = unique_item.replace("2 Ki.", "2 Kings")
                unique_item = unique_item.replace("2Ki.", "2 Kings")
                unique_item = unique_item.replace("2Kin.", "2 Kings")
                unique_item = unique_item.replace("2K.", "2 Kings")
                unique_item = unique_item.replace("2 Chron.", "1 Kings")
                unique_item = unique_item.replace("2 Ch.", "1 Kings")
                unique_item = unique_item.replace("2Ch.", "1 Kings")
                unique_item = unique_item.replace("2Chr.", "1 Kings")
                unique_item = unique_item.replace("2Chron.", "1 Kings")
                unique_item = unique_item.replace("Ezr.", "Ezra")
                unique_item = unique_item.replace("Ez.", "Ezra")
                unique_item = unique_item.replace("Jb.", "Job")
                unique_item = re.sub(r"Psalm(?=\s+\d+)|Psalm(?![sS])", "Psalms", unique_item)
                unique_item = unique_item.replace("Pslm.", "Psalms")
                unique_item = unique_item.replace("Ps.", "Psalms")
                unique_item = unique_item.replace("Psa.", "Psalms")
                unique_item = unique_item.replace("Psm.", "Psalms")
                unique_item = unique_item.replace("Pss.", "Psalms")
                unique_item = unique_item.replace("Prov.", "Proverbs")
                unique_item = unique_item.replace("Pro.", "Proverbs")
                unique_item = unique_item.replace("Pr.", "Proverbs")
                unique_item = unique_item.replace("Prv.", "Proverbs")
                unique_item = unique_item.replace("Eccles.", "Ecclesiastes")
                unique_item = unique_item.replace("Eccle.", "Ecclesiastes")
                unique_item = unique_item.replace("Ecc.", "Ecclesiastes")
                unique_item = unique_item.replace("Ec.", "Ecclesiastes")
                unique_item = unique_item.replace("Qoh.", "Ecclesiastes")
                unique_item = unique_item.replace("Song of Songs.", "Song of Solomon")
                unique_item = unique_item.replace("Song.", "Song of Solomon")
                unique_item = unique_item.replace("So.", "Song of Solomon")
                unique_item = unique_item.replace("SOS.", "Song of Solomon")
                unique_item = unique_item.replace("Canticle of Canticles.", "Song of Solomon")
                unique_item = unique_item.replace("Canticles.", "Song of Solomon")
                unique_item = unique_item.replace("Cant", "Song of Solomon")
                unique_item = unique_item.replace("Isa.", "Isaiah")
                unique_item = unique_item.replace("Is.", "Isaiah")
                unique_item = unique_item.replace("Jeremiah.", "Jer")
                unique_item = unique_item.replace("Jeremiah", "Je")
                unique_item = unique_item.replace("Jeremiah.", "Jr")
                unique_item = unique_item.replace("Lam.", "Lamentations")
                unique_item = unique_item.replace("La.", "Lamentations")
                unique_item = unique_item.replace("Ezek.", "Ezekiel")
                unique_item = unique_item.replace("Eze.", "Ezekiel")
                unique_item = unique_item.replace("Ezk.", "Ezekiel")
                unique_item = unique_item.replace("Dan.", "Daniel")
                unique_item = unique_item.replace("Da.", "Daniel")
                unique_item = unique_item.replace("Dn.", "Daniel")
                unique_item = unique_item.replace("Hos.", "Hosea")
                unique_item = unique_item.replace("Ho.", "Hosea")
                unique_item = unique_item.replace("Joe.", "Joel")
                unique_item = unique_item.replace("Jl.", "Joel")
                unique_item = unique_item.replace("Jl.", "Joel")
                unique_item = unique_item.replace("Am.", "Amos")
                unique_item = unique_item.replace("Obad.", "Obadiah")
                unique_item = unique_item.replace("Ob.", "Obadiah")
                unique_item = unique_item.replace("Jnh.", "Jonah")
                unique_item = unique_item.replace("Jon.", "Jonah")
                unique_item = unique_item.replace("Micah.", "Micah")
                unique_item = unique_item.replace("Mic.", "Micah")
                unique_item = unique_item.replace("Mc.", "Micah")
                unique_item = unique_item.replace("Nah.", "Nahum")
                unique_item = unique_item.replace("Na.", "Nahum")
                unique_item = unique_item.replace("Hab.", "Habakkuk")
                unique_item = unique_item.replace("Hb.", "Habakkuk")
                unique_item = unique_item.replace("Zech.", "Zechariah")
                unique_item = unique_item.replace("Zec.", "Zechariah")
                unique_item = unique_item.replace("Zc.", "Zechariah")
                unique_item = unique_item.replace("Mal.", "Malachi")
                unique_item = unique_item.replace("Ml.", "Malachi")
                unique_item = unique_item.replace("1 Ne.", "1 Nephi")
                unique_item = unique_item.replace("2 Ne.", "2 Nephi")
                unique_item = unique_item.replace("Jacob.", "Jacob")
                unique_item = unique_item.replace("Enos.", "Enos")
                unique_item = unique_item.replace("Jarom.", "Jarom")
                unique_item = unique_item.replace("Omni.", "Omni")
                unique_item = unique_item.replace("W of M", "Words of Mormon")
                unique_item = unique_item.replace("Mosiah.", "Mosiah")
                unique_item = unique_item.replace("Alma.", "Alma")
                unique_item = unique_item.replace("Hel.", "Helaman")
                unique_item = unique_item.replace("3 Ne.", "3 Nephi")
                unique_item = unique_item.replace("4 Ne.", "4 Nephi")
                unique_item = unique_item.replace("Morm.", "Mormon")
                unique_item = unique_item.replace("Ether.", "Ether")
                unique_item = unique_item.replace("Moro.", "Moroni")

                replaced_unique_items.append(unique_item)
                #print(replaced_unique_items)
            else:
                replaced_unique_items.append(unique_item)
        return replaced_unique_items

    def remove_duplicates(items):
        """Remove duplicate items from a list."""
        #print(items)
        seen = set()
        unique_items = []
        for item in items:
            
            if item not in seen:
                unique_items.append(item)
                seen.add(item)
        #print(unique_items)
        return unique_items

    def process_scriptures(article_text):
        pattern_matched = pattern_matching(article_text)
        #print(pattern_matched)
        abreviation_removed = abreviation_remover(pattern_matched)
        abreviation_removed = [item for item in abreviation_removed if item]
        #print(abreviation_removed)
        final_scriptures = remove_duplicates(abreviation_removed)
        if final_scriptures == []:
            final_scriptures = ["No scriptures"]
        return final_scriptures

    scriptures = process_scriptures(article_text)
    #print(scriptures)
    matches_string = ", ".join(scriptures)
    matches_string_list = matches_string+"+"+str(i)
    #matches_string_formatted = ", ".join(matches_string_list)
    with open('regex_experiment2.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([matches_string_list])
                #writer.writerow(["+"])
                #writer.writerow([i])
    print(matches_string + i)

#text = """"""

#Issues:
#Mormon the prophet vs Mormon the people vs Mormon the book (solution) adjetive identifier
#Prophets name's vs scripture titles

#Plan:
#1. adjust the code to look for chapters for the titles that are also names(done)
#2. implement the scraper and add to a csv file(done)
#3. duplicate code and make a variation that looks only for Mormon(done)
#4. implement adjective api(done and not needed)
#5. combined the two spread sheets
#6. duplicate code and make a variation that looks only for Prophet names
#7. Depending on number Lots: use chatgpt scrapter to explicitly say this refers to the book. Little: manually look at articles sections.




