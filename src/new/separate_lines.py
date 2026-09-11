def separate_lines(lines, angle_tolerance=10):

    verticals = []
    horizontal = []

    # Check whether no lines were detected
    if lines is None:
        return verticals, horizontal

    for line in lines:

        # Convert the segment to a 1D array
        line = np.asarray(line).reshape(-1)

        # Ensure that the segment has exactly 4 coordinates
        if line.size != 4:
            print(
                f"Warning: segment ignored. "
                f"Format found: {line.shape}"
            )
            continue

        # Coordinates of the start and end points
        x1, y1, x2, y2 = line.astype(float)

        # Differences between the points
        dx = x2 - x1
        dy = y2 - y1

        # Calculate the line angle
        angulo = np.degrees(
            np.arctan2(dy, dx)
        )

        # Convert the angle to the range [0, 180)
        angulo = angulo % 180

        # --------------------------------------------------
        # VERTICAL line
        # --------------------------------------------------

        if abs(angulo - 90) <= angle_tolerance:

            # Average X coordinate
            x = (x1 + x2) / 2

            verticals.append(x)

        # --------------------------------------------------
        # HORIZONTAL line
        # --------------------------------------------------

        elif (
            angulo <= angle_tolerance
            or abs(angulo - 180) <= angle_tolerance
        ):

            # Average Y coordinate
            y = (y1 + y2) / 2

            horizontal.append(y)

    return verticals, horizontal
