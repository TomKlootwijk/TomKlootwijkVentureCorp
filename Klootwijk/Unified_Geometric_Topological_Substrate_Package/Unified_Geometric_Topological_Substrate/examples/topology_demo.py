from __future__ import annotations

from ugts import HourglassRouter, KleinBottleQuotient, MobiusBand, PortalMap, Vec2


samples = [Vec2(-0.5, 0.25), Vec2(3.5, 0.25), Vec2(4.5, 0.25), Vec2(8.5, 0.25)]
print('Mobius quotient:')
band = MobiusBand(4.0, 2.0)
for p in samples:
    print(p, '->', band.map(p))

print('\nKlein quotient:')
klein = KleinBottleQuotient(4.0, 2.0)
for p in samples:
    print(p, '->', klein.map(p))

print('\nHourglass parity routing:')
router = HourglassRouter()
for chamber in ('A', 'B', 'C', 'D', 'PINCH'):
    print(chamber, 'p=0 ->', router.route(chamber, 0), ', p=1 ->', router.route(chamber, 1))
