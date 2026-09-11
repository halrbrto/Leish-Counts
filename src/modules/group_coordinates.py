import numpy as np  

def group_coordinates(coordinates, distance=10): 

    # Return an empty list when no coordinates are provided.
    if len(coordinates) == 0:
        return []

    # Sort coordinates so that nearby values can be processed sequentially.
    coordinates = sorted(coordinates)

    # Store the completed groups of nearby coordinates.
    groups = []

    # Start the first group with the smallest coordinate.
    current_group = [
        coordinates[0]
    ]

    # Compare each remaining coordinate with the current group's center.
    for value in coordinates[1:]:

        # Calculate the center of the coordinates in the current group.
        center = np.mean(
            current_group
        )

        # Add the value to the current group when it is within the allowed distance.
        if abs(value - center) <= distance:

            current_group.append(value)

        # Otherwise, finish the current group and start a new one.
        else:

            groups.append(
                current_group
            )

            current_group = [
                value
            ]

    # Add the final group after all coordinates have been processed.
    groups.append(
        current_group
    )

    # Represent each group by its center.
    centers = [
        np.mean(group)
        for group in groups
    ]
    
    return centers