

class Stream:

    # noinspection PyMethodMayBeStatic
    def input(self) -> str:
        return input("> ")

    # noinspection PyMethodMayBeStatic
    def output(self, text: str) -> None:
        print(text)

    # noinspection PyMethodMayBeStatic
    def output_renewable_line(self, text: str) -> None:
        print("\r" + text, end="")

    # noinspection PyMethodMayBeStatic
    def output_renewable_line_end(self, text: str, *, new_line: bool = False) -> None:
        start = "\n" if new_line else "\r"
        print(start + text)
