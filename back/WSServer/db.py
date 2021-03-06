#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

from config import *
from .channel import Channel
import json


class Db:
    def __init__(self, lock):
        self.lock = lock
        self.users = {}
        self.db_update()

        self.games = {}

        self.handlers = []

        self.main_channel = Channel('main')
    
    def db_update(self):
        with self.lock:
            with open(USERS, 'r', encoding='utf-8') as f:
                self.users = json.load(f)

    def db_save(self, name, value):
        with self.lock:
            with open(name, 'w', encoding='utf-8') as f:
                json.dump(value, f, indent=2)

    def db_save_all(self):
        with self.lock:
            with open(USERS, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2)
        return True

    def get_user_information(self, user):
        user = self.users[user]
        return {
            'user': user,
            'user_rights': user['user_rights'],
            'user_id': user['user_id'],
            'user_stat': user['user_stat']
        }

    def get_user_id_information(self, user_id):
        for user in self.users:
            if self.users[user]['user_id'] == user_id:
                return self.get_user_information(user)

    def give_score(self, user, score=1):
        with self.lock:
            if score == -1:
                user.user_stat[1] += 1
            else:
                user.user_stat[0] += score
            if (user.user_stat[1] > 10) \
                    and (user.user_stat[0] / user.user_stat[1] > 0.5) and (user.user_rights == 1):
                user.user_rights = 2
            elif user.user_rights == 2:
                user.user_rights = 1
        self.db_save_all()
