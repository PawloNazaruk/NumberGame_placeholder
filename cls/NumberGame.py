from collections import namedtuple
from threading import Thread
from playsound import playsound
from pprint import pprint
import random
import time

import wave
import contextlib

# BEEP_PATH = 'KahnemanAddX\\media\\beep.wav'
BEEP_PATH = 'C:\\python\\projects\\KahnemanAddX\\media\\beep.wav'

# TODO split na metody
# TODO generator z kolekcji
# TODO BEEP_PATH it should works from relative path


class GameAddX:

    def __init__(self, length: str, amount: str, time_per_number: str, operation: str, digit_for_operation: str):
        self._number_length = int(length)
        self._numbers_amount = int(amount)
        self._time_per_number = int(time_per_number)
        self._math_operation = operation
        self._math_operation_sign = int(digit_for_operation)
        self._game_session = self.make_game_session()
        self._input = []

    def show_score(self):
        counter = 0
        for seq in self._game_session:
            if seq.answer_digits == seq.correct_digits:
                counter += 1

        score = float((counter / self._numbers_amount) * 100)
        print(score)

    def game(self):
        audio_channel = Thread(target=self.play_beep_loop)
        audio_channel.daemon = True
        audio_channel.start()

        for seq in self._game_session:
            """displaying digits for memorise"""
            for digit in seq.number_digits:
                print(time.perf_counter())
                print(digit)
                self.time_wait()

            """pause"""
            print(time.perf_counter())
            self.time_wait()

            """catching answers"""
            for i in range(self._number_length):
                print(time.perf_counter())
                get_input_thread = Thread(target=self.get_input)
                # Otherwise the thread won't be terminated when the main program terminates.
                get_input_thread.daemon = True
                get_input_thread.start()
                get_input_thread.join(timeout=self._time_per_number)

                if self._input:
                    seq.answer_digits.append(self._input[0])
                else:
                    seq.answer_digits.append('')
                self._input.clear()

        print(time.perf_counter())
        time_wait = self._number_length * self._numbers_amount * self._time_per_number
        audio_channel.join(timeout=time_wait)

    def get_input(self):
        print("Waiting for input: ...")
        while True:
            _input = input()
            self._input.append(_input)

    def time_wait(self) -> None:
        time.sleep(self._time_per_number)

    def make_game_session(self):
        Sequence = namedtuple("Sequence", [
            "number_digits",
            "correct_digits",
            "answer_digits",
        ])

        game_session = []
        for i in range(self._numbers_amount):

            number = self.generate_number_from_range()
            number_digits = self.divide_on_digits(number)
            correct_digits = self.calculate_correct_digits(number)
            answer_digits = []

            seq = Sequence(number_digits, correct_digits, answer_digits)
            game_session.append(seq)

        return game_session

    def generate_number_from_range(self) -> str:
        number_min = 10 ** (self._number_length - 1)
        number_max = int("".join(["9" for _ in range(self._number_length)]))
        return str(random.randint(number_min, number_max))

    def calculate_correct_digits(self, number: str) -> list:
        return {
            "+": [str(int(x) + self._math_operation_sign) for x in number],
            "-": [str(int(x) - self._math_operation_sign) for x in number],
            "*": [str(int(x) * self._math_operation_sign) for x in number],
            "/": [str(int(x) / self._math_operation_sign) for x in number],
        }.get(self._math_operation, "Incorrect operation")

    def play_beep_loop(self):
        with contextlib.closing(wave.open(BEEP_PATH, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            difference = self._time_per_number - duration
            while True:
                playsound(BEEP_PATH)
                time.sleep(difference)

    @staticmethod
    def divide_on_digits(number: str) -> list:
        return [x for x in number]

    @staticmethod
    def play_beep():
        playsound(BEEP_PATH)


# property na limity
default_kwargs = {
            "length": 2,
            "amount": 6,
            "time_per_number": 1,
            "operation": "+",
            "digit_for_operation": 1,
        }
asd = GameAddX(**default_kwargs)
asd.game()
asd.show_score()
