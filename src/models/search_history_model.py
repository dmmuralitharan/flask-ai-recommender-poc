from datetime import datetime, timezone
from src import db


class SearchHistory(db.Model):
    __tablename__ = "search_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    search_query = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    user = db.relationship("User", backref=db.backref("search_history", lazy=True))

    def __repr__(self):
        return f"<SearchHistory user_id={self.user_id} query={self.search_query}>"
