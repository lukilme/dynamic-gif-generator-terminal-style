import pstats

p = pstats.Stats("profile.out")
p.print_stats()
