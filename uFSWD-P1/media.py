class Movie:
    """Class Movie provides a way to encapsulate data members used
    to define a Movie such as title, poster image etc..,
    """
    def __init__(self, title, image_url, trailer_url):
        """This method accepts data to generate a new movie object

        :param title: Movie title
        :type title: str

        :param image_url: URL to movie poster
        :type image_url: str

        :param trailer_url: URL to movie trailer hosted in youtube
        :type trailer_url: str
        """
        self.title = title
        self.trailer_youtube_url = trailer_url
        self.poster_image_url = image_url
