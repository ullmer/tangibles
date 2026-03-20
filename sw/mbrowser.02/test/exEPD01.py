import os, sys

sys.path.insert(0, #access module in parent directory (for test stubs)
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from enoPrismsDetails import EnoPrismsDetails

# Construct the trusted+overlay provider
epd = EnoPrismsDetails(
    base_yaml='yaml/prismsAcmTei01bb.yaml',
    overlay_yaml='yaml/prismsAcmTei01bo.yaml'
)

# Usual lifecycle
#epd.update()  # lazy setup of background actors
p1 = epd.summonPrism('teiLandscape', 0)
p2 = epd.summonPrism('teiYearsQ4', 1)

#print(epd)
#print(epd.cfg)
#print(epd.activePrisms)
print(p1)
print(p2)
#print("summon_map =", epd._summon_map)  # should show {('teiLandscape', 0): 'teiLandscape', ('teiYearsQ4', 1): 'teiYearsQ4'}
# in draw loop: provider.draw(screen)

