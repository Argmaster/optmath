from concurrent.futures import ProcessPoolExecutor
from typing import Generator, Iterable, List, Set

import rich
from rich.progress import Progress

from optmath.motifs.sequence import SequenceLike

_POSITIVE: str = "[blue]%s[/]"
_NEGATIVE: str = "[red]%s[/]"
_NUCLEOTIDES: str = "ATGC"


def exhaustive(
    sequence: SequenceLike,
    mer_length: int,
    max_distance: int,
    sector_length: int,
) -> Set[str]:
    """Find all motifs from sequence.

    Parameters
    ----------
    sequence : SequenceLike
        sequence to search in. Only DNA is supported.
    mer_length : int
        k mer length.
    max_distance : int
        maximal distance for pattern to be considered matching.
    sector_length : int
        length of a sector in sequence that must contain pattern.

    Returns
    -------
    Set[str]
        set containing all possible matching motifs.
    """
    assert sector_length >= mer_length >= max_distance
    sequences: Set[str] = set()
    dna = sequence.as_dna()
    sectionized = dna.sectors(sector_length)
    # progress object is used for pretty signalizing progress of searching
    with Progress() as progress:
        all_k_mers = set(dna.iter_subsequences(mer_length, mer_length, True))
        task = progress.add_task(
            f"Finding motifs for {mer_length}-mers", total=len(all_k_mers)
        )
        # multiprocessing is used to speed up searching process
        with ProcessPoolExecutor() as executor:
            # runs find_motifs_for_k_mer for each (max_distance, sectionized,
            # all_k_mers) then iterates over results
            for k_mer_motifs in executor.map(
                find_motifs_for_k_mer,
                [max_distance] * len(all_k_mers),
                [sectionized] * len(all_k_mers),
                all_k_mers,
            ):
                # updating set removes all repetitions
                sequences.update(k_mer_motifs)
                progress.advance(task, 1)
    return sequences


def find_motifs_for_k_mer(
    max_distance: int,
    sectionized: Iterable[SequenceLike],
    k_mer: str,
) -> Set[str]:
    """Finds all motifs matching given k-mer.

    Parameters
    ----------
    max_distance : int
        max humming distance for pattern to be considered
        neighbour of k mer sequence.
    sectionized : Iterable[SequenceLike]
        sequence of all dna sections that have to contain
        given pattern with at most max_distance mismatches
        to consider it a motif.
    k_mer : str
        base k mer sequence for pattern generation.

    Returns
    -------
    Set[str]
        all patterns that appear in all sections.
    """
    sequences = set()
    for pattern in neighbors(k_mer, max_distance):
        for sector in sectionized:
            if not sector.contains(pattern, max_distance):
                break
        else:
            sequences.add(pattern)
    return sequences


def neighbors(pattern: str, max_mismatches: int) -> Set[str]:
    """Get all neighbor strings for pattern with at most max_mismatches.

    Parameters
    ----------
    pattern : str
        base pattern for neighbor creation.
    max_mismatches : int
        max number of mismatches between pattern and new string to consider
        new string a neighbor of pattern.

    Returns
    -------
    Set[str]
        all unique neighbors
    """
    neighborhood = {pattern}
    for _ in range(max_mismatches):
        extra = set()
        for sub_pattern in neighborhood:
            extra.update(immediate_neighbors(sub_pattern))
        neighborhood.update(extra)
    return neighborhood


def immediate_neighbors(pattern: str) -> Generator[str, None, None]:
    for i, char in enumerate(pattern):
        for nucleotide in _NUCLEOTIDES:
            if nucleotide != char:
                yield pattern[:i] + nucleotide + pattern[i + 1 :]


def print_mismatches(base: str, second: str) -> None:
    """Print two sequences with char match comparison.

    Consider "ATTTCCG" and "ATTGCTC" example:
    ```
    ATTTCCG
       | ||
    ATTgCtc
    ```
    Mismatching nucleotides are marked red in terminal
    supporting color tags.

    Parameters
    ----------
    base : str
        base string considered valid.
    second : str
        string to check mismatches from base.
    """
    rich.print(highlight_mismatches(base, second))


def highlight_mismatches(base: str, second: str) -> str:
    """Add rich tags to highlight string comparison."""
    assert len(base) == len(second)
    base = base.upper()
    base_line: List[str] = []
    mid_line: List[str] = []
    second_line: List[str] = []
    for base_char, second_char in zip(base, second):
        if base_char != second_char:
            base_line.append(_NEGATIVE % base_char)
            mid_line.append("|")
            second_line.append(_NEGATIVE % second_char.lower())
        else:
            base_line.append(_POSITIVE % base_char)
            mid_line.append(" ")
            second_line.append(_POSITIVE % second_char.upper())
    base_line_str = "".join(base_line)
    mid_line_str = "".join(mid_line)
    second_line_str = "".join(second_line)
    return f"{base_line_str}\n{mid_line_str}\n{second_line_str}"
