import os
from dataclasses import dataclass
import math

import random
import numpy as np

from SpaceGame.shared import Line, Point
from aggdraw import Draw, Pen
from PIL import Image

PURE_WHITE = (255, 255, 255, 255)



@dataclass
class StarConfig:
    pen_thin_width: float
    pen_thick_width: float
    thin_line_legnth: int
    thick_line_length: int
    glit_size: int

star_size_config = {
    'small' : StarConfig(
        pen_thin_width=1.0,
        pen_thick_width=4.0,
        thin_line_legnth=10,
        thick_line_length=3,
        glit_size=2
    ),
    'medium' : StarConfig(
        pen_thin_width=1.0,
        pen_thick_width=4.0,
        thin_line_legnth=10,
        thick_line_length=3,
        glit_size=2
    ),
    'large' : StarConfig(
        pen_thin_width=1.0,
        pen_thick_width=3.0,
        thin_line_legnth=13,
        thick_line_length=4,
        glit_size=2
    )
}

class Star():
    def __init__(self, center : Point,
                       rotation_degrees,
                       star_size, 
                       star_brightness=255,
                       **kwargs):
        self.center = center
        self.rotation_degrees = rotation_degrees
        self._config = star_size_config[star_size]
        self.star_brightness = star_brightness
        self.color = (255, 255, 255, self.star_brightness)

        self.perturb_x_eps = kwargs.get('perturb_x', 0.00)
        self.perturb_y_eps = kwargs.get('perturb_y', 0.00)
        self.perturb_x : float = random.uniform(-self.perturb_x_eps, self.perturb_x_eps)
        self.perturb_y : float = random.uniform(-self.perturb_y_eps, self.perturb_y_eps)

        self.x_length_pert_eps = kwargs.get('x_length_pert', 2.00)
        self.x_length_pert = random.gauss(0, self.x_length_pert_eps)

        self.y_length_pert_eps = kwargs.get('y_length_pert', 2.00)
        self.y_length_pert = random.gauss(0, self.y_length_pert_eps)
    
    def __str__(self):
        return f"Star({self.center.x}, {self.center.y})"

    def __repr__(self):
        return f"<Star({self.center.x}, {self.center.y})>"

    def make_star(self, img, perturb_x=None, perturb_y=None):
        draw = Draw(img)

        if perturb_x is None:
            perturb_x = self.perturb_x
        if perturb_y is None:
            perturb_y = self.perturb_y

        pen_thin = Pen(self.color, self._config.pen_thin_width)
        pen_thick = Pen(self.color, self._config.pen_thick_width)

        x_line_thin = Line(self.center, 
                           self._config.thin_line_legnth + self.x_length_pert,
                           self.rotation_degrees,
                           perturb_start=perturb_x)
        x_line_thick = Line(self.center,
                            self._config.thick_line_length + self.x_length_pert,
                            self.rotation_degrees)

        y_line_thin = Line(self.center,
                           self._config.thin_line_legnth + self.y_length_pert,
                           self.rotation_degrees + 90,
                           perturb_start=perturb_y)
        y_line_thick = Line(self.center,
                            self._config.thick_line_length + self.y_length_pert,
                            self.rotation_degrees + 90,
                            )

        draw.line(x_line_thin.value, pen_thin)
        draw.line(x_line_thick.value, pen_thick)
        draw.line(y_line_thin.value, pen_thin)
        draw.line(y_line_thick.value, pen_thick)
        draw.flush()

    def add_glit(self, img):
        draw = Draw(img)
        pen_thin = Pen(self.color, self._config.pen_thin_width)

        glit_line = Line(self.center + (0, self._config.thin_line_legnth + 1),
                         self._config.glit_size, 90)
        glit_line.rotate(around=self.center, angle=self.rotation_degrees)

        draw.line(glit_line.value, pen_thin)

        glit_line = Line(self.center - (0, self._config.thin_line_legnth + 1),
                         self._config.glit_size,
                         90)
        glit_line.rotate(around=self.center, angle=self.rotation_degrees)
        draw.line(glit_line.value, pen_thin)
        draw.flush()


@dataclass
class StarFieldConfig:
    nLargeStars : int
    nMediumStars : int
    nSmallStars : int

class StarField:
    def __init__(self, name, width, height, config: StarFieldConfig):
        self.name = name
        self.width = width
        self.height = height
        self.stars = []
        self.stars_by_size = { 'large' : [], 'medium' : [], 'small' : [] }
        self.config : StarFieldConfig = config
        self.img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))


    def generate_random_brightness(self, nSamples, shape=10.0, scale=2.0):
        samples = np.random.default_rng().gamma(shape=shape, scale=scale, size=nSamples)
        scaled_samples = (samples / samples.max()) * 210
        scaled_samples = 210 - scaled_samples
        scaled_samples = scaled_samples.astype(int)
        return scaled_samples


    def _uniform_generator(self, img, star_size : str, nStars : int):
        star_brightness = self.generate_random_brightness(nStars)

        for i in range(nStars):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            rotation_degrees = random.randint(0, 360)
            star = Star(center=Point(x, y), 
                        rotation_degrees=rotation_degrees, 
                        star_size=star_size, 
                        star_brightness=star_brightness[i],
                        perturb_x=3.05,
                        perturb_y=3.05)
            self.stars.append(star)
            self.stars_by_size[star_size].append(star)
            star.make_star(img)

        return img

    def uniform_generator(self, img):
        self._uniform_generator(img, "large", self.config.nLargeStars)
        self._uniform_generator(img, "medium", self.config.nMediumStars)
        self._uniform_generator(img, "small", self.config.nSmallStars)

    def generate_stars_around(self,
                              star_size : 'str', 
                              seed_stars : list[Star], 
                              nStars : int=None,
                              distance_from_seed_stars : float=75):

        print("Starting star field generation")
        star_birghtness = self.generate_random_brightness(5000)
        str_cnt = 0

        for seed_star in seed_stars:
            points_2d = np.random.normal(loc=(seed_star.center.x, seed_star.center.y),
                                         scale=distance_from_seed_stars,
                                         size=(nStars, 2))

            print(f"Generating {nStars} stars around seed star at ({seed_star.center.x}, {seed_star.center.y})")
            for iStar in range(nStars):
                center = Point(x=points_2d[iStar, 0], y=points_2d[iStar, 1])
                star = Star(center=center,
                            rotation_degrees=random.randint(0,360),
                            star_size=star_size,
                            star_brightness=star_birghtness[str_cnt],
                            perturb_x=3.05,
                            perturb_y=3.05)

                self.stars.append(star)
                self.stars_by_size[star_size].append(star)
                star.make_star(self.img)
                str_cnt += 1

        return self.img

    def new_generator(self, img):
        # First place some large stars
        self._uniform_generator(img, "large", self.config.nLargeStars)

        distance_from_large_stars = 200
        distance_from_med_stars = 300
        n_med_stars_per_large = math.ceil(self.config.nMediumStars / self.config.nLargeStars)

        medium_star_brightness = self.generate_random_brightness(self.config.nMediumStars+self.config.nSmallStars+100)
        iStar = 0


        print("Creating large stars as seed stars")
        for large_star in self.stars_by_size['large']:
            points_2d = np.random.normal(loc=(large_star.center.x, large_star.center.y),
                                         scale=distance_from_large_stars,
                                         size=(n_med_stars_per_large, 2))

            for med_stars in range(n_med_stars_per_large):
                center = Point(x=points_2d[med_stars,0], y=points_2d[med_stars,1])
                med_star = Star(center, random.randint(0,360), 'medium', star_brightness=medium_star_brightness[iStar],
                                perturb_x=3.05, perturb_y=3.05)
                self.stars_by_size['medium'].append(med_star)
                med_star.make_star(img)
                iStar += 1

        print("Creating medium and small stars around large stars")
        n_small_stars_per_med = math.ceil(self.config.nSmallStars / self.config.nMediumStars)
        for med_star in self.stars_by_size['large']:
            points_2d = np.random.normal(loc=(med_star.center.x, med_star.center.y),
                                         scale=distance_from_med_stars,
                                         size=(n_small_stars_per_med, 2))

            for small_star in range(n_small_stars_per_med):
                center = Point(x=points_2d[small_star, 0], y=points_2d[small_star,1])
                small_star = Star(center, random.randint(0,360), 'small', star_brightness=medium_star_brightness[iStar],
                                  perturb_x=3.05, perturb_y=3.05)
                self.stars_by_size['small'].append(small_star)
                small_star.make_star(img)
                iStar += 1
                

    def render(self, generator, show=False):
        self.img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))

        if generator == "uniform":
            self.uniform_generator(self.img)
        elif generator == "new":
            self.new_generator(self.img)

        if show:
            self.show()

    def show(self):
        self.img.show()

    def save(self, fname=None):
        if fname is None:
            fname = f"{self.name}.png"
        self.img.save(fname)


class StarFieldsGenerator:
    """ Generate a series of star fields to be the background"""

    def __init__(self, width : int, height : int, config : StarFieldConfig, nFields : int):
        self.width = width
        self.height = height
        self.config = config
        self.nFields = nFields
        self.stars_by_size = {
            'large': [],
            'medium': [],
            'small': []
        }

    def generate_seed_stars(self):
        self.seed_stars = StarField('seeds', self.width, self.height,
                                    self.config)
        self.seed_stars._uniform_generator(self.seed_stars.img, 'large', self.config.nLargeStars)

    def render_fields(self, show=False):
        self.generate_seed_stars()
        self.seed_stars.save(f"field_3d_0.png")

        print("Saving star field as: field_3d_0.png")

        distance = 75
        for field in range(self.nFields):
            print(f"Creating star field {field+1}")
            field_stars = StarField(f'field_{field+1}', self.width, self.height, self.config)
            field_stars.generate_stars_around('medium', self.seed_stars.stars_by_size['large'],
                                              nStars=self.config.nMediumStars,
                                              distance_from_seed_stars=distance)
            field_stars.generate_stars_around('small', self.seed_stars.stars_by_size['medium'],
                                              nStars=self.config.nSmallStars,
                                              distance_from_seed_stars=distance)
            distance += 30
            print(f"Saving star field as: field_3d_{field+1}.png")
            path = os.path.join('E:/Projects/SpaceGame/resources/png/backgrounds/star_fields',
                                     f'star_3d_{field+1}.png')
            print(f"Saving star field as: {path}")
            field_stars.save(path)  




