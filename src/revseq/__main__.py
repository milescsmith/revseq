from collections import deque
from importlib.metadata import version

import typer
from icontract import require
from rich import print
from typeguard import typechecked


def version_callback(value: bool) -> None:
    """Prints the version of the package."""
    if value:
        print(f"[red]{__package__}[/red] version: {version(__package__)}")
        raise typer.Exit()


app = typer.Typer(
    name="revseq",
    help="Generate reversed, reverse complement, and complement sequences",
    add_completion=False,
)


@app.command(no_args_is_help=True)
@require(
    lambda seq: len(set(seq) - set("AGCTagct")) == 0,
    error=lambda seq: ValueError("{} has non-standard DNA bases."),
)
def main(
    seq: str = typer.Argument(...),
    rev: bool = typer.Option(True, "-r", "--reverse", help="reverse sequence"),
    comp: bool = typer.Option(True, "-c", "--complement", help="complement sequence"),
    version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version.",
    ),
) -> None:

    print(revseq(seq, rev, comp))


@require(
    lambda seq: len(seq) != 0,
    error=lambda seq: ValueError("Nothing to do with an empty sequence"),
)
@typechecked
def revseq(
    seq: str,
    rev: bool = True,
    comp: bool = True,
) -> str:
    """Generate a (reverse) (complement) of DNA sequence

    Parameters
    ----------
    seq : str, required
        sequence to manipulate
    rev : bool, optional
        return the reversed sequence
    comp : bool, optional
        return the complemented sequence
    version : bool, optional
        display version number

    Returns
    -------
    str
        the (reverse) (complement) sequence
    """

    seq_deque = deque(seq)

    complement_dict = {
        "A": "T",
        "C": "G",
        "G": "C",
        "T": "A",
        "a": "t",
        "c": "g",
        "g": "c",
        "t": "a",
    }

    if rev:
        seq_deque.reverse()

    if comp:
        seq_deque = deque([complement_dict[_] if _ in complement_dict else _ for _ in seq_deque])

    return "".join(seq_deque)


if __name__ == "__main__":
    typer.run(main)  # pragma: no cover
