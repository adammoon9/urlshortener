from .extensions import db
from .models.url import URL

class DBHelper():

    def create_url(url:str, shortCode:str) -> URL:
        url = URL(url=url, shortCode=shortCode)
        db.session.add(url)
        db.session.commit()

        return url

    def get_url(url:str) -> URL:
        result = db.session.query(URL).filter_by(shortCode=url).first()
        if result:
            result.accessCount += 1
            db.session.commit()
            return result
        return None

    def update_url(url:str, shortCode:str) -> URL:
        result = db.session.query(URL).filter_by(shortCode=shortCode).first()
        if result:
            result.url = url
            db.session.commit()
            return result
        return None

    def delete_url(url:str) -> int:
        result = db.session.query(URL).filter_by(shortCode=url).delete()
        if result > 0 and result <= 1:
            db.session.commit()
            return 204 # We only want 1 row deleted, if more than 1 then we have duplicate shortCodes
        if result == 0:
            db.session.rollback()
            return 404 # No rows affected, no matches on database query
