from fastapi import FastAPI, BackgroundTasks
from groa_ds_api.utils import MovieUtility
from groa_ds_api.models import RecInput, RecOutput, SimInput, SimOutput
import os
from pathlib import Path

app = FastAPI(
    title="groa-ds-api",
    description="Movie recommendations based on user ratings and preferences using a trained w2v model",
    version="1.0"
)

parent_path = Path(__file__).resolve().parents[1]
model_path = os.path.join(parent_path, 'w2v_limitingfactor_v2.model')

predictor = MovieUtility(model_path)


def create_app():
    
    @app.get("/")
    async def index():
        """
        Simple 'hello' from our API.
        """
        welcome_message = "This is the DS API for Groa"
        return welcome_message

    @app.post("/recommendations", response_model=RecOutput)
    async def get_recommendations(payload: RecInput, background_tasks: BackgroundTasks):
        """
        Given a `user_id`, the user's ratings are used to create a user's 'taste'
        vector. We then get the most similar movies to that vector using cosine similarity.

        Parameters: 

        - **user_id:** int
        - num_recs: int [1, 100]
        - good_threshold: int [3, 5]
        - bad_threshold: int [1, 3]
        - harshness: int [1, 2]

        Returns:

        - **data:** List[Movie]

        `Will not always return as many recommendations as 
        num_recs due to the algorithms filtering process.`
        """
        result = predictor.get_recommendations(payload, background_tasks)
        return result
    
    @app.post("/similar-movies", response_model=SimOutput)
    async def get_similar_movies(payload: SimInput):
        """
        Given a `movie_id`, we get the movie's vector using our trained `w2v` model. 
        We then get the most similar movies to that vector using cosine similarity.

        Parameters:

        - **movie_id:** str
        - num_movies: int [1, 100]

        Returns:

        - **data:** List[Movie]

        `Will reliably return as many recommendations as indicated
        in num_movies parameter.`
        """
        result = predictor.get_similar_movies(payload)
        return result
    
    @app.get("/service-providers/{movie_id}")
    async def service_providers(movie_id: str):
        """
        Given a `movie_id`, we provide the service providers and the links 
        to the movie of that service provider for quick access to the film.

        Parameters:
        - **movie_id:** str

        Returns:
        - **data:** List[Provider]

        Provider Object:
        - provider_id
        - name
        - link
        - presentation_type (HD or SD)
        - monetization_type (buy, rent or flatrate)
        """
        # could make a post and allow input of included_providers
        # should add caching for this query
        return predictor.get_service_providers(movie_id)

    @app.get("/stats/decades/{user_id}")
    async def get_stats_by_decade(user_id):
        # df = predictor.get_user_data(user_id)
        # df["decade"] = df["year"].apply(lambda x: x//10*10)
        # first_decade = df["decade"].min()
        # last_decade = df["decade"].max()
        # dec_to_count = {dec: 0 for dec in range(first_decade, last_decade+1, 10)}
        # for dec in df["decade"].values:
        #     dec_to_count[dec] += 1
        return "New class needs to be built for user_data"

    return app
