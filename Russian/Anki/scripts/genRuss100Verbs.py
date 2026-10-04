#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anki deck generator: 100 most-used Russian verbs with conjugations and audio.
Uses edge-tts for TTS and genanki to build the .apkg file.
"""

import asyncio
import tempfile
from pathlib import Path

import edge_tts
import genanki

# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------
VOICE = "ru-RU-SvetlanaNeural"   # Female voice. For male: "ru-RU-DmitryNeural"
RATE = "+0%"
DECK_NAME = "Russian: 100 Verbs with Audio"
OUTPUT_FILE = "russian_100_verbs_audio.apkg"

TEMP_DIR = Path(tempfile.mkdtemp(prefix="anki_audio_"))

# ----------------------------------------------------------------------
# DATA: 100 VERBS
# Each entry: infinitive, English translation, 6 present-tense forms
# (I, you, he/she, we, you-pl, they), Russian example, English translation.
# ----------------------------------------------------------------------
VERBOS = [
    {"inf":"делать","trans":"to do / to make","conj":{"я":"делаю","ты":"делаешь","он/она":"делает","мы":"делаем","вы":"делаете","они":"делают"},"frase_ru":"Я делаю уроки.","frase_en":"I am doing homework."},
    {"inf":"говорить","trans":"to speak","conj":{"я":"говорю","ты":"говоришь","он/она":"говорит","мы":"говорим","вы":"говорите","они":"говорят"},"frase_ru":"Я говорю по-русски.","frase_en":"I speak Russian."},
    {"inf":"знать","trans":"to know","conj":{"я":"знаю","ты":"знаешь","он/она":"знает","мы":"знаем","вы":"знаете","они":"знают"},"frase_ru":"Я знаю это слово.","frase_en":"I know this word."},
    {"inf":"хотеть","trans":"to want","conj":{"я":"хочу","ты":"хочешь","он/она":"хочет","мы":"хотим","вы":"хотите","они":"хотят"},"frase_ru":"Я хочу чай.","frase_en":"I want tea."},
    {"inf":"идти","trans":"to go (on foot)","conj":{"я":"иду","ты":"идёшь","он/она":"идёт","мы":"идём","вы":"идёте","они":"идут"},"frase_ru":"Я иду домой.","frase_en":"I am going home."},
    {"inf":"думать","trans":"to think","conj":{"я":"думаю","ты":"думаешь","он/она":"думает","мы":"думаем","вы":"думаете","они":"думают"},"frase_ru":"Я думаю о тебе.","frase_en":"I think about you."},
    {"inf":"работать","trans":"to work","conj":{"я":"работаю","ты":"работаешь","он/она":"работает","мы":"работаем","вы":"работаете","они":"работают"},"frase_ru":"Он работает здесь.","frase_en":"He works here."},
    {"inf":"жить","trans":"to live","conj":{"я":"живу","ты":"живёшь","он/она":"живёт","мы":"живём","вы":"живёте","они":"живут"},"frase_ru":"Я живу в Москве.","frase_en":"I live in Moscow."},
    {"inf":"любить","trans":"to love","conj":{"я":"люблю","ты":"любишь","он/она":"любит","мы":"любим","вы":"любите","они":"любят"},"frase_ru":"Я люблю кофе.","frase_en":"I love coffee."},
    {"inf":"видеть","trans":"to see","conj":{"я":"вижу","ты":"видишь","он/она":"видит","мы":"видим","вы":"видите","они":"видят"},"frase_ru":"Я вижу дом.","frase_en":"I see a house."},
    {"inf":"слышать","trans":"to hear","conj":{"я":"слышу","ты":"слышишь","он/она":"слышит","мы":"слышим","вы":"слышите","они":"слышат"},"frase_ru":"Я слышу музыку.","frase_en":"I hear music."},
    {"inf":"читать","trans":"to read","conj":{"я":"читаю","ты":"читаешь","он/она":"читает","мы":"читаем","вы":"читаете","они":"читают"},"frase_ru":"Я читаю книгу.","frase_en":"I am reading a book."},
    {"inf":"писать","trans":"to write","conj":{"я":"пишу","ты":"пишешь","он/она":"пишет","мы":"пишем","вы":"пишете","они":"пишут"},"frase_ru":"Он пишет письмо.","frase_en":"He is writing a letter."},
    {"inf":"пить","trans":"to drink","conj":{"я":"пью","ты":"пьёшь","он/она":"пьёт","мы":"пьём","вы":"пьёте","они":"пьют"},"frase_ru":"Я пью воду.","frase_en":"I drink water."},
    {"inf":"есть","trans":"to eat","conj":{"я":"ем","ты":"ешь","он/она":"ест","мы":"едим","вы":"едите","они":"едят"},"frase_ru":"Мы едим яблоко.","frase_en":"We are eating an apple."},
    {"inf":"спать","trans":"to sleep","conj":{"я":"сплю","ты":"спишь","он/она":"спит","мы":"спим","вы":"спите","они":"спят"},"frase_ru":"Она спит.","frase_en":"She is sleeping."},
    {"inf":"смотреть","trans":"to watch / to look","conj":{"я":"смотрю","ты":"смотришь","он/она":"смотрит","мы":"смотрим","вы":"смотрите","они":"смотрят"},"frase_ru":"Я смотрю фильм.","frase_en":"I am watching a movie."},
    {"inf":"давать","trans":"to give","conj":{"я":"даю","ты":"даёшь","он/она":"даёт","мы":"даём","вы":"даёте","они":"дают"},"frase_ru":"Он даёт мне книгу.","frase_en":"He gives me a book."},
    {"inf":"понимать","trans":"to understand","conj":{"я":"понимаю","ты":"понимаешь","он/она":"понимает","мы":"понимаем","вы":"понимаете","они":"понимают"},"frase_ru":"Я понимаю тебя.","frase_en":"I understand you."},
    {"inf":"брать","trans":"to take","conj":{"я":"беру","ты":"берёшь","он/она":"берёт","мы":"берём","вы":"берёте","они":"берут"},"frase_ru":"Я беру такси.","frase_en":"I am taking a taxi."},
    {"inf":"ходить","trans":"to go (habitually)","conj":{"я":"хожу","ты":"ходишь","он/она":"ходит","мы":"ходим","вы":"ходите","они":"ходят"},"frase_ru":"Я хожу в школу.","frase_en":"I go to school."},
    {"inf":"ехать","trans":"to go (by vehicle)","conj":{"я":"еду","ты":"едешь","он/она":"едет","мы":"едем","вы":"едете","они":"едут"},"frase_ru":"Мы едем в парк.","frase_en":"We are going to the park."},
    {"inf":"играть","trans":"to play","conj":{"я":"играю","ты":"играешь","он/она":"играет","мы":"играем","вы":"играете","они":"играют"},"frase_ru":"Дети играют.","frase_en":"The children are playing."},
    {"inf":"петь","trans":"to sing","conj":{"я":"пою","ты":"поёшь","он/она":"поёт","мы":"поём","вы":"поёте","они":"поют"},"frase_ru":"Она поёт песню.","frase_en":"She is singing a song."},
    {"inf":"танцевать","trans":"to dance","conj":{"я":"танцую","ты":"танцуешь","он/она":"танцует","мы":"танцуем","вы":"танцуете","они":"танцуют"},"frase_ru":"Я танцую.","frase_en":"I dance."},
    {"inf":"бежать","trans":"to run","conj":{"я":"бегу","ты":"бежишь","он/она":"бежит","мы":"бежим","вы":"бежите","они":"бегут"},"frase_ru":"Он бежит.","frase_en":"He runs."},
    {"inf":"плавать","trans":"to swim","conj":{"я":"плаваю","ты":"плаваешь","он/она":"плавает","мы":"плаваем","вы":"плаваете","они":"плавают"},"frase_ru":"Я плаваю в море.","frase_en":"I swim in the sea."},
    {"inf":"готовить","trans":"to cook / to prepare","conj":{"я":"готовлю","ты":"готовишь","он/она":"готовит","мы":"готовим","вы":"готовите","они":"готовят"},"frase_ru":"Мама готовит ужин.","frase_en":"Mom is cooking dinner."},
    {"inf":"мыть","trans":"to wash","conj":{"я":"мою","ты":"моешь","он/она":"моет","мы":"моем","вы":"моете","они":"моют"},"frase_ru":"Я мою руки.","frase_en":"I wash my hands."},
    {"inf":"стоять","trans":"to stand","conj":{"я":"стою","ты":"стоишь","он/она":"стоит","мы":"стоим","вы":"стоите","они":"стоят"},"frase_ru":"Он стоит там.","frase_en":"He is standing there."},
    {"inf":"сидеть","trans":"to sit","conj":{"я":"сижу","ты":"сидишь","он/она":"сидит","мы":"сидим","вы":"сидите","они":"сидят"},"frase_ru":"Я сижу на стуле.","frase_en":"I sit on a chair."},
    {"inf":"лежать","trans":"to lie (down)","conj":{"я":"лежу","ты":"лежишь","он/она":"лежит","мы":"лежим","вы":"лежите","они":"лежат"},"frase_ru":"Книга лежит на столе.","frase_en":"The book lies on the table."},
    {"inf":"помнить","trans":"to remember","conj":{"я":"помню","ты":"помнишь","он/она":"помнит","мы":"помним","вы":"помните","они":"помнят"},"frase_ru":"Я помню тебя.","frase_en":"I remember you."},
    {"inf":"помогать","trans":"to help","conj":{"я":"помогаю","ты":"помогаешь","он/она":"помогает","мы":"помогаем","вы":"помогаете","они":"помогают"},"frase_ru":"Я помогаю маме.","frase_en":"I help mom."},
    {"inf":"показывать","trans":"to show","conj":{"я":"показываю","ты":"показываешь","он/она":"показывает","мы":"показываем","вы":"показываете","они":"показывают"},"frase_ru":"Он показывает фото.","frase_en":"He shows a photo."},
    {"inf":"рассказывать","trans":"to tell","conj":{"я":"рассказываю","ты":"рассказываешь","он/она":"рассказывает","мы":"рассказываем","вы":"рассказываете","они":"рассказывают"},"frase_ru":"Она рассказывает историю.","frase_en":"She tells a story."},
    {"inf":"спрашивать","trans":"to ask","conj":{"я":"спрашиваю","ты":"спрашиваешь","он/она":"спрашивает","мы":"спрашиваем","вы":"спрашиваете","они":"спрашивают"},"frase_ru":"Я спрашиваю учителя.","frase_en":"I ask the teacher."},
    {"inf":"отвечать","trans":"to answer","conj":{"я":"отвечаю","ты":"отвечаешь","он/она":"отвечает","мы":"отвечаем","вы":"отвечаете","они":"отвечают"},"frase_ru":"Он отвечает правильно.","frase_en":"He answers correctly."},
    {"inf":"звонить","trans":"to call (by phone)","conj":{"я":"звоню","ты":"звонишь","он/она":"звонит","мы":"звоним","вы":"звоните","они":"звонят"},"frase_ru":"Я звоню другу.","frase_en":"I call a friend."},
    {"inf":"ждать","trans":"to wait","conj":{"я":"жду","ты":"ждёшь","он/она":"ждёт","мы":"ждём","вы":"ждёте","они":"ждут"},"frase_ru":"Я жду автобус.","frase_en":"I am waiting for the bus."},
    {"inf":"искать","trans":"to look for","conj":{"я":"ищу","ты":"ищешь","он/она":"ищет","мы":"ищем","вы":"ищете","они":"ищут"},"frase_ru":"Я ищу ключи.","frase_en":"I am looking for my keys."},
    {"inf":"получать","trans":"to receive","conj":{"я":"получаю","ты":"получаешь","он/она":"получает","мы":"получаем","вы":"получаете","они":"получают"},"frase_ru":"Я получаю письмо.","frase_en":"I receive a letter."},
    {"inf":"посылать","trans":"to send","conj":{"я":"посылаю","ты":"посылаешь","он/она":"посылает","мы":"посылаем","вы":"посылаете","они":"посылают"},"frase_ru":"Он посылает сообщение.","frase_en":"He sends a message."},
    {"inf":"встречать","trans":"to meet","conj":{"я":"встречаю","ты":"встречаешь","он/она":"встречает","мы":"встречаем","вы":"встречаете","они":"встречают"},"frase_ru":"Я встречаю друга.","frase_en":"I meet a friend."},
    {"inf":"узнавать","trans":"to find out","conj":{"я":"узнаю","ты":"узнаёшь","он/она":"узнаёт","мы":"узнаём","вы":"узнаёте","они":"узнают"},"frase_ru":"Я узнаю новости.","frase_en":"I find out the news."},
    {"inf":"решать","trans":"to decide / to solve","conj":{"я":"решаю","ты":"решаешь","он/она":"решает","мы":"решаем","вы":"решаете","они":"решают"},"frase_ru":"Он решает задачу.","frase_en":"He solves the problem."},
    {"inf":"нравиться","trans":"to like (to be pleasing)","conj":{"я":"нравлюсь","ты":"нравишься","он/она":"нравится","мы":"нравимся","вы":"нравитесь","они":"нравятся"},"frase_ru":"Мне нравится чай.","frase_en":"I like tea."},
    {"inf":"менять","trans":"to change","conj":{"я":"меняю","ты":"меняешь","он/она":"меняет","мы":"меняем","вы":"меняете","они":"меняют"},"frase_ru":"Я меняю работу.","frase_en":"I am changing jobs."},
    {"inf":"возвращаться","trans":"to return","conj":{"я":"возвращаюсь","ты":"возвращаешься","он/она":"возвращается","мы":"возвращаемся","вы":"возвращаетесь","они":"возвращаются"},"frase_ru":"Я возвращаюсь домой.","frase_en":"I return home."},
    {"inf":"носить","trans":"to wear / to carry","conj":{"я":"ношу","ты":"носишь","он/она":"носит","мы":"носим","вы":"носите","они":"носят"},"frase_ru":"Она носит платье.","frase_en":"She wears a dress."},
    {"inf":"водить","trans":"to drive","conj":{"я":"вожу","ты":"водишь","он/она":"водит","мы":"водим","вы":"водите","они":"водят"},"frase_ru":"Он водит машину.","frase_en":"He drives a car."},
    {"inf":"уметь","trans":"to know how to","conj":{"я":"умею","ты":"умеешь","он/она":"умеет","мы":"умеем","вы":"умеете","они":"умеют"},"frase_ru":"Я умею плавать.","frase_en":"I can swim."},
    {"inf":"оставаться","trans":"to stay / to remain","conj":{"я":"остаюсь","ты":"остаёшься","он/она":"остаётся","мы":"остаёмся","вы":"остаётесь","они":"остаются"},"frase_ru":"Я остаюсь дома.","frase_en":"I stay at home."},
    {"inf":"выходить","trans":"to go out / to exit","conj":{"я":"выхожу","ты":"выходишь","он/она":"выходит","мы":"выходим","вы":"выходите","они":"выходят"},"frase_ru":"Я выхожу из дома.","frase_en":"I go out of the house."},
    {"inf":"входить","trans":"to enter","conj":{"я":"вхожу","ты":"входишь","он/она":"входит","мы":"входим","вы":"входите","они":"входят"},"frase_ru":"Он входит в класс.","frase_en":"He enters the classroom."},
    {"inf":"приезжать","trans":"to arrive (by vehicle)","conj":{"я":"приезжаю","ты":"приезжаешь","он/она":"приезжает","мы":"приезжаем","вы":"приезжаете","они":"приезжают"},"frase_ru":"Она приезжает завтра.","frase_en":"She arrives tomorrow."},
    {"inf":"уезжать","trans":"to leave (by vehicle)","conj":{"я":"уезжаю","ты":"уезжаешь","он/она":"уезжает","мы":"уезжаем","вы":"уезжаете","они":"уезжают"},"frase_ru":"Мы уезжаем в отпуск.","frase_en":"We leave on vacation."},
    {"inf":"открывать","trans":"to open","conj":{"я":"открываю","ты":"открываешь","он/она":"открывает","мы":"открываем","вы":"открываете","они":"открывают"},"frase_ru":"Я открываю окно.","frase_en":"I open the window."},
    {"inf":"закрывать","trans":"to close","conj":{"я":"закрываю","ты":"закрываешь","он/она":"закрывает","мы":"закрываем","вы":"закрываете","они":"закрывают"},"frase_ru":"Он закрывает дверь.","frase_en":"He closes the door."},
    {"inf":"покупать","trans":"to buy","conj":{"я":"покупаю","ты":"покупаешь","он/она":"покупает","мы":"покупаем","вы":"покупаете","они":"покупают"},"frase_ru":"Я покупаю хлеб.","frase_en":"I buy bread."},
    {"inf":"продавать","trans":"to sell","conj":{"я":"продаю","ты":"продаёшь","он/она":"продаёт","мы":"продаём","вы":"продаёте","они":"продают"},"frase_ru":"Он продаёт машину.","frase_en":"He sells a car."},
    {"inf":"изучать","trans":"to study (a subject)","conj":{"я":"изучаю","ты":"изучаешь","он/она":"изучает","мы":"изучаем","вы":"изучаете","они":"изучают"},"frase_ru":"Я изучаю русский.","frase_en":"I study Russian."},
    {"inf":"учить","trans":"to learn / to teach","conj":{"я":"учу","ты":"учишь","он/она":"учит","мы":"учим","вы":"учите","они":"учат"},"frase_ru":"Я учу слова.","frase_en":"I am learning words."},
    {"inf":"учиться","trans":"to study (be a student)","conj":{"я":"учусь","ты":"учишься","он/она":"учится","мы":"учимся","вы":"учитесь","они":"учатся"},"frase_ru":"Она учится в университете.","frase_en":"She studies at university."},
    {"inf":"мечтать","trans":"to dream","conj":{"я":"мечтаю","ты":"мечтаешь","он/она":"мечтает","мы":"мечтаем","вы":"мечтаете","они":"мечтают"},"frase_ru":"Я мечтаю о море.","frase_en":"I dream about the sea."},
    {"inf":"гулять","trans":"to walk / to stroll","conj":{"я":"гуляю","ты":"гуляешь","он/она":"гуляет","мы":"гуляем","вы":"гуляете","они":"гуляют"},"frase_ru":"Мы гуляем в парке.","frase_en":"We walk in the park."},
    {"inf":"отдыхать","trans":"to rest","conj":{"я":"отдыхаю","ты":"отдыхаешь","он/она":"отдыхает","мы":"отдыхаем","вы":"отдыхаете","они":"отдыхают"},"frase_ru":"Я отдыхаю дома.","frase_en":"I rest at home."},
    {"inf":"летать","trans":"to fly","conj":{"я":"летаю","ты":"летаешь","он/она":"летает","мы":"летаем","вы":"летаете","они":"летают"},"frase_ru":"Птицы летают.","frase_en":"Birds fly."},
    {"inf":"дарить","trans":"to give (as a gift)","conj":{"я":"дарю","ты":"даришь","он/она":"дарит","мы":"дарим","вы":"дарите","они":"дарят"},"frase_ru":"Я дарю цветы.","frase_en":"I give flowers."},
    {"inf":"курить","trans":"to smoke","conj":{"я":"курю","ты":"куришь","он/она":"курит","мы":"курим","вы":"курите","они":"курят"},"frase_ru":"Он курит.","frase_en":"He smokes."},
    {"inf":"болеть","trans":"to be sick","conj":{"я":"болею","ты":"болеешь","он/она":"болеет","мы":"болеем","вы":"болеете","они":"болеют"},"frase_ru":"Я болею.","frase_en":"I am sick."},
    {"inf":"лечить","trans":"to treat (medically)","conj":{"я":"лечу","ты":"лечишь","он/она":"лечит","мы":"лечим","вы":"лечите","они":"лечат"},"frase_ru":"Врач лечит пациента.","frase_en":"The doctor treats the patient."},
    {"inf":"чувствовать","trans":"to feel","conj":{"я":"чувствую","ты":"чувствуешь","он/она":"чувствует","мы":"чувствуем","вы":"чувствуете","они":"чувствуют"},"frase_ru":"Я чувствую себя хорошо.","frase_en":"I feel good."},
    {"inf":"волноваться","trans":"to worry","conj":{"я":"волнуюсь","ты":"волнуешься","он/она":"волнуется","мы":"волнуемся","вы":"волнуетесь","они":"волнуются"},"frase_ru":"Мама волнуется.","frase_en":"Mom worries."},
    {"inf":"смеяться","trans":"to laugh","conj":{"я":"смеюсь","ты":"смеёшься","он/она":"смеётся","мы":"смеёмся","вы":"смеётесь","они":"смеются"},"frase_ru":"Дети смеются.","frase_en":"The children laugh."},
    {"inf":"плакать","trans":"to cry","conj":{"я":"плачу","ты":"плачешь","он/она":"плачет","мы":"плачем","вы":"плачете","они":"плачут"},"frase_ru":"Она плачет.","frase_en":"She cries."},
    {"inf":"улыбаться","trans":"to smile","conj":{"я":"улыбаюсь","ты":"улыбаешься","он/она":"улыбается","мы":"улыбаемся","вы":"улыбаетесь","они":"улыбаются"},"frase_ru":"Он улыбается.","frase_en":"He smiles."},
    {"inf":"кричать","trans":"to shout","conj":{"я":"кричу","ты":"кричишь","он/она":"кричит","мы":"кричим","вы":"кричите","они":"кричат"},"frase_ru":"Он кричит громко.","frase_en":"He shouts loudly."},
    {"inf":"молчать","trans":"to be silent","conj":{"я":"молчу","ты":"молчишь","он/она":"молчит","мы":"молчим","вы":"молчите","они":"молчат"},"frase_ru":"Она молчит.","frase_en":"She is silent."},
    {"inf":"звать","trans":"to call (by name)","conj":{"я":"зову","ты":"зовёшь","он/она":"зовёт","мы":"зовём","вы":"зовёте","они":"зовут"},"frase_ru":"Меня зовут Анна.","frase_en":"My name is Anna."},
    {"inf":"называть","trans":"to name / to call","conj":{"я":"называю","ты":"называешь","он/она":"называет","мы":"называем","вы":"называете","они":"называют"},"frase_ru":"Он называет город.","frase_en":"He names the city."},
    {"inf":"строить","trans":"to build","conj":{"я":"строю","ты":"строишь","он/она":"строит","мы":"строим","вы":"строите","они":"строят"},"frase_ru":"Они строят дом.","frase_en":"They are building a house."},
    {"inf":"ломать","trans":"to break","conj":{"я":"ломаю","ты":"ломаешь","он/она":"ломает","мы":"ломаем","вы":"ломаете","они":"ломают"},"frase_ru":"Он ломает игрушку.","frase_en":"He breaks a toy."},
    {"inf":"рисовать","trans":"to draw","conj":{"я":"рисую","ты":"рисуешь","он/она":"рисует","мы":"рисуем","вы":"рисуете","они":"рисуют"},"frase_ru":"Я рисую кошку.","frase_en":"I draw a cat."},
    {"inf":"фотографировать","trans":"to photograph","conj":{"я":"фотографирую","ты":"фотографируешь","он/она":"фотографирует","мы":"фотографируем","вы":"фотографируете","они":"фотографируют"},"frase_ru":"Я фотографирую город.","frase_en":"I photograph the city."},
    {"inf":"считать","trans":"to count","conj":{"я":"считаю","ты":"считаешь","он/она":"считает","мы":"считаем","вы":"считаете","они":"считают"},"frase_ru":"Я считаю до десяти.","frase_en":"I count to ten."},
    {"inf":"измерять","trans":"to measure","conj":{"я":"измеряю","ты":"измеряешь","он/она":"измеряет","мы":"измеряем","вы":"измеряете","они":"измеряют"},"frase_ru":"Он измеряет длину.","frase_en":"He measures the length."},
    {"inf":"завтракать","trans":"to have breakfast","conj":{"я":"завтракаю","ты":"завтракаешь","он/она":"завтракает","мы":"завтракаем","вы":"завтракаете","они":"завтракают"},"frase_ru":"Я завтракаю утром.","frase_en":"I have breakfast in the morning."},
    {"inf":"обедать","trans":"to have lunch","conj":{"я":"обедаю","ты":"обедаешь","он/она":"обедает","мы":"обедаем","вы":"обедаете","они":"обедают"},"frase_ru":"Мы обедаем в час.","frase_en":"We have lunch at one."},
    {"inf":"ужинать","trans":"to have dinner","conj":{"я":"ужинаю","ты":"ужинаешь","он/она":"ужинает","мы":"ужинаем","вы":"ужинаете","они":"ужинают"},"frase_ru":"Они ужинают вечером.","frase_en":"They have dinner in the evening."},
    {"inf":"просыпаться","trans":"to wake up","conj":{"я":"просыпаюсь","ты":"просыпаешься","он/она":"просыпается","мы":"просыпаемся","вы":"просыпаетесь","они":"просыпаются"},"frase_ru":"Я просыпаюсь рано.","frase_en":"I wake up early."},
    {"inf":"вставать","trans":"to get up","conj":{"я":"встаю","ты":"встаёшь","он/она":"встаёт","мы":"встаём","вы":"встаёте","они":"встают"},"frase_ru":"Я встаю в семь.","frase_en":"I get up at seven."},
    {"inf":"ложиться","trans":"to lie down / to go to bed","conj":{"я":"ложусь","ты":"ложишься","он/она":"ложится","мы":"ложимся","вы":"ложитесь","они":"ложатся"},"frase_ru":"Я ложусь спать.","frase_en":"I go to bed."},
    {"inf":"одеваться","trans":"to get dressed","conj":{"я":"одеваюсь","ты":"одеваешься","он/она":"одевается","мы":"одеваемся","вы":"одеваетесь","они":"одеваются"},"frase_ru":"Я одеваюсь быстро.","frase_en":"I get dressed quickly."},
    {"inf":"раздеваться","trans":"to undress","conj":{"я":"раздеваюсь","ты":"раздеваешься","он/она":"раздевается","мы":"раздеваемся","вы":"раздеваетесь","они":"раздеваются"},"frase_ru":"Он раздевается дома.","frase_en":"He undresses at home."},
    {"inf":"мыться","trans":"to wash oneself","conj":{"я":"моюсь","ты":"моешься","он/она":"моется","мы":"моемся","вы":"моетесь","они":"моются"},"frase_ru":"Я моюсь утром.","frase_en":"I wash myself in the morning."},
    {"inf":"причёсываться","trans":"to comb one's hair","conj":{"я":"причёсываюсь","ты":"причёсываешься","он/она":"причёсывается","мы":"причёсываемся","вы":"причёсываетесь","они":"причёсываются"},"frase_ru":"Она причёсывается.","frase_en":"She combs her hair."},
    {"inf":"убирать","trans":"to clean up","conj":{"я":"убираю","ты":"убираешь","он/она":"убирает","мы":"убираем","вы":"убираете","они":"убирают"},"frase_ru":"Я убираю комнату.","frase_en":"I clean the room."},
    {"inf":"петь","trans":"to sing","conj":{"я":"пою","ты":"поёшь","он/она":"поёт","мы":"поём","вы":"поёте","они":"поют"},"frase_ru":"Мы поём песню.","frase_en":"We sing a song."},
    {"inf":"слушать","trans":"to listen","conj":{"я":"слушаю","ты":"слушаешь","он/она":"слушает","мы":"слушаем","вы":"слушаете","они":"слушают"},"frase_ru":"Я слушаю музыку.","frase_en":"I listen to music."},
    {"inf":"смеяться","trans":"to laugh","conj":{"я":"смеюсь","ты":"смеёшься","он/она":"смеётся","мы":"смеёмся","вы":"смеётесь","они":"смеются"},"frase_ru":"Мы смеёмся вместе.","frase_en":"We laugh together."},
]

# ----------------------------------------------------------------------
# GENANKI MODEL
# ----------------------------------------------------------------------
MODEL_ID = 1607392319
DECK_ID = 2059400110

model = genanki.Model(
    MODEL_ID,
    'Russian Verb with Audio',
    fields=[
        {'name': 'Infinitive'},
        {'name': 'Translation'},
        {'name': 'Conjugations'},
        {'name': 'ExampleRU'},
        {'name': 'ExampleEN'},
        {'name': 'AudioInfinitive'},
        {'name': 'AudioConj1'},
        {'name': 'AudioConj2'},
        {'name': 'AudioConj3'},
        {'name': 'AudioConj4'},
        {'name': 'AudioConj5'},
        {'name': 'AudioConj6'},
        {'name': 'AudioExample'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '''
                <div style="font-family: Arial; text-align: center;">
                    <h2>{{Infinitive}}</h2>
                    <p><i>{{Translation}}</i></p>
                    {{AudioInfinitive}}
                </div>
            ''',
            'afmt': '''
                <div style="font-family: Arial; text-align: left;">
                    <h2>{{Infinitive}} – {{Translation}}</h2>
                    <hr>
                    <h3>Present tense</h3>
                    <table style="width:100%; border-collapse: collapse;">
                        <tr><td><b>I</b></td><td>{{Conjugations}}</td></tr>
                        <tr><td><b>you (sg)</b></td><td>{{AudioConj1}}</td></tr>
                        <tr><td><b>he / she</b></td><td>{{AudioConj2}}</td></tr>
                        <tr><td><b>we</b></td><td>{{AudioConj3}}</td></tr>
                        <tr><td><b>you (pl)</b></td><td>{{AudioConj4}}</td></tr>
                        <tr><td><b>they</b></td><td>{{AudioConj5}}</td></tr>
                    </table>
                    <hr>
                    <h3>Example sentence</h3>
                    <p><b>RU:</b> {{ExampleRU}} {{AudioExample}}</p>
                    <p><b>EN:</b> {{ExampleEN}}</p>
                </div>
            '''
        }
    ]
)

# ----------------------------------------------------------------------
# AUDIO HELPERS
# ----------------------------------------------------------------------
async def generate_audio(text: str, path: Path) -> None:
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(str(path))

# ----------------------------------------------------------------------
# DECK BUILDER
# ----------------------------------------------------------------------
async def main():
    deck = genanki.Deck(DECK_ID, DECK_NAME)
    media_files = []

    for idx, verb in enumerate(VERBOS):
        print(f"Processing {idx+1}/{len(VERBOS)}: {verb['inf']}")

        # Infinitive audio
        inf_audio = TEMP_DIR / f"inf_{idx}.mp3"
        await generate_audio(verb["inf"], inf_audio)
        media_files.append(str(inf_audio))

        # Conjugation audios (pronouns in Russian for natural pronunciation)
        conj_texts = [
            f"я {verb['conj']['я']}",
            f"ты {verb['conj']['ты']}",
            f"он {verb['conj']['он/она']}",
            f"мы {verb['conj']['мы']}",
            f"вы {verb['conj']['вы']}",
            f"они {verb['conj']['они']}",
        ]
        conj_audios = []
        for j, txt in enumerate(conj_texts):
            p = TEMP_DIR / f"conj_{idx}_{j}.mp3"
            await generate_audio(txt, p)
            media_files.append(str(p))
            conj_audios.append(p)

        # Example sentence audio
        ex_audio = TEMP_DIR / f"ex_{idx}.mp3"
        await generate_audio(verb["frase_ru"], ex_audio)
        media_files.append(str(ex_audio))

        # Build conjugation display string
        conj_display = (
            f"I: {verb['conj']['я']} &nbsp;|&nbsp; "
            f"you: {verb['conj']['ты']} &nbsp;|&nbsp; "
            f"he/she: {verb['conj']['он/она']} &nbsp;|&nbsp; "
            f"we: {verb['conj']['мы']} &nbsp;|&nbsp; "
            f"you (pl): {verb['conj']['вы']} &nbsp;|&nbsp; "
            f"they: {verb['conj']['они']}"
        )

        note = genanki.Note(
            model=model,
            fields=[
                verb["inf"],
                verb["trans"],
                conj_display,
                verb["frase_ru"],
                verb["frase_en"],
                f"[sound:{inf_audio.name}]",
                f"[sound:{conj_audios[0].name}]",
                f"[sound:{conj_audios[1].name}]",
                f"[sound:{conj_audios[2].name}]",
                f"[sound:{conj_audios[3].name}]",
                f"[sound:{conj_audios[4].name}]",
                f"[sound:{conj_audios[5].name}]",
                f"[sound:{ex_audio.name}]",
            ]
        )
        deck.add_note(note)

    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(OUTPUT_FILE)
    print(f"\nDeck created: {OUTPUT_FILE}")
    print(f"Cards: {len(deck.notes)}")
    print(f"Audio files: {len(media_files)}")

if __name__ == "__main__":
    asyncio.run(main())