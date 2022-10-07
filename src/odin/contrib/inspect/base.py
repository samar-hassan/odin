from humanfriendly.terminal import ansi_wrap, HIGHLIGHT_COLOR

from odin.utils import getmeta


def resource_reference(resource):
    return (
        f"{getmeta(resource).resource_name} <{resource.__module__}.{resource.__name__}>"
    )


class SummaryBase:
    """
    Base class for summaries
    """

    def __init__(self, out):
        self.out = out

    def print(self, objects, sep=" ", end="\n"):
        print(*objects, sep=sep, end=end, file=self.out)

    def title(self, value, underline="="):
        self.print(
            [
                ansi_wrap(value, bold=True, color=HIGHLIGHT_COLOR),
                underline * len(value),
            ],
            sep="\n",
        )
