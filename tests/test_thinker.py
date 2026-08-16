from datetime import datetime

from persistent_agency.runtime import Runtime
from persistent_agency.state import Observation, OperatingMode


def at(hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 8, 17, hour, minute)


def test_endogenous_cognition_advances_without_external_input():
    runtime = Runtime()
    first = runtime.tick(at(18))
    second = runtime.tick(at(18, 1))
    assert second.cycle == first.cycle + 1
    assert second.foreground != first.foreground


def test_human_question_interrupts_during_work_mode():
    runtime = Runtime(goals=["continue private research"])
    runtime.tick(at(9))
    question = Observation(
        source="human",
        content="What is the current test status?",
        salience=0.9,
        is_human_request=True,
    )
    state = runtime.tick(at(9, 1), [question])
    assert state.operating_mode == OperatingMode.HUMAN_WORK
    assert state.requested_action == "respond_to_human"
    assert "current test status" in state.foreground


def test_schedule_enters_open_cognition_and_consolidation():
    runtime = Runtime()
    assert runtime.tick(at(12, 30)).operating_mode == OperatingMode.OPEN_COGNITION
    assert runtime.tick(at(22)).operating_mode == OperatingMode.CONSOLIDATION


def test_consolidation_moves_short_term_state_into_long_term_memory():
    runtime = Runtime(goals=["prototype persistent cognition"])
    runtime.tick(at(18))
    runtime.tick(at(18, 1))
    assert runtime.memory.short_term
    runtime.tick(at(22))
    assert runtime.memory.long_term
    assert runtime.memory.consolidation_log
    assert runtime.memory.short_term == []
