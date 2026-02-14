from datetime import datetime, timezone

DEFAULT_WINDOW_MS = 5000

def clamp01(x: float) -> float:
    x = float(x)
    return max(0.0, min(1.0, x))

def predict(payload: dict) -> dict:
    raw = payload.get("raw_signals", {}) or {}
    game_context = payload.get("game_context", {}) or {}
    vad = payload.get("vad", {}) or {}

    window_ms = int(raw.get("window_ms", DEFAULT_WINDOW_MS) or DEFAULT_WINDOW_MS)

    move_count = max(int(raw.get("move_count", 0)), 1)
    push_with_box = int(raw.get("push_with_box_count", 0))
    moves_without_box = int(raw.get("moves_without_box_count", 0))
    wrong = int(raw.get("wrong_direction_count", 0))
    repeated = int(raw.get("repeated_move_count", 0))
    stuck = int(raw.get("boxes_stuck_in_window", 0))
    undos = int(raw.get("undos_in_window", 0))
    idle_time_ms = int(raw.get("idle_time_ms", 0))
    idle_count = int(raw.get("idle_count", 0))
    avg_gap_ms = int(raw.get("avg_time_between_moves_ms", 0))
    timing_std_ms = int(raw.get("timing_std_ms", 0))
    boxes_on_target_delta = int(raw.get("boxes_on_target_delta", 0))

    # Derived metrics (requested in schema discussion)
    major_errors = undos + stuck
    minor_errors = wrong + repeated

    # Placeholder behavioral metrics (deterministic)
    interaction_intensity = clamp01(move_count / 40.0)
    pause_frequency = clamp01(idle_time_ms / window_ms)
    error_rate = clamp01((major_errors * 1.0 + minor_errors * 0.5) / move_count)
    interaction_instability = clamp01(timing_std_ms / 500.0)

    # Placeholder “stress” (at least one computed output)
    stress = clamp01(0.5 * interaction_intensity + 0.5 * error_rate)

    # Confidence: simple heuristic from data completeness
    completeness = 1.0
    if move_count <= 1:
        completeness -= 0.3
    if avg_gap_ms <= 0:
        completeness -= 0.2
    if window_ms != DEFAULT_WINDOW_MS:
        completeness -= 0.1
    confidence = clamp01(0.6 + 0.4 * completeness)

    session_id = payload.get("session_id") or payload.get("scenario_id") or "UNKNOWN"
    timestamp = datetime.now(timezone.utc).isoformat()

    # Output JSON (integration-test friendly, includes derived values)
    return {
        "session_id": session_id,
        "timestamp": timestamp,
        "prediction": {
            "stress": round(stress, 3),
            "confidence": round(confidence, 3)
        },
        "behavioral_metrics": {
            "interaction_intensity": round(interaction_intensity, 3),
            "error_rate": round(error_rate, 3),
            "pause_frequency": round(pause_frequency, 3),
            "performance_quality": round(clamp01(1.0 - error_rate + (boxes_on_target_delta * 0.1)), 3),
            "temporal_features": {
                "interaction_instability": round(interaction_instability, 3)
            }
        },
        "derived_metrics": {
            "major_errors": major_errors,
            "minor_errors": minor_errors,
            "idle_count": idle_count
        },
        "echo": {
            "vad": vad,
            "game_context": game_context,
            "raw_signals": {
                "window_ms": window_ms,
                "move_count": move_count,
                "push_with_box_count": push_with_box,
                "moves_without_box_count": moves_without_box,
                "wrong_direction_count": wrong,
                "repeated_move_count": repeated,
                "boxes_stuck_in_window": stuck,
                "undos_in_window": undos,
                "idle_time_ms": idle_time_ms,
                "idle_count": idle_count,
                "avg_time_between_moves_ms": avg_gap_ms,
                "timing_std_ms": timing_std_ms,
                "boxes_on_target_delta": boxes_on_target_delta
            }
        }
    }