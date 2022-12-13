from src.data_parser import parser


def process_data(data):
    data = data[0].split(', ')
    x = [int(i) for i in data[0].split('x=')[1].split('..')]
    y = [int(i) for i in data[1][2:].split('..')]
    return x, y


def possible_velocities(data):
    x, y = process_data(data)
    x_min, x_max = x
    y_min, y_max = y

    x_vel_min = round((-1 + (1 + 8 * x_min) ** 0.5) / 2)
    x_vel_max = x_max

    y_vel_min = y_min
    y_vel_max = abs(y_min) - 1

    prob_velocities = 0

    for i in range(x_vel_min, x_vel_max + 1):
        for j in range(y_vel_min, y_vel_max + 1):
            x_var, y_var = 0, 0
            x_velocity = i
            y_velocity = j
            while x_var <= x_max and y_var >= y_min:

                if x_min <= x_var <= x_max and y_min <= y_var <= y_max:
                    prob_velocities += 1
                    break

                x_var += x_velocity
                x_velocity -= 1 if x_velocity > 0 else 0

                y_var += y_velocity

                y_velocity -= 1

    return prob_velocities


if __name__ == '__main__':
    test_data = parser("input/day17_test")
    actual_data = parser("input/day17")

    print(possible_velocities(test_data))
    print(possible_velocities(actual_data))
