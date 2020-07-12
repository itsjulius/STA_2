# game settings
screen_width = 1280
screen_height = 800
collision_corner_dist = 25  # distance from the car center to the corner collision points
racetrack = 'tracks/racetrack_1.png'
car_size = 80  # car img size (must be a square)

# NN - GA settings
timeout = 2000  # max frames before gen ends, if there are still cars remaining
n_gen = 2000   # max number of generations
car_timeout = 20  # max frames a car survives if it does not change its position
steering_thr = 0.85  # threshold to steer to left or right values must be [0;1]
acc_thr = 0.85  # threshold to accelerate values must be [0;1]
brake_thr = 0.85  # threshold to accelerate values must be [0;1]
distance_weight = 1  # weight for valuing the distance for the cars fitness
time_weight = 0  # weight for valuing the time for the cars fitness (note: its distance * dstance_weight/(time_weight*time))
bonus = 500   #bonus for fitness for each bonus_dist
bonus_dist = 200   #needed distance to gather bonus

# car settings
acc_car = 2
brake_car = 1
steer_speed_car = 3  # max angle frame per frame
max_speed_car = 6
