import numpy as np
import pandas as pd


class SpaceImage:
    def __init__(self, width, height, data: str):
        self.width = width
        self.height = height
        self.layer_size = width * height
        self.n_layers = len(data) // self.layer_size
        if self.layer_size * self.n_layers != len(data):
            raise ValueError("data is the wrong shape")
        d = [int(c) for c in data]
        self.image = np.reshape(d, (self.n_layers, self.height, self.width))
        self.decoded_image = None

    def image_check(self):
        min_zeros = self.layer_size
        min_zero_idx = -1
        for layer_number, layer in enumerate(self.image):
            n_zeros = np.count_nonzero(layer.flatten() == 0)
            if min_zeros >= n_zeros:
                min_zeros = n_zeros
                min_zero_idx = layer_number
        return np.count_nonzero(
            self.image[min_zero_idx].flatten() == 1
        ) * np.count_nonzero(self.image[min_zero_idx].flatten() == 2)

    def decode_image(self):
        self.decoded_image = np.full((self.height, self.width), 2)
        for w in range(self.width):
            for h in range(self.height):
                depth = 0
                v = 2
                while depth < self.n_layers and v == 2:
                    v = self.image[depth, h, w]
                    depth += 1
                self.decoded_image[h, w] = v
        return self.decoded_image


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from pathlib import Path
    import os

    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "year2019", "day_08_input.txt")
    with open(file, "r") as f:
        image_data = f.readline().strip()

    image = SpaceImage(25, 6, image_data)
    assert image.image_check() == 1690
    print(f"Part 1: {image.image_check()}")
    print(f"Part 2:\n{image.decode_image()}")
    file = os.path.join(project_dir, "year2019", "day_08_part_2.png")
    plt.imsave(file, image.decoded_image)
    # it should read ZPZUB
