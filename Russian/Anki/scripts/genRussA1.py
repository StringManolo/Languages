#!/bin/env python3

import asyncio
import hashlib
import os
import re
from pathlib import Path

import edge_tts
import genanki

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------
VOICE = "ru-RU-SvetlanaNeural"   # o "ru-RU-DmitryNeural"
RATE  = "-10%"                    # un poco más lento para A1
MEDIA_DIR = Path("media_ru")
MEDIA_DIR.mkdir(exist_ok=True)

MODEL_ID = 1607392319
DECK_ID  = 2059400110

# ------------------------------------------------------------------
# MODELO
# ------------------------------------------------------------------
model = genanki.Model(
    MODEL_ID,
    'RussianA1 Model (audio)',
    fields=[
        {'name': 'Russian'},
        {'name': 'English'},
        {'name': 'Audio'},
        {'name': 'Kind'},
    ],
    templates=[{
        'name': 'Recognition',
        'qfmt': '{{Audio}}<br><br>'
                '<div style="font-size:30px;">{{Russian}}</div>',
        'afmt': '{{Audio}}<br><br>'
                '<div style="font-size:30px;">{{Russian}}</div>'
                '<hr id=answer>'
                '<div style="font-size:22px;">{{English}}</div>'
                '<br><small style="color:gray;">{{Kind}}</small>',
    }],
    css='''
    .card {
        font-family: Arial, sans-serif;
        text-align: center;
        background: #fff;
        color: #222;
        padding: 20px;
    }
    ''',
)

deck = genanki.Deck(DECK_ID, 'RussianA1')

# ------------------------------------------------------------------
# DATOS (idénticos a tu versión anterior)
# ------------------------------------------------------------------
SENTENCES_RAW = """
Здравствуйте!|Hello!
Привет!|Hi!
Спасибо!|Thank you!
Пожалуйста.|Please / You're welcome.
Да.|Yes.
Нет.|No.
Извините.|Excuse me / Sorry.
Простите.|Sorry / Excuse me.
Как дела?|How are you?
Хорошо.|Good / Okay.
Плохо.|Bad.
Как вы?|How are you? (formal)
Что это?|What is this?
Кто это?|Who is this?
Где туалет?|Where is the toilet?
Сколько это стоит?|How much does this cost?
Я не понимаю.|I don't understand.
Я не знаю.|I don't know.
Вы говорите по-английски?|Do you speak English?
Я не говорю по-русски.|I don't speak Russian.
Повторите, пожалуйста.|Repeat, please.
Говорите медленнее, пожалуйста.|Speak slower, please.
Помогите, пожалуйста.|Help, please.
Можно?|May I?
Можно мне...?|May I have...?
Я хочу...|I want...
Мне нужно...|I need...
У меня есть...|I have...
У меня нет...|I don't have...
Я не могу.|I can't.
Я могу.|I can.
Конечно.|Of course.
Может быть.|Maybe.
Я согласен / Я согласна.|I agree. (m/f)
Я не согласен / Я не согласна.|I disagree. (m/f)
Не за что.|You're welcome.
Ничего страшного.|It's okay / No problem.
До свидания!|Goodbye!
Пока!|Bye!
Доброе утро!|Good morning!
Добрый день!|Good afternoon!
Добрый вечер!|Good evening!
Спокойной ночи!|Good night!
Как вас зовут?|What is your name?
Меня зовут...|My name is...
Очень приятно.|Nice to meet you.
Откуда вы?|Where are you from?
Я из...|I am from...
Сколько вам лет?|How old are you?
Мне ... лет.|I am ... years old.
Где вы живёте?|Where do you live?
Я живу в...|I live in...
Я работаю...|I work...
Я учусь...|I study...
Что вы делаете?|What are you doing?
Как это сказать по-русски?|How do you say this in Russian?
Что это значит?|What does this mean?
Я забыл / Я забыла.|I forgot. (m/f)
Я помню.|I remember.
Подождите, пожалуйста.|Wait, please.
Сейчас.|Now / Just a moment.
Сегодня.|Today.
Завтра.|Tomorrow.
Вчера.|Yesterday.
Который час?|What time is it?
Во сколько?|At what time?
Здесь.|Here.
Там.|There.
Слева.|On the left.
Справа.|On the right.
Прямо.|Straight ahead.
Остановите здесь, пожалуйста.|Stop here, please.
Где находится...?|Where is...?
Как добраться до...?|How do I get to...?
Я заблудился / Я заблудилась.|I'm lost. (m/f)
Это далеко?|Is it far?
Это близко?|Is it close?
Я голоден / Я голодна.|I'm hungry. (m/f)
Я хочу пить.|I'm thirsty.
Я устал / Я устала.|I'm tired. (m/f)
Мне плохо.|I feel bad.
Мне холодно.|I'm cold.
Мне жарко.|I'm hot.
Удачи!|Good luck!
С днём рождения!|Happy birthday!
С Новым годом!|Happy New Year!
Поздравляю!|Congratulations!
Добро пожаловать!|Welcome!
Приятного аппетита!|Bon appetit!
Будьте здоровы!|Bless you / Get well!
Я тебя люблю.|I love you.
Мне нравится...|I like...
Мне не нравится...|I don't like...
Это очень вкусно.|It's very tasty.
Дайте мне, пожалуйста...|Give me, please...
Счёт, пожалуйста.|The bill, please.
Я оплачу картой.|I'll pay by card.
У вас есть...?|Do you have...?
Можно вопрос?|May I ask a question?
Всё хорошо.|Everything is fine.
Я не говорю по-русски хорошо.|I don't speak Russian well.
Я немного говорю по-русски.|I speak a little Russian.
Я изучаю русский язык.|I am studying Russian.
Как по-русски ...?|How do you say ... in Russian?
Что вы имеете в виду?|What do you mean?
Я не уверен / Я не уверена.|I'm not sure. (m/f)
Я думаю, что...|I think that...
Мне кажется...|It seems to me...
Я знаю.|I know.
Я не помню.|I don't remember.
Напомните мне, пожалуйста.|Remind me, please.
Не могли бы вы мне помочь?|Could you help me?
Мне нужна помощь.|I need help.
Вызовите врача!|Call a doctor!
Скорая помощь.|Ambulance.
Я плохо себя чувствую.|I feel unwell.
У меня болит голова.|I have a headache.
У меня болит живот.|I have a stomachache.
У меня температура.|I have a fever.
Я простудился / Я простудилась.|I caught a cold. (m/f)
У меня аллергия.|I have an allergy.
Мне нужна аптека.|I need a pharmacy.
Где ближайшая аптека?|Where is the nearest pharmacy?
Где ближайшая больница?|Where is the nearest hospital?
Вызовите полицию!|Call the police!
Я потерял паспорт.|I lost my passport.
Я потерял кошелёк.|I lost my wallet.
Меня обокрали.|I've been robbed.
Это опасно?|Is it dangerous?
Я хочу домой.|I want to go home.
Я хочу спать.|I'm sleepy.
Я хочу есть.|I'm hungry.
Дайте мне меню, пожалуйста.|Give me the menu, please.
Что вы посоветуете?|What do you recommend?
Я буду это.|I'll have this.
Я не ем мясо.|I don't eat meat.
Я вегетарианец / Я вегетарианка.|I'm vegetarian. (m/f)
У меня нет аппетита.|I have no appetite.
Это острое?|Is it spicy?
Это сладкое?|Is it sweet?
Это солёное?|Is it salty?
Я плачу.|I'm paying.
Я не буду платить.|I won't pay.
Сколько с меня?|How much do I owe?
Где можно купить...?|Where can I buy...?
У вас есть это в другом размере?|Do you have this in another size?
У вас есть это другого цвета?|Do you have this in another color?
Можно примерить?|Can I try it on?
Это слишком дорого.|It's too expensive.
Есть скидка?|Is there a discount?
Я просто смотрю.|I'm just looking.
Я беру это.|I'll take it.
Заверните, пожалуйста.|Wrap it, please.
Можно пакет?|Can I have a bag?
Где касса?|Where is the checkout?
Я ищу...|I'm looking for...
Вы можете мне показать?|Can you show me?
Как это работает?|How does it work?
Это не работает.|It doesn't work.
Сломано.|It's broken.
У меня не работает интернет.|My internet doesn't work.
Где здесь Wi-Fi?|Where is Wi-Fi here?
Какой пароль от Wi-Fi?|What's the Wi-Fi password?
Мне нужно зарядить телефон.|I need to charge my phone.
Где можно зарядить телефон?|Where can I charge my phone?
Я опаздываю.|I'm late.
Я спешу.|I'm in a hurry.
Не спешите.|Don't hurry.
Подождите минуту.|Wait a minute.
Я скоро вернусь.|I'll be back soon.
Я вернусь позже.|I'll come back later.
Увидимся позже.|See you later.
До завтра.|See you tomorrow.
До вечера.|See you in the evening.
Хорошего дня!|Have a nice day!
Хороших выходных!|Have a nice weekend!
Всего хорошего!|All the best!
Берегите себя.|Take care.
Не волнуйтесь.|Don't worry.
Всё будет хорошо.|Everything will be fine.
Я волнуюсь.|I'm worried.
Я счастлив / Я счастлива.|I'm happy. (m/f)
Мне грустно.|I'm sad.
Мне скучно.|I'm bored.
Мне интересно.|I'm interested.
Это интересно.|It's interesting.
Это скучно.|It's boring.
Это важно.|It's important.
Это не важно.|It's not important.
Это правда.|It's true.
Это неправда.|It's not true.
Я не верю.|I don't believe it.
Я верю тебе.|I believe you.
Ты уверен? / Вы уверены?|Are you sure?
Я уверен / Я уверена.|I'm sure. (m/f)
Я не знаю наверняка.|I don't know for sure.
Что случилось?|What happened?
Ничего.|Nothing.
Всё нормально.|Everything's fine.
Пока всё.|That's all for now.
"""

WORDS_RAW = """
и|and
в|in
не|not
на|on / at
я|I
быть|to be
он|he
с|with
что|what / that
а|and / but
по|by / along
это|this / it is
она|she
этот|this
к|to / toward
но|but
они|they
мы|we
как|how / like
из|from / out of
у|at / by (have)
который|which / who
то|that
за|for / behind
свой|one's own
весь|all / whole
год|year
от|from
так|so / thus
о|about
для|for
ты|you (informal)
же|same / particle
все|everyone / all
тот|that one
мой|my
человек|person / human
нет|no / there isn't
да|yes
очень|very
мне|to me
тебя|you (acc./gen.)
нас|us
вас|you (pl./formal)
себя|oneself
чтобы|in order to
если|if
когда|when
где|where
почему|why
какой|what kind / which
кто|who
чей|whose
там|there
тут|here
здесь|here
сейчас|now
потом|then / later
тогда|then / at that time
всегда|always
никогда|never
можно|one may / it's possible
нельзя|one may not / forbidden
нужно|necessary / need
надо|need to
хотеть|to want
мочь|to be able to
говорить|to speak / say
знать|to know
думать|to think
видеть|to see
слышать|to hear
делать|to do / make
идти|to go (on foot)
ехать|to go (by vehicle)
дать|to give
взять|to take
стать|to become
жить|to live
работать|to work
учиться|to study
любить|to love
нравиться|to like
понимать|to understand
помнить|to remember
забыть|to forget
найти|to find
потерять|to lose
купить|to buy
продать|to sell
есть|to eat / there is
пить|to drink
спать|to sleep
читать|to read
писать|to write
смотреть|to watch / look
слушать|to listen
ждать|to wait
помогать|to help
спрашивать|to ask
меня|me
тебе|to you
нам|to us
вам|to you (pl./formal)
его|his / him
её|her / hers
их|their / them
твой|your (informal)
наш|our
ваш|your (pl./formal)
такой|such / so
каждый|each / every
любой|any
другой|other / another
самый|the most / very
всё|everything
никто|nobody
ничто|nothing
ничего|nothing
кто-то|someone
что-то|something
кто-нибудь|anyone / someone
что-нибудь|anything / something
некоторый|some / certain
многие|many
несколько|several
один|one
два|two
три|three
первый|first
второй|second
последний|last
новый|new
старый|old
хороший|good
плохой|bad
большой|big
маленький|small
молодой|young
русский|Russian
главный|main
разный|different
раз|time (occurrence)
дело|matter / business
время|time
день|day
жизнь|life
рука|hand / arm
работа|work / job
слово|word
место|place
вопрос|question
дом|house / home
сторона|side
лицо|face / person
друг|friend
ребёнок|child
мир|world / peace
случай|case / incident
голова|head
глаз|eye
страна|country
город|city
книга|book
женщина|woman
мужчина|man
мать|mother
отец|father
сын|son
дочь|daughter
семья|family
школа|school
университет|university
язык|language / tongue
история|history / story
музыка|music
фильм|film / movie
вода|water
хлеб|bread
чай|tea
кофе|coffee
еда|food
деньги|money
машина|car / machine
улица|street
дорога|road / way
ночь|night
утро|morning
вечер|evening
неделя|week
месяц|month
минута|minute
час|hour
телефон|telephone
друг друга|each other
поэтому|therefore
потому что|because
также|also
тоже|too / also
ещё|still / yet / more
без|without
до|until / before
после|after
между|between
через|through / in (time)
около|near / about
вокруг|around
против|against
среди|among
кроме|except
вместо|instead of
из-за|because of / from behind
под|under
над|above / over
перед|in front of / before
при|at / in the presence of
про|about
или|or
либо|or / either
ни|not even / neither
даже|even
только|only
уже|already
опять|again
снова|again
совсем|completely / at all
почти|almost
вообще|in general / at all
конечно|of course
наверное|probably
возможно|possibly
действительно|really / indeed
особенно|especially
обычно|usually
часто|often
редко|rarely
иногда|sometimes
теперь|now
раньше|earlier / before
позже|later
скоро|soon
давно|long ago
недавно|recently
сразу|at once / immediately
вместе|together
отдельно|separately
быстро|quickly
медленно|slowly
легко|easily
трудно|difficult / hard
тяжело|heavy / hard
просто|simply / just
сложно|complicated
важно|important
интересно|interesting
ясно|clear
понятно|understandable / clear
правильно|correctly / right
неправильно|incorrectly / wrong
хорошо|well / good
плохо|badly / bad
много|a lot / many
мало|few / little
больше|more / bigger
меньше|less / smaller
лучше|better
хуже|worse
достаточно|enough
слишком|too (much)
абсолютно|absolutely
полностью|completely
точно|exactly / precisely
именно|precisely / exactly
вроде|like / seemingly
кажется|it seems
значит|so / it means
например|for example
кстати|by the way
вообще-то|actually
на самом деле|in fact / actually
в общем|in general
так сказать|so to speak
во-первых|first of all
во-вторых|secondly
наконец|finally
однако|however
зато|but on the other hand
причём|and moreover
притом|besides / moreover
оттого|that's why
зачем|why / what for
почему-то|for some reason
как-то|somehow
где-то|somewhere
когда-то|once / at some time
куда|where to
откуда|from where
туда|there / that way
сюда|here / this way
отсюда|from here
сказать|to say
ответить|to answer
спросить|to ask
рассказывать|to tell / narrate
показать|to show
давать|to give
брать|to take
становиться|to become
оставаться|to remain / stay
начинать|to begin
начать|to begin (perf.)
кончать|to finish / end
закончить|to finish
продолжать|to continue
перестать|to stop (doing)
уметь|to know how to
казаться|to seem
значить|to mean
следовать|to follow
являться|to be (formal)
называться|to be called
входить|to enter
выходить|to exit / go out
приходить|to come
уходить|to leave
приезжать|to arrive
уезжать|to depart / leave
приносить|to bring
уносить|to carry away
класть|to put (lying)
ставить|to put (standing)
лежать|to lie
сидеть|to sit
стоять|to stand
вставать|to get up
садиться|to sit down
ложиться|to lie down
открывать|to open
закрывать|to close
включать|to turn on
выключать|to turn off
звонить|to call / ring
отвечать|to answer
повторять|to repeat
изменять|to change / alter
менять|to change / exchange
решать|to decide / solve
решить|to decide (perf.)
выбирать|to choose
выбрать|to choose (perf.)
пытаться|to try / attempt
пробовать|to try / taste
успеть|to manage (in time)
успевать|to have time
опаздывать|to be late
опоздать|to be late (perf.)
случаться|to happen
случиться|to happen (perf.)
происходить|to occur
произойти|to occur (perf.)
бывать|to visit / happen to be
умирать|to die
умереть|to die (perf.)
рождаться|to be born
родиться|to be born (perf.)
расти|to grow
вырасти|to grow up
учить|to teach / learn
изучать|to study
научить|to teach (perf.)
научиться|to learn
играть|to play
петь|to sing
танцевать|to dance
рисовать|to draw
готовить|to cook / prepare
кормить|to feed
мыть|to wash
стирать|to do laundry
убирать|to clean up
чистить|to clean / peel
одеваться|to get dressed
раздеваться|to undress
носить|to wear / carry
надевать|to put on
снимать|to take off
улыбаться|to smile
смеяться|to laugh
плакать|to cry
кричать|to shout
молчать|to be silent
шептать|to whisper
дышать|to breathe
чувствовать|to feel
болеть|to hurt / be sick
лечить|to treat / cure
отдыхать|to rest
уставать|to get tired
просыпаться|to wake up
мыться|to wash oneself
бежать|to run
лететь|to fly
плавать|to swim
ходить|to go (on foot, habitual)
ездить|to go (by vehicle, habitual)
водить|to drive / lead
держать|to hold
бросать|to throw
кидать|to throw / toss
ловить|to catch
искать|to search
находить|to find
терять|to lose
дарить|to give as a gift
получать|to receive
посылать|to send
отправлять|to send
приглашать|to invite
встречать|to meet / greet
встречаться|to meet (each other)
знакомиться|to get acquainted
просить|to ask / request
благодарить|to thank
извиняться|to apologize
поздравлять|to congratulate
желать|to wish
надеяться|to hope
верить|to believe
сомневаться|to doubt
радоваться|to rejoice
бояться|to be afraid
ненавидеть|to hate
скучать|to be bored / miss
удивляться|to be surprised
интересоваться|to be interested
заниматься|to be engaged in
увлекаться|to be fond of
гордиться|to be proud
стыдиться|to be ashamed
извинить|to excuse
прощать|to forgive
ругать|to scold
хвалить|to praise
спорить|to argue
соглашаться|to agree
отказываться|to refuse
разрешать|to allow
запрещать|to forbid
обещать|to promise
советовать|to advise
предупреждать|to warn
напоминать|to remind
забывать|to forget
вспоминать|to recall
узнавать|to recognize / find out
объяснять|to explain
переводить|to translate
стоить|to cost
платить|to pay
тратить|to spend
экономить|to save / economize
зарабатывать|to earn
путешествовать|to travel
гулять|to stroll / walk
выигрывать|to win
проигрывать|to lose (game)
соревноваться|to compete
выздоравливать|to recover
курить|to smoke
бриться|to shave
краситься|to put on makeup
причёсываться|to comb one's hair
стричься|to get a haircut
шить|to sew
вязать|to knit
строить|to build
ремонтировать|to repair
ломать|to break
чинить|to fix
фотографировать|to photograph
записывать|to record / write down
считать|to count / consider
мечтать|to dream
планировать|to plan
гладить|to iron
поить|to give water
одевать|to dress (someone)
обувать|to put shoes on
купать|to bathe
спасать|to save / rescue
мешать|to disturb / hinder
поддерживать|to support
критиковать|to criticize
наказывать|to punish
обожать|to adore
презирать|to despise
завидовать|to envy
ревновать|to be jealous
жалеть|to pity
сочувствовать|to sympathize
солнце|sun
луна|moon
небо|sky
земля|earth / land
море|sea
река|river
озеро|lake
лес|forest
гора|mountain
поле|field
цветок|flower
дерево|tree
трава|grass
лист|leaf / sheet
снег|snow
дождь|rain
ветер|wind
погода|weather
холод|cold
тепло|warmth
огонь|fire
свет|light
тень|shadow
звук|sound
голос|voice
шум|noise
тишина|silence
запах|smell
вкус|taste
цвет|color
форма|form / shape
размер|size
вес|weight
скорость|speed
расстояние|distance
высота|height
глубина|depth
ширина|width
длина|length
количество|quantity
качество|quality
цена|price
стоимость|cost / value
польза|benefit
вред|harm
причина|cause / reason
цель|goal / aim
результат|result
успех|success
ошибка|mistake
правило|rule
закон|law
право|right / law
свобода|freedom
обязанность|duty
ответственность|responsibility
возможность|opportunity / possibility
способность|ability
необходимость|necessity
желание|desire
чувство|feeling
мысль|thought
идея|idea
память|memory
воображение|imagination
внимание|attention
сознание|consciousness
характер|character
поведение|behavior
отношение|attitude / relationship
общение|communication
дружба|friendship
любовь|love
ненависть|hatred
радость|joy
грусть|sadness
страх|fear
гнев|anger
удивление|surprise
интерес|interest
скука|boredom
надежда|hope
вера|faith
сомнение|doubt
правда|truth
ложь|lie
добро|good
зло|evil
красота|beauty
сила|strength
слабость|weakness
здоровье|health
болезнь|illness
судьба|fate
смерть|death
рождение|birth
детство|childhood
юность|youth
старость|old age
будущее|future
нога|leg / foot
палец|finger
ухо|ear
нос|nose
рот|mouth
зуб|tooth
волосы|hair
сердце|heart
спина|back
живот|stomach / belly
грудь|chest / breast
шея|neck
колено|knee
локоть|elbow
одежда|clothing
рубашка|shirt
брюки|trousers
платье|dress
юбка|skirt
куртка|jacket
пальто|coat
обувь|footwear
ботинки|boots / shoes
туфли|shoes
шапка|hat / cap
шарф|scarf
перчатки|gloves
мясо|meat
рыба|fish
овощ|vegetable
фрукт|fruit
яблоко|apple
банан|banana
апельсин|orange
картофель|potato
помидор|tomato
огурец|cucumber
сыр|cheese
молоко|milk
масло|butter / oil
сахар|sugar
соль|salt
суп|soup
каша|porridge
салат|salad
собака|dog
кошка|cat
птица|bird
лошадь|horse
корова|cow
свинья|pig
курица|chicken / hen
мышь|mouse
медведь|bear
волк|wolf
лиса|fox
заяц|hare / rabbit
компьютер|computer
интернет|internet
сайт|website
программа|program
кнопка|button
экран|screen
файл|file
письмо|letter
сообщение|message
врач|doctor
учитель|teacher
инженер|engineer
студент|student
продавец|seller
водитель|driver
полицейский|policeman
юрист|lawyer
экономист|economist
программист|programmer
автобус|bus
поезд|train
самолёт|airplane
корабль|ship
метро|metro / subway
такси|taxi
велосипед|bicycle
мотоцикл|motorcycle
магазин|shop
аптека|pharmacy
больница|hospital
ресторан|restaurant
кафе|cafe
банк|bank
почта|post office / mail
вокзал|railway station
аэропорт|airport
парк|park
музей|museum
театр|theater
кино|cinema
культура|culture
искусство|art
наука|science
понедельник|Monday
вторник|Tuesday
среда|Wednesday
четверг|Thursday
пятница|Friday
суббота|Saturday
воскресенье|Sunday
январь|January
февраль|February
март|March
апрель|April
май|May
июнь|June
июль|July
август|August
сентябрь|September
октябрь|October
ноябрь|November
декабрь|December
весна|spring
лето|summer
осень|autumn
зима|winter
ноль|zero
четыре|four
пять|five
шесть|six
семь|seven
восемь|eight
девять|nine
десять|ten
сто|hundred
тысяча|thousand
миллион|million
брат|brother
сестра|sister
дедушка|grandfather
бабушка|grandmother
дядя|uncle
тётя|aunt
муж|husband
жена|wife
подруга|(female) friend
сосед|neighbor
господин|mister / sir
госпожа|madam / Mrs.
имя|name
фамилия|surname
адрес|address
номер|number
ключ|key
дверь|door
окно|window
стол|table
стул|chair
кровать|bed
комната|room
кухня|kitchen
ванная|bathroom
туалет|toilet
пол|floor
потолок|ceiling
стена|wall
крыша|roof
лестница|stairs
лифт|elevator
этаж|floor / story
квартира|apartment
офис|office
завод|factory
ферма|farm
деревня|village
село|village / rural area
район|district
центр|center
площадь|square / area
мост|bridge
сад|garden
огород|vegetable garden
красный|red
синий|blue
зелёный|green
жёлтый|yellow
чёрный|black
белый|white
серый|gray
коричневый|brown
оранжевый|orange (color)
розовый|pink
фиолетовый|purple
голубой|light blue
золотой|golden
серебряный|silver
тёплый|warm
холодный|cold
горячий|hot
свежий|fresh
вкусный|tasty
сладкий|sweet
солёный|salty
"""

# ------------------------------------------------------------------
# AUDIO
# ------------------------------------------------------------------
def safe_filename(text: str) -> str:
    """Nombre corto y determinista basado en hash + sanitizado."""
    h = hashlib.md5(text.encode("utf-8")).hexdigest()[:10]
    clean = re.sub(r"[^\w\-]+", "_", text, flags=re.UNICODE)[:30]
    return f"ru_{clean}_{h}.mp3"

async def synth(text: str, path: Path):
    if path.exists() and path.stat().st_size > 0:
        return  # cache
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(str(path))

async def synth_all(items):
    sem = asyncio.Semaphore(8)  # 8 paralelas, evita rate-limit

    async def worker(text, path):
        async with sem:
            try:
                await synth(text, path)
            except Exception as e:
                print(f"⚠️  {text!r}: {e}")

    tasks = [worker(t, p) for t, p in items]
    await asyncio.gather(*tasks)

# ------------------------------------------------------------------
# CONSTRUCCIÓN
# ------------------------------------------------------------------
def parse(raw):
    for line in raw.strip().splitlines():
        if "|" in line:
            ru, en = line.split("|", 1)
            yield ru.strip(), en.strip()

sentence_pairs = list(parse(SENTENCES_RAW))
word_pairs     = list(parse(WORDS_RAW))

# 1) Preparar tareas de audio (con cache por si re-ejecutas)
audio_tasks = []
for ru, _ in sentence_pairs + word_pairs:
    fname = safe_filename(ru)
    audio_tasks.append((ru, MEDIA_DIR / fname))

print(f"🎙️  Generando {len(audio_tasks)} audios con {VOICE} ...")
asyncio.run(synth_all(audio_tasks))

# 2) Construir notas
media_files = []
for ru, en in sentence_pairs:
    fname = safe_filename(ru)
    media_files.append(str(MEDIA_DIR / fname))
    deck.add_note(genanki.Note(
        model=model,
        fields=[ru, en, f"[sound:{fname}]", "Sentence"],
        guid=genanki.guid_for("sent", ru),
        tags=["RussianA1", "sentence"],
    ))

for ru, en in word_pairs:
    fname = safe_filename(ru)
    media_files.append(str(MEDIA_DIR / fname))
    deck.add_note(genanki.Note(
        model=model,
        fields=[ru, en, f"[sound:{fname}]", "Word"],
        guid=genanki.guid_for("word", ru),
        tags=["RussianA1", "word"],
    ))

# 3) Empaquetar
pkg = genanki.Package(deck)
pkg.media_files = media_files
pkg.write_to_file("RussianA1.apkg")
print(f"✅ Listo -> RussianA1.apkg  ({len(deck.notes)} notas, "
      f"{len(set(media_files))} mp3)")
