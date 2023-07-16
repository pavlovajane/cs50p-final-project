from swagger_server.persistence.repository import DbRepository
from swagger_server.models.quote import Quote  # noqa: E501
from swagger_server.models.movie import Movie # noqa: E501
from swagger_server.models.scene import Scene # noqa: E501
from injector import inject
import random

class QuotesService:

    @inject
    def __init__(self, repo: DbRepository, ) -> None:
        self.repo = repo

    def get_random_quote(self):
        # randomize for an id
        minrows =  self.repo.find_all("SELECT MIN(id) FROM scripts")
        maxrows =  self.repo.find_all("SELECT MAX(id) FROM scripts")
        if len(maxrows) == 0:
            return None
        random_id = random.randint(minrows[0][0],maxrows[0][0])

        rows =  self.repo.find_all("SELECT * FROM scripts WHERE id = ?",(random_id,))
        if len(rows) == 0:
            return None

        return Quote(id = rows[0][0],
                    movie=Movie(name=rows[0][1]),
                    scene=Scene(number=rows[0][2],name=rows[0][3]),
                    type=rows[0][4],
                    character=rows[0][5],
                    text=rows[0][6])

    def find_quote(self, text):
        
        rows =  self.repo.find_all("SELECT * FROM scripts WHERE text LIKE ?",(f"%{text}%",))
        if len(rows) == 0:
            return None

        quotes = []
        for r in rows:
            quote = Quote(id = r[0],
                    movie=Movie(name=r[1]),
                    scene=Scene(number=r[2],name=r[3]),
                    type=r[4],
                    character=r[5],
                    text=r[6])
            quotes.append(quote)

        return quotes

