from weather import WeatherRenderer
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from utils import args, led_matrix_options

args = args()
matrixOptions = led_matrix_options(args)
matrix = RGBMatrix(options = matrixOptions)
canvas = matrix.CreateFrameCanvas()

while True:
    WeatherRenderer(matrix, canvas).render()