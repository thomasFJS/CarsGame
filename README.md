
Author: Thomas Fujise

# CarsGame

# Info
## Controller
- Use OpenCV to detect contours and filters out the blue color on the steering wheel
- It then gets the slope of the line formed using the center of the wheel and the top of the wheel and uses that to determine the steering input
- Also, the position center of the wheel is responsible for braking and accelerating
- The steering wheel is used as controller for the car game
## Game
- Player can moove on the road with keys (w-a-s-d)
- You need to dodge other cars on the road, if you hit a cars you loose.

# Usage (Requires python3):
1. `pip install -r requirements.txt`
2. `./run.sh`
 