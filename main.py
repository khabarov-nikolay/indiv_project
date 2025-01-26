import pygame
pygame.init()
import pathlib
import random
from string import ascii_lowercase
try:
    import toml
except ModuleNotFoundError:
    import tomli as toml

objects = []




class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunctions=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunctions = onclickFunctions
        self.onPress = False
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


        self.buttonSurface.blit(self.buttonSurf, [self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2, self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2])
        canvas.blit(self.buttonSurface, self.buttonRect)

def testFunctions():
    print('test')




def end():
    pygame.quit()


#play_button = Button(500, 500, 200, 100, 'Button', testFunctions)

button_start = Button(100, 100, 200, 100, 'START', testFunctions)
button_end = Button(500, 500, 200, 100, 'EXIT', end)











'''
NUM_QUESTIONS_PER_QUIZ = 5
QUESTIONS_PATH = pathlib.Path(__file__).parent / "questions5.toml"

def run_quiz():
    questions = prepare_questions(
        QUESTIONS_PATH, num_questions=NUM_QUESTIONS_PER_QUIZ
    )

    num_correct = 0
    for num, question in enumerate(questions, start=1):
        print(f"\nQuestion {num}:")
        num_correct += ask_question(question)

    print(f"\nYou got {num_correct} correct out of {num} questions")

def prepare_questions(path, num_questions):
    questions = toml.loads(path.read_text())["questions"]
    num_questions = min(num_questions, len(questions))
    return random.sample(questions, k=num_questions)

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

        return [labeled_alternatives[answer] for answer in answers]

if __name__ == "__main__":
    run_quiz()
'''












canvas = pygame.display.set_mode((1000, 900))
pygame.display.set_caption('My quiz!')


font = pygame.font.SysFont('Comic Sans MS', 100)
main_title = font.render('Grand quiz', False, (0, 0, 0))




exit = False
while not exit:


    canvas.fill((0, 0, 255))



    canvas.blit(main_title, (250, 20))




    for object in objects:
        object.update()

    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
            pygame.quit()





























