#!/usr/bin/env python3
import cProfile
from pstats import Stats, SortKey
from track_file_creation import Create_tracks

def run_profiling():
    print(Create_tracks(True))

if __name__ == 'Profiling':
    with cProfile.Profile() as pr:
        run_profiling()

    with open('profiling_stats.txt','w') as stream:
        stats = Stats(pr, stream=stream)
        stats.strip_dirs()
        stats.sort_stats('time')
        stats.dump_stats('.prof_stats')
        stats.print_stats()