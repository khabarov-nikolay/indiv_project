
# импортируем библиотеки
import pygame
pygame.init()
import pathlib
import random

import toml

# создаем переменные, необходимые для работы
NUM_QUESTIONS_PER_QUIZ = 10
QUESTIONS_PATH = pathlib.Path(__file__).parent / "questions5.toml"   # сохраняем местоположения файла с вопросами
objects = []
questions = []
question_count = 0
question_answered = False
correct_count = 0
is_game_finished = False



# создаем класс обьектов для создания кнопок
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunctions=None, is_answer = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.show_color = False
        self.onclickFunctions = onclickFunctions
        self.onPress = False
        self.is_answer = is_answer
        self.fillColors = {'normal': '#ffffff', 'hover': '#666666', 'pressed': '#333333'}

        font = pygame.font.SysFont('Times New Roman', 30)
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        objects.append(self)


# создание функции для активации кнопок
    def update(self):


        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if not self.onPress:
                    self.onclickFunctions()
                    self.onPress = True
            else:
                self.onPress = False

        if self.show_color:
            if self.is_answer:
                self.buttonSurface.fill('#00ff00')
            elif self.is_answer != None:
                self.buttonSurface.fill('#ff0000')

        self.buttonSurface.blit(self.buttonSurf, [self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2, self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2])
        canvas.blit(self.buttonSurface, self.buttonRect)
# создание функции, которая позволяет перейти к следующему вопросу
def next_question():
    global is_game_finished
    global question_answered
    global question_count
    if question_answered and question_count < NUM_QUESTIONS_PER_QUIZ - 1:
        question_count += 1
        start_game()
        question_answered = False
    elif question_answered and question_count >= NUM_QUESTIONS_PER_QUIZ - 1:
        is_game_finished = True
# создание функции, которая окрашивает кнопку с правильным ответом зеленым цветом
def correct():
    global correct_count
    correct_count += 1
    global question_answered
    question_answered = True
    for i in objects:
        i.show_color = True
# создание функции, которая окрашивает кнопку с правильным ответом красным цветом
def wrong():
    global question_answered
    question_answered = True
    for i in objects:
        i.show_color = True
# создание функции, которая позволяет переносить текст вопроса, если он не помещается в окно приложения
def blit_text(surface, text, pos, font, color=(0, 0, 0)):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = 1000, 900                     #surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

# создание функции, которая подгружает текст вопроса из файла с вопросами
def prepare_questions(path, num_questions):
    io = open(path, 'r', encoding='utf-8')
    text = io.read()
    io.close()
    questions = toml.loads(text)['questions']
    num_questions = min(num_questions, len(questions))

    return random.sample(questions, k=num_questions)
# создание кнопки, которая
def start_game():
    objects.clear()

    if question_count == 0:
        questions.clear()
        questions.append(prepare_questions(QUESTIONS_PATH, num_questions=NUM_QUESTIONS_PER_QUIZ))

    answ_text = questions[0][question_count]['answers'][0]
    possition_offsets = [[0, 0], [350, 0], [0, 150], [350, 150]]
    index = random.randint(0, len(possition_offsets) - 1)
    answ_button = Button(50 + possition_offsets[index][0], 600 + possition_offsets[index][1], 320, 100, answ_text, correct, True)
    possition_offsets.remove(possition_offsets[index])

    for i, alt in enumerate(questions[0][question_count]['alternatives']):
        answ_text = questions[0][question_count]['alternatives'][i]
        index = random.randint(0, len(possition_offsets) - 1)
        butt = Button(50 + possition_offsets[index][0], 600 + possition_offsets[index][1], 320, 100, answ_text, wrong)
        possition_offsets.remove(possition_offsets[index])

    # создание кнопки "Далее"
    next_button = Button(800, 770, 120, 100, "ДАЛЕЕ", next_question, None)
# создание функции, которая позволяет перейти в меню
def reset():
    global is_game_finished
    is_game_finished = False
    global objects
    objects.clear()
    global questions
    questions.clear()
    global question_count
    question_count = 0
    global question_answered
    question_answered = False
    global correct_count
    correct_count = 0



    button_start = Button((1000 - 250)//2, 300, 250, 120, 'НАЧАТЬ', start_game)
    button_end = Button((1000 - 250)//2, 450, 250, 120, 'ВЫХОД', end_game)

# создание функции, которая позволяет окончить игру
def end_game():
    exit()
# создание кнопок "Старт" и "Выход"
button_start = Button((1000 - 250)//2, 300, 250, 120, 'НАЧАТЬ', start_game)
button_end = Button((1000 - 250)//2, 450, 250, 120, 'ВЫХОД', end_game)
# запуск основного кода программы
if __name__ == "__main__":
    question_text = ""
    canvas = pygame.display.set_mode((1000, 900))
    pygame.display.set_caption('My quiz!')

    # создание заставки
    zastavka = pygame.image.load('images/111.jpg')
    zastavka = pygame.transform.scale(zastavka, (1000, 900))

#Comic Sans MS

    font = pygame.font.SysFont('Times New Roman', 100)
    question_font = pygame.font.SysFont('Times New Roman', 45)
    main_title = font.render('ВИКТОРИНА', False, (0, 0, 0))
    alpha = 0

    while alpha <= 200:
        pygame.display.update()
        canvas.fill('#ffffff')
        canvas.blit(zastavka, (0, 0))
        zastavka.set_alpha(alpha)
        alpha += 1
        pygame.time.wait(11)
        if alpha == 200:
            pygame.time.wait(1500)






    # создание основного игрового цикла
    while True:
        pygame.display.update()

        canvas.fill('#0d7fbf')

        if len(questions) == 0:
            canvas.blit(main_title, (205, 30))
        elif not is_game_finished:
            # подгрузка и вывод на экран фото и текста для вопроса
            name_foto = questions[0][question_count]['foto'][0]
            foto = pygame.image.load(f'images/{name_foto}')
            foto = pygame.transform.scale(foto, (questions[0][question_count]['xy'][0], questions[0][question_count]['xy'][1]))
            canvas.blit(foto, ((1000-questions[0][question_count]['xy'][0]) // 2, 0))

            question_text = questions[0][question_count]['question']

            question = question_font.render(question_text.encode('utf-8'), False, (225, 225, 225))

            blit_text(canvas, question_text, (20, 400), question_font)
        elif is_game_finished:
            # финальное окно
            objects.clear()
            home_button = Button(400, 710, 200, 100, 'МЕНЮ', reset)
            font = pygame.font.SysFont('Times New Roman', 60)
            end_title = font.render('Поздравляем, вы прошли викторину!', False, (0, 0, 0))
            score = font.render(f'Правильных ответов: {correct_count}', False, (0, 0, 0))
            # вывод медалей
            medal = None

            if correct_count <= 3:
                medal = pygame.image.load("images/three.png")
                medal = pygame.transform.scale(medal, (550, 500))
                canvas.blit(medal, (220, 270))

            elif 3 < correct_count <= 7:
                medal = pygame.image.load("images/two.png")
                medal = pygame.transform.scale(medal, (350, 430))
                canvas.blit(medal, (325, 270))
            else:

                medal = pygame.image.load("images/one.png")
                medal = pygame.transform.scale(medal, (550, 550))
                canvas.blit(medal, ((1000-550)//2, 220))

            canvas.blit(end_title, (20, 20))
            canvas.blit(score, (20, 200))




        # рендеринг (отрисовка) всез обьектов на экране
        for object in objects:
            object.update()
        # выход из программы
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()



