import numpy as np
from typing import List, Tuple, Union


def split_at(array: np.array, value) -> List[np.array]:
    """Split an array after every index where it contains `value`.

    Parameters
    ----------
    array : np.array
        The array to split insections
    value : mixed
        The value at which to split the array

    Returns
    -------
    List[np.array]
        A list of array sections
    """
    matches = np.isnan(array) if np.isnan(value) else array == value
    splitpoints = np.where(matches)[0] + 1
    if splitpoints[-1] == len(array):
        splitpoints = splitpoints[:-1]
    return np.array_split(array, splitpoints)


def split_at_nan(array: np.array, skip_empty: bool = False) -> List[np.array]:
    """Split an array whenever it contains A NaN.

    Parameters
    ----------
    array : np.array
        The array to split in sections
    skip_empty : bool, optional
        Whether to skip empty sections, by default False

    Returns
    -------
    List[np.array]
        A list of arrays, each a section of the original array
    """
    sections = []
    for section in split_at(array, np.nan):
        if np.isnan(section[-1]):
            section = section[:-1]
        if len(section) > 0 or not skip_empty:
            sections.append(section)
    return sections


def sliding_window(array: np.array, window: int) -> np.array:
    """Returns a matrix where every row corresponds to a window from the array

    Parameters
    ----------
    array : np.array
        An array
    window : int
        The size of the window

    Returns
    -------
    np.array
        A matrix with as many columns as the window size, and each row
        corresponds to a slice from the original array.
    """

    if window > len(array):
        return np.array([])
    N = len(array) - window + 1
    repeated_windows = np.tile(np.arange(window), (N, 1))
    indices = repeated_windows + np.arange(N)[:, np.newaxis]
    return array[indices]


def interval_motifs(
    songs: np.array, length: int = 2, normalize: bool = False
) -> Union[np.array, Tuple[np.array, np.array]]:
    """Return an matrix of motifs from an interable of songs, represented by
    an array of pitches. A motif is then a subsequence of *intervals* between
    successive pitches.

    Parameters
    ----------
    songs : Iterable[np.array]
        An iterable of songs: arrays with pitches
    length : int, optional
        The length or size of the motif, by default 2
    normalize : bool, optional
        whether to normalize the motifs, by default False

    Returns
    -------
    Union[np.array, Tuple[np.array, np.array]]
        Either the motifs (if normalize=False) or otherwise both the motifs and
        their normalizing values ('total interval sizes').
    """
    motifs = []
    for song in songs:
        intervals = song[1:] - song[:-1]
        song_motifs = sliding_window(intervals, length)
        motifs.extend(song_motifs)
    motifs = np.array(motifs)

    if not normalize:
        return motifs
    else:
        duration = motifs.sum(axis=1)
        motifs = motifs / duration[:, np.newaxis]
        return motifs, duration


def normalize(motifs: np.array) -> Tuple[np.array, np.array]:
    """Normalize the rows of an array (of motifs)

    Parameters
    ----------
    motifs : np.array
        The array to normalize

    Returns
    -------
    Tuple[np.array, np.array]
        A row-normalized array
    """
    duration = motifs.sum(axis=1)
    motifs = motifs / duration[:, np.newaxis]
    return motifs, duration
