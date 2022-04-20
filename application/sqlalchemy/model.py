from application import db

class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(256))
    namefirst = db.Column(db.String(50))
    namelast = db.Column(db.String(50))
    gender = db.Column(db.Boolean())
    age = db.Column(db.PositiveIntegerField())

    def to_user(self):
        return dict(
            username=self.username,
            email=self.email,
            namefirst=self.namefirst,
            namelast=self.namelast,
            gender=self.gender,
            age=self.age,
        )

class OAuth2Token(db.Model):
    name = db.Column(db.String(50))
    token_type = db.Column(db.String(50))
    access_token = db.Column(db.String(256))
    refresh_token = db.Column(db.String(256))
    expires_at = db.Column(db.PositiveIntegerField())
    user = db.Column(db.ForeignKey(User))

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )