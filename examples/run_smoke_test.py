from datetime import datetime, timedelta

from persistent_agency.runtime import Runtime
from persistent_agency.state import Observation

runtime = Runtime(goals=["design and test a persistent cognitive architecture"])
start = datetime(2026, 8, 17, 7, 0)

for i in range(5):
    now = start + timedelta(hours=i)
    observations = []
    if i == 2:
        observations = [Observation("human", "Summarize what you are working on.", 1.0, True)]
    state = runtime.tick(now, observations)
    print(f"{now:%H:%M} | {state.operating_mode.value:22s} | cycle={state.cycle:02d} | {state.foreground}")
