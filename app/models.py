# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import UserMixin

from app import db, login


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    username = db.Column(db.String(128), index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def check_password(self, password):
        return self.password == password


class Terrorist(db.Model):
    __tablename__ = 'terrorists'
    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    lname = db.Column(db.String(512), index=True)
    fname = db.Column(db.String(512))
    mname = db.Column(db.String(512))
    iin = db.Column(db.String(512))
    birthdate = db.Column(db.Date())
    note = db.Column(db.String(512))
    included = db.Column(db.Date())
    excluded = db.Column(db.Date())

    def __repr__(self):
        return "<Terrorist {}: {}>".format(self.id, self.lname)

    @staticmethod
    def iso_date(date_and_time):
        """Convert datetime to iso8601 format or None"""
        if date_and_time:
            return date_and_time.isoformat()
        else:
            return None

    def as_json(self):
        """Return Terrorist data as dictionary."""
        terrorist = dict(
                id=self.id, created=self.iso_date(self.created),
                lname=self.lname, fname=self.fname, mname=self.mname,
                iin=self.iin, birthdate=self.iso_date(self.birthdate),
                note=self.note, included=self.iso_date(self.included),
                excluded=self.iso_date(self.excluded)
            )
        return terrorist

    @staticmethod
    def init_active():
        """Create initial database records for active persons"""
        from app.kfm.utils import request_active
        active_persons_list = request_active('person')
        for x in active_persons_list:
            t = Terrorist(
                    lname=x['lname'], fname=x['fname'], mname=x['mname'],
                    iin=x['iin'], birthdate=x['birthdate'], note=x['note'],
                    included=x['included'], excluded=x['excluded']
                )
            db.session.add(t)
        db.session.commit()

    @staticmethod
    def init_excluded():
        """Create initial database records for excluded persons"""
        from app.kfm.utils import request_excluded

        excluded_persons_list = request_excluded('person')

        # We need to loop over persons and add exclusion date
        # to the history
        for ep in excluded_persons_list:
            # Find a person in db by iin or last 'name + first name'
            t = None  # found terrorist
            if ep['lname'] is not None and ep['fname'] is not None:
                t = db.session.query(Terrorist).filter(
                        Terrorist.lname == ep['lname'],
                        Terrorist.fname == ep['fname']
                    ).first()
            if t is not None:
                t.excluded = ep['excluded']
        # Commit all changes to database
        db.session.commit()

    @staticmethod
    def init_included():
        """Create initial database records for included persons"""
        from app.kfm.utils import request_included
        included_persons_list = request_included('person')

        # We need to loop over persons and check if person exists
        for ip in included_persons_list:
            # Find a person in database by iin or last 'name + first name'
            t = None  # found terrorist
            if ip['lname'] is not None and ip['fname'] is not None:
                t = db.session.query(Terrorist).filter(
                        Terrorist.lname == ip['lname'],
                        Terrorist.fname == ip['fname']
                    ).first()
            if t is None:
                t = Terrorist(
                        lname=ip['lname'], fname=ip['fname'],
                        mname=ip['mname'], iin=ip['iin'],
                        birthdate=ip['birthdate'], note=ip['note'],
                        included=ip['included'], excluded=ip['excluded']
                    )
                db.session.add(t)
                db.session.commit()


class Org(db.Model):
    __tablename__ = 'orgs'

    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    name = db.Column(db.String(512), index=True)
    name_eng = db.Column(db.String(512))
    note = db.Column(db.String(512))
    included = db.Column(db.Date())
    excluded = db.Column(db.Date())

    def as_json(self):
        """Return Organisation data as dictionary."""
        org = dict(
            id=self.id,
            created=self.iso_date(self.created),
            name=self.name,
            name_eng=self.name_eng,
            note=self.note,
            included=self.iso_date(self.included),
            excluded=self.iso_date(self.excluded)
        )
        return org

    @staticmethod
    def iso_date(date_and_time):
        """Convert datetime object to iso8601 format"""
        if date_and_time:
            return date_and_time.isoformat()
        else:
            return None

    @staticmethod
    def init_active():
        """Initialize active organizations records to database"""
        from app.kfm.utils import request_active
        active_orgs_list = request_active('org')
        for k in active_orgs_list:
            o = Org(
                    name=k['org_name'], name_eng=k['org_name_en'],
                    note=k['note'], included=k['included']
                )
            db.session.add(o)
        db.session.commit()

    @staticmethod
    def init_excluded():
        """Initialize excluded organizations records to database"""
        from app.kfm.utils import request_excluded
        excluded_orgs_list = request_excluded('org')
        for an_org in excluded_orgs_list:
            to = None
            if an_org['org_name'] is not None:
                to = Org.query.filter_by(name=an_org['org_name']).first()
            if to is not None:
                t.excluded = an_org['excluded']
        db.session.commit()

    @staticmethod
    def init_included():
        """Create initial database records for included orgs"""
        from app.kfm.utils import request_included
        included_orgs_list = request_included('org')
        # We need to loop over orgs and check if org exists
        for iorg in included_orgs_list:
            # Find a person in database by iin or last 'name + first name'
            o = None  # found terrorist
            if iorg['name'] is not None:
                o = db.session.query(Org).filter(
                        Org.name == iorg['name']
                    ).first()
            if o is None:
                o = Org(
                        name=iorg['org_name'], name_eng=iorg['org_name_en'],
                        note=iorg['note'], included=iorg['included']
                    )
                db.session.add(o)
                db.session.commit()


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    message = db.Column(db.String(512))


# --------------- Helper Functions --------------------------------------------
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
