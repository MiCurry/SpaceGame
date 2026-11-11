# Code using Pillow to make stars
import os
import random
import time
import argparse
from dataclasses import dataclass
import math
import numpy as np

from PIL import Image


from aggdraw import Draw, Pen


from SpaceGame.shared import Line, Point
from SpaceGame.ideas.Star import Star, StarField, StarFieldConfig, StarFieldsGenerator


WHITE = 255
BLACK = 0

star_color = (0, 0, 0, 255)  # White color for the star
star_size = 10
star_size_range = (5, 15)  
star_density = 0.01  # Fraction of the image area covered by stars


def make_star(img, 
              center : Point,
              rotation_degrees : float,
              star_size : str,
              perturb_x=0.00,
              perturb_y=0.00):

    star = Star(center, rotation_degrees, star_size, perturb_x=perturb_x, perturb_y=perturb_y)
    star.make_star(img)
    star.add_glit(img)

def generate_random_brightness(nSamples):
    shape = 10.0
    scale = 2.0
    samples = np.random.default_rng().gamma(shape=shape, scale=scale, size=nSamples)
    scaled_samples = (samples / samples.max()) * 255
    scaled_samples = 255 - scaled_samples
    return scaled_samples

def make_start_field(seed=None):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed(time.time())


    # 1. Initialize the Generator (optionally set a seed for reproducibility)
    rng = np.random.default_rng(seed=42)

    width = 2024
    height = 2024

    img = Image.new("RGBA", 
                    (width, height), 
                    (0, 0, 0, 255))

    # First Generate large stars
    nLargeStars = 24

    # Draw samples from a gamma distribution (shape=2.0, scale=2.0)
    star_brightness = generate_random_brightness(nLargeStars)

    i = 0
    star_brightness.sort()
    for _ in range(nLargeStars):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        rotation = random.uniform(0, 360)

        star = Star(Point(x, y), rotation, 'large', star_brightness=int(star_brightness[i]))
        star.make_star(img)

        if random.random() < 0.05:
            star.add_glit(img)

        i += 1

    nMediumStars = 48
    star_brightness = generate_random_brightness(nMediumStars)
    i = 0
    star_brightness.sort()
    for _ in range(nMediumStars):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        rotation = random.uniform(0, 360)

        star = Star(Point(x, y), rotation, 'medium', star_brightness=int(star_brightness[i]))
        star.make_star(img)

        if random.random() < 0.05:
            star.add_glit(img)
        i += 1

    nSmallStars = 96
    star_brightness = generate_random_brightness(nSmallStars)
    i = 0
    star_brightness.sort()
    for _ in range(nSmallStars):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        rotation = random.uniform(0, 360)

        star = Star(Point(x, y),
                    rotation,
                    'small', star_brightness=int(star_brightness[i]))
        star.make_star(img)

        if random.random() < 0.05:
            star.add_glit(img)
        i += 1

    img.show()


def make_star_field_test(seed=None):
    make_start_field(seed=seed)

def basic_stars_test():
    img = Image.new("RGBA", 
                    (100, 100), 
                    (0, 0, 0, 255))


    make_star(img, Point(25, 25), 0, 'small', perturb_x=3.05, perturb_y=3.05)
    make_star(img, Point(25, 75), 0, 'medium')
    make_star(img, Point(75, 25), 0, 'large')
    img.show()


def make_star_field_new(seed=None, generator="new"):
    if seed is not None:
        random.seed(seed)
    width, height = 1024, 1024
    config = StarFieldConfig(nLargeStars=24, nMediumStars=75, nSmallStars=126)
    star_field = StarField("new_field_4", width, height, config)
    star_field.render(generator)

def make_star_fields(nFields=4, 
                     seed=None, 
                     generator='new', 
                     config=None,
                     show=False):
    if seed is not None:
        random.seed(seed)

    if config is not None:
        config = config
    else:
        config = StarFieldConfig(nLargeStars=24, nMediumStars=75, nSmallStars=126)

    width, height = 1024, 1024

    for field in range(nFields):
        print(f"Creating star field {field}")
        star_field = StarField(f"new_field_{field}", width, height, config)
        star_field.render(generator)
        if show:
            star_field.show()
        star_field.save(os.path.join('E:/Projects/SpaceGame/resources/png/backgrounds/star_fields',
                                     f'star_field_{field}.png'))

        #config.nLargeStars += 10
        #config.nMediumStars += 15
        #config.nSmallStars += 20




if __name__ == "__main__":
    print(os.getcwd())
    parser = argparse.ArgumentParser(description="Star Creator")
    parser.add_argument("--seed", type=int, help="Random seed for star generation")
    parser.add_argument("action", type=str, help="Action to perform (e.g., 'stars-test', 'star_field')")
    parser.add_argument("--nFields", '-n',type=int, help="Number of star fields to generate")
    parser.add_argument("--nLarge", type=int, help="Number of large stars to generate",
                        default=24)
    parser.add_argument("--nMedium", type=int, help="Number of medium stars to generate",
                        default=75)
    parser.add_argument("--nSmall", type=int, help="Number of small stars to generate",
                        default=126)
    parser.add_argument("--show", action="store_true", help="Show the star fields after creation")

    args = parser.parse_args()

    if args.action == "stars-test":
        basic_stars_test()

    if args.action == "star_field":
        make_star_field_new(seed=args.seed, generator="new")

    if args.action == "star_fields":
        make_star_fields(nFields=args.nFields, seed=args.seed,
                         config=StarFieldConfig(nLargeStars=args.nLarge, nMediumStars=args.nMedium, nSmallStars=args.nSmall),
                         show=args.show)

    if args.action == "star_fields_3d":
        gen = StarFieldsGenerator(width=1024, height=1024, 
                                  config=StarFieldConfig(nLargeStars=5, nMediumStars=10, nSmallStars=10),
                                  nFields=30)
        gen.render_fields(show=True)
