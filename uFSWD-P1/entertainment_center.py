#!/usr/bin/env python
from media import Movie
from fresh_tomatoes import open_movies_page
# Initializing the data array with Movie objects
# Movie objects are defined using the imported class from media.py
data = [
    Movie('SPIDER-MAN: Homecoming',
        'http://t0.gstatic.com/images?q=tbn:ANd9GcT8W3Fe7DD101g0M7OCalJN9u675sQAJFslGCjvs74PTOfEKt_t',  # noqa
        'https://www.youtube.com/watch?v=DiTECkLZ8HM'),
    Movie('Guardians of the Galaxy Vol. 2',
        'http://t2.gstatic.com/images?q=tbn:ANd9GcSzRHzPW9j56dGLliOdUV0lzjeUwfALe9Zn2Ys7Kkwj4YsvDpsh',  # noqa
        'https://www.youtube.com/watch?v=dW1BIid8Osg'),
    Movie('Thor: Ragnarok',
        'http://t1.gstatic.com/images?q=tbn:ANd9GcQAmMN0WnVLHXIKsFbj7dp7-HTUmyQ_d46RruMyj7Tv33mqXy7i',  # noqa
        'https://www.youtube.com/watch?v=v7MGUNV8MxU'),
       ]
# Generating the HTML page
open_movies_page(data)
