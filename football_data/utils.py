def result_to_points(result, team, home, away) -> int:
    if result == "H":
        return 3 if team == home else 0
    elif result == "A":
        return 3 if team == away else 0
    else:
        return 1

