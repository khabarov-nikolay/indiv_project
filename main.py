import pygame
pygame.init()
import pathlib
import random
from string import ascii_lowercase
try:
    import toml
except ModuleNotFoundError:
    import tomli as toml

NUM_QUESTIONS_PER_QUIZ = 10
QUESTIONS_PATH = pathlib.Path(__file__).parent / "questions5.toml"
objects = []
questions = []
question_count = 0
question_answered = False
correct_count = 0
is_game_finished = False




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

        font = pygame.font.SysFont('Comic Sans MS', 30)
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        objects.append(self)



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

def correct():
    global correct_count
    correct_count += 1
    global question_answered
    question_answered = True
    for i in objects:
        i.show_color = True

def wrong():
    global question_answered
    question_answered = True
    for i in objects:
        i.show_color = True

def blit_text(surface, text, pos, font, color=pygame.Color('white')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
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

def prepare_questions(path, num_questions):
    io = open(path, 'r', encoding='utf-8')
    text = io.read()
    io.close()
    questions = toml.loads(text)['questions']
    num_questions = min(num_questions, len(questions))

    return random.sample(questions, k=num_questions)

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


    next_button = Button(800, 770, 100, 100, "Next", next_question, None)

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

    button_start = Button(400, 300, 200, 100, 'START', start_game)
    button_end = Button(400, 410, 200, 100, 'EXIT', end_game)


def end_game():
    exit()

button_start = Button(400, 300, 200, 100, 'START', start_game)
button_end = Button(400, 410, 200, 100, 'EXIT', end_game)

if __name__ == "__main__":
    question_text = ""
    canvas = pygame.display.set_mode((1000, 900))
    pygame.display.set_caption('My quiz!')


    font = pygame.font.SysFont('Comic Sans MS', 100)
    question_font = pygame.font.SysFont('Comic Sans MS', 20)
    main_title = font.render('Grand quiz', False, (0, 0, 0))

    while True:
        pygame.display.update()

        canvas.fill((0, 0, 255))

        if len(questions) == 0:
            canvas.blit(main_title, (250, 20))
        elif not is_game_finished:
            question_text = questions[0][question_count]['question']

            question = question_font.render(question_text.encode('utf-8'), False, (255, 255, 255))

            blit_text(canvas, question_text, (20, 500), question_font)
        elif is_game_finished:
            objects.clear()
            exit_button = Button(400, 510, 200, 100, 'EXIT', end_game)
            home_button = Button(400, 400, 200, 100, 'MENU', reset)
            font = pygame.font.SysFont('Comic Sans MS', 60)
            end_title = font.render('Поздравляем, вы прошли квиз!', False, (0, 0, 0))
            score = font.render(f'Правильных ответов: {correct_count}', False, (0, 0, 0))
            canvas.blit(end_title, (20, 20))
            canvas.blit(score, (20, 200))

        for object in objects:
            object.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
'''

def run_quiz():

    num_correct = 0
    for num, question in enumerate(questions, start=1):
        print(f"\nQuestion {num}:")
        num_correct += ask_question(question)

    print(f"\nYou got {num_correct} correct out of {num} questions")

def ask_question(question):
    correct_answers = question["answers"]
    alternatives = question["answers"] + question["alternatives"]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))

    answers = get_answers(
        question=question["question"],
        alternatives=ordered_alternatives,
        num_choices=len(correct_answers),
        hint=question.get("hint"),
    )
    if correct := (set(answers) == set(correct_answers)):
        print("⭐ Correct! ⭐")
    else:
        is_or_are = " is" if len(correct_answers) == 1 else "s are"
        print("\n- ".join([f"No, the answer{is_or_are}:"] + correct_answers))

    if "explanation" in question:
        print(f"\nEXPLANATION:\n{question['explanation']}")

    return 1 if correct else 0

def get_answers(question, alternatives, num_choices=1, hint=None):
    print(f"{question}?")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    if hint:
        labeled_alternatives["?"] = "Hint"

    for label, alternative in labeled_alternatives.items():
        print(f"  {label}) {alternative}")

    while True:
        plural_s = "" if num_choices == 1 else f"s (choose {num_choices})"
        answer = input(f"\nChoice{plural_s}? ")
        answers = set(answer.replace(",", " ").split())

        # Handle hints
        if hint and "?" in answers:
            print(f"\nHINT: {hint}")
            continue

        # Handle invalid answers
        if len(answers) != num_choices:
            plural_s = "" if num_choices == 1 else "s, separated by comma"
            print(f"Please answer {num_choices} alternative{plural_s}")
            continue

        if any(
            (invalid := answer) not in labeled_alternatives
            for answer in answers
        ):
            print(
                f"{invalid!r} is not a valid choice. "
                f"Please use {', '.join(labeled_alternatives)}"
            )
            continue

        return [labeled_alternatives[answer] for answer in answers
'''


