#!/usr/bin/env python3
"""
Lab Lição 0012: Structured Streaming com Watermarking e Windowing
Exame DP-750: Descarte de dados atrasados (late arriving data) com watermark.
"""
from datetime import datetime, timedelta

def simulate_watermark_stream(events: list, watermark_delay_minutes: int):
    accepted = []
    dropped = []
    current_max_time = datetime.min
    
    for event in events:
        event_time = datetime.fromisoformat(event['timestamp'])
        if event_time > current_max_time:
            current_max_time = event_time
        
        watermark_threshold = current_max_time - timedelta(minutes=watermark_delay_minutes)
        if event_time >= watermark_threshold:
            accepted.append(event)
        else:
            dropped.append(event)
    return accepted, dropped

def test_streaming_watermark():
    events = [
        {'id': 1, 'timestamp': '2025-01-01T12:00:00'},
        {'id': 2, 'timestamp': '2025-01-01T12:15:00'}, # Max avança para 12:15, threshold = 12:05 (10 min)
        {'id': 3, 'timestamp': '2025-01-01T12:02:00'}  # Atrasado! Anterior a 12:05
    ]
    accepted, dropped = simulate_watermark_stream(events, watermark_delay_minutes=10)
    assert len(accepted) == 2
    assert len(dropped) == 1 and dropped[0]['id'] == 3
    print('✅ Lab 0012 OK: Watermarking filtrou eventos tardios com exatidão')

if __name__ == '__main__':
    test_streaming_watermark()
