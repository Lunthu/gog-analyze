This is a simple code, aimed at collecting high-level data about games and reviews on GOG Galaxy Platform. It utilizes unofficial GOG API (https://gogapidocs.readthedocs.io/en/latest/) + methods presented on frontend (for reviews analysis).

The presented Python code contains 4 functions:

**games_basic_data** - extracts all basic information about games on GOG, including title, publisher, developer, release date, gallery, price. Receives "pages" as variable, which defines the number of requests (similar to offsets in classic API requests)

**reviews_agg_data** - extracts high-level review data of the selected game. 

**reviews_agg_data** - extracts high-level review data of the selected game + 10 reviews.

**reviews_full_data** - extracts all reviews of selected game.
