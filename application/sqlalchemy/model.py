from application import db

class User(db.Model):
    name = db.Column(db.String(40), primary_key=True)
    email = db.Column(db.String(256))

    def to_user(self):
        return dict(
            name=self.name,
            email=self.email,
        )

class OAuth2Token(db.Model):
    name = db.Column(db.String(40))
    token_type = db.Column(db.String(40))
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