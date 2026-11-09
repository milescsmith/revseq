from collections import deque
from importlib.metadata import version
from typing import Annotated

import typer
from icontract import require
from rich import print as rprint
from typeguard import typechecked


def version_callback(value: bool) -> None:
    """Prints the version of the package."""
    if value:
        rprint(f"[red]{__name__}[/red] version: {version(__name__)}")
        raise typer.Exit()


app = typer.Typer(
    name="revseq", help="Generate reversed, reverse complement, and complement sequences", no_args_is_help=True
)


@app.callback(invoke_without_command=True)
@app.command(no_args_is_help=True)
@require(
    lambda seq: len(set(seq) - set("AGCTagctUuWwSsMmKkRrYyBbDdHhVvNn")) == 0,
    error=lambda seq: ValueError(f"{seq} has non-standard DNA bases."),
)
def main(
    seq: Annotated[str, typer.Argument()],
    rev: Annotated[bool, typer.Option("-r", "--reverse", help="reverse sequence")] = False,
    comp: Annotated[bool, typer.Option("-c", "--complement", help="complement sequence")] = False,
    colorize: Annotated[bool, typer.Option("-l", "--colorize", help="add color to the sequence")] = False,
    version: Annotated[
        bool | None,
        typer.Option(
            "-v",
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Prints the version.",
        ),
    ] = None,
) -> None:

    rprint(revseq(seq, rev, comp, colorize))


@require(
    lambda seq: len(seq) != 0,
    error=lambda _: ValueError("Nothing to do with an empty sequence"),
)
@typechecked
def revseq(
    seq: str,
    rev: bool = False,
    comp: bool = False,
    colorize: bool = False,
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
        "U": "A",
        "u": "a",
        "W": "W",
        "w": "w",
        "S": "S",
        "s": "s",
        "M": "K",
        "m": "k",
        "K": "M",
        "k": "m",
        "R": "Y",
        "r": "y",
        "Y": "R",
        "y": "r",
        "B": "V",
        "b": "v",
        "D": "H",
        "d": "h",
        "H": "D",
        "h": "d",
        "V": "B",
        "v": "b",
        "N": "N",
        "n": "n",
    }

    if rev:
        seq_deque.reverse()

    if comp:
        seq_deque = deque([complement_dict[_] if _ in complement_dict else _ for _ in seq_deque])

    if colorize:
        seq_deque = add_color(seq_deque)

    return "".join(seq_deque)


def add_color(seq: deque[str]) -> deque[str]:
    repl_dict = {
        "A": r"[red]A[/]",
        "a": r"[red]a[/]",
        "C": r"[yellow1]C[/]",
        "c": r"[yellow1]c[/]",
        "G": r"[green3]G[/]",
        "g": r"[green3]g[/]",
        "T": r"[dodger_blue2]T[/]",
        "t": r"[dodger_blue2]t[/]",
        "U": r"[dark_khaki]U[/]",
        "u": r"[dark_khaki]u[/]",
        "W": r"[dark_cyan]W[/]",
        "w": r"[dark_cyan]w[/]",
        "S": r"[orange]S[/]",
        "s": r"[orange]s[/]",
        "M": r"[chartreuse1]M[/]",
        "m": r"[chartreuse1]m[/]",
        "K": r"[purple]K[/]",
        "k": r"[purple]k[/]",
        "R": r"[dark_red]R[/]",
        "r": r"[dark_red]r[/]",
        "Y": r"[dark_green]Y[/]",
        "y": r"[dark_green]y[/]",
        "B": r"[yellow4]B[/]",
        "b": r"[yellow4]b[/]",
        "D": r"[magenta]D[/]",
        "d": r"[magenta]d[/]",
        "H": r"[gold1]H[/]",
        "h": r"[gold1]h[/]",
        "V": r"[#b8860b]V[/]",
        "v": r"[#b8860b]v[/]",
        "N": r"[#2f4f4f]N[/]",
        "n": r"[#2f4f4f]n[/]",
    }

    return deque([repl_dict[x] for x in seq])


if __name__ == "__main__":
    app()  # pragma: no cover
