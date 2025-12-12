def time_descriptor(estimated_time: int) -> None:
    if estimated_time < 60:
        print(f"Total time: [{int(estimated_time)}] seconds")
    elif estimated_time >= 3600:
        hours = estimated_time // 3600
        minutes = (estimated_time % 3600) // 60
        seconds = estimated_time - (hours * 3600) - (minutes * 60)
        print(
            f"Total time: "
            f"[{int(hours)}] hours - "
            f"[{int(minutes)}] minutes - "
            f"[{int(seconds)}] seconds"
        )
    else:
        minutes = estimated_time // 60
        seconds = estimated_time - (minutes * 60)
        print(
            f"Total time: "
            f"[{int(minutes)}] minutes - "
            f"[{int(seconds)}] seconds"
        )