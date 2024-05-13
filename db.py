import sqlite3
import cleaner


class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    async def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    async def event_exists(self, event_id):
        result = self.cursor.execute("SELECT `DD` FROM `events` WHERE `q_id` = ?", (event_id,))
        return bool(len(result.fetchall()))

    async def sid_exists(self, user_id):
        result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    async def user_banned(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `banned` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    async def add_user(self, user_id, ):
        self.cursor.execute("INSERT INTO `users` (user_id) VALUES (?)", (user_id,))
        return self.conn.commit()

    async def add_fio(self, user_id, name, surname):
        self.cursor.execute("UPDATE `users` SET `name` = ? WHERE `user_id` = ?",
                            (name, user_id,))
        self.cursor.execute("UPDATE `users` SET `surname` = ? WHERE `user_id` = ?",
                            (surname, user_id,))
        return self.conn.commit()

    async def get_fio(self, user_id):
        name = str(self.cursor.execute("SELECT `name` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall())
        surname = str(self.cursor.execute("SELECT `surname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall())
        result = surname + " " + name
        result = cleaner.remove_special_characters(result)
        return result

    async def get_id(self, user_id):
        id = str(self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall())
        id = cleaner.remove_special_characters(id)
        return id

    async def get_sid(self, user_id):
        id = str(self.cursor.execute("SELECT `user_id` FROM `users` WHERE `id` = ?", (user_id,)).fetchall())
        id = cleaner.remove_special_characters(id)
        return id

    async def is_admin(self, user_id):
        result = str(self.cursor.execute("SELECT `is_admin` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def change_name(self, user_id, name):
        self.cursor.execute("UPDATE `users` SET `name` = ? WHERE `user_id` = ?", (name, user_id,))
        return self.conn.commit()

    async def change_surname(self, user_id, name):
        self.cursor.execute("UPDATE `users` SET `surname` = ? WHERE `user_id` = ?", (name, user_id,))
        return self.conn.commit()

    async def change_admin_status(self, user_id, lvl):
        self.cursor.execute("UPDATE `users` SET `is_admin` = ? WHERE `user_id` = ?", (lvl, user_id,))
        return self.conn.commit()

    async def change_soldout(self, g_id, new_num):
        self.cursor.execute("update `events` set `soldout`=? where `q_id`=?", (new_num, g_id,))
        return self.conn.commit()

    async def ban_user(self, user_id, reason, admin):
        self.cursor.execute("INSERT INTO `banned` (user_id,reason,admin) VALUES (?,?,?)", (user_id, reason, admin,))
        return self.conn.commit()

    async def get_reason(self, user_id):
        result = str(self.cursor.execute("SELECT `reason` FROM `banned` WHERE `user_id` = ?", (user_id,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def get_q_id(self, normal_id):
        result = str(self.cursor.execute("SELECT `admin` FROM `banned` WHERE `user_id` = ?", (user_id,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def get_admin(self, user_id):
        result = str(self.cursor.execute("SELECT `admin` FROM `banned` WHERE `user_id` = ?", (user_id,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def unban(self, user_id):
        self.cursor.execute("DELETE FROM `banned` WHERE `user_id` = ?", (user_id,))
        return self.conn.commit()

    async def get_users(self):
        result = str(self.cursor.execute("SELECT `user_id` FROM `users`").fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def get_events(self):
        result = str(self.cursor.execute("SELECT `q_id` FROM `events` WHERE `is_active` = ?", (1,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def get_event_name(self, event_id):
        result = str(self.cursor.execute("SELECT `eventname` FROM `events` WHERE `q_id` = ?", (event_id,)).fetchall())

        return result

    async def get_soldout(self, event_id):
        not_sold = str(self.cursor.execute("SELECT `soldout` FROM `events` WHERE `q_id` = ?", (event_id,)).fetchall())
        not_sold = cleaner.remove_special_characters(not_sold)
        return not_sold

    async def get_event_date(self, event_id):
        dd = str(self.cursor.execute("SELECT `DD` FROM `events` WHERE `q_id` = ?", (event_id,)).fetchall())
        mm = str(self.cursor.execute("SELECT `MM` FROM `events` WHERE `q_id` = ?", (event_id,)).fetchall())
        yy = str(self.cursor.execute("SELECT `YYYY` FROM `events` WHERE `q_id` = ?", (event_id,)).fetchall())
        dd = cleaner.remove_special_characters(dd)
        mm = cleaner.remove_special_characters(mm)
        yy = cleaner.remove_special_characters(yy)
        result = dd + "." + mm + "." + yy
        return result

    async def add_event(self, eventname, desc, url, q_id, DD, MM, YYYY, HH, min):
        self.cursor.execute(
            "INSERT INTO `events` (eventname, desc,url, q_id, soldout, DD, MM, YYYY, HH, min, is_active) VALUES (?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (eventname, desc, url, q_id, 0, DD, MM, YYYY, HH, min, 1))
        return self.conn.commit()

    async def get_soldout(self, event_id):
        soldout = str(self.cursor.execute("SELECT `soldout` FROM `events` WHERE `q_id`=?", (event_id,)).fetchall())
        soldout = cleaner.remove_special_characters(soldout)
        return soldout

    async def get_desc(self, event_id):
        desc = str(self.cursor.execute("SELECT `desc` FROM `events` WHERE `q_id`=?", (event_id,)).fetchall())
        desc = desc[3:-4]
        desc = desc.replace("\\n", "\n")
        desc = desc.replace("\\", " ")
        return desc

    async def get_event_id(self, eventname):
        id = str(self.cursor.execute("SELECT `id` FROM `events` WHERE `eventname` = ?", (eventname,)).fetchall())
        id = cleaner.remove_special_characters(id)
        return id

    async def get_event_img(self, event_id):
        img = str(self.cursor.execute("SELECT `url` FROM `events` WHERE `q_id` = ?", (event_id,)).fetchall())
        img = img[3:-4]
        return img

    async def get_event_time(self, event_id):
        hh = str(self.cursor.execute("SELECT `HH` FROM `events` WHERE `q_id` = ?", (event_id,)).fetchall())
        minutes = str(self.cursor.execute("SELECT `min` FROM `events` WHERE `q_id` = ?", (event_id,)).fetchall())
        hh = cleaner.remove_special_characters(hh)
        minutes = cleaner.remove_special_characters(minutes)
        result = hh + ":" + minutes
        return result

    async def delevent(self, event_id):
        self.cursor.execute("DELETE FROM `events` WHERE `q_id` = ?", (event_id,))
        return self.conn.commit()

    async def add_event_count(self, user_id):
        self.cursor.execute("UPDATE `users` SET `events` = events + ? WHERE `user_id` = ?", (1, user_id,))
        return self.conn.commit()

    async def set_stuff(self, user_id, new):
        self.cursor.execute("UPDATE `users` SET `is_stuff` = ? WHERE `user_id` = ?", (new, user_id,))
        return self.conn.commit()

    async def get_stuff(self):
        result = str(self.cursor.execute("SELECT `user_id` FROM `users` WHERE `is_stuff` = ?", (1,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def set_cur_prom(self, user_id, new):
        self.cursor.execute("UPDATE `users` SET `is_cur_prom` = ? WHERE `user_id` = ?", (new, user_id,))
        return self.conn.commit()

    async def set_cur_piar(self, user_id, new):
        self.cursor.execute("UPDATE `users` SET `is_cur_piar` = ? WHERE `user_id` = ?", (new, user_id,))
        return self.conn.commit()

    async def set_is_prom(self, user_id, new):
        self.cursor.execute("UPDATE `users` SET `is_prom` = ? WHERE `user_id` = ?", (new, user_id,))
        return self.conn.commit()

    async def set_is_piar(self, user_id, new):
        self.cursor.execute("UPDATE `users` SET `is_piar` = ? WHERE `user_id` = ?", (new, user_id,))
        return self.conn.commit()

    async def is_cur_prom(self, user_id):
        result = str(
            self.cursor.execute("SELECT `is_cur_prom` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def is_cur_piar(self, user_id):
        result = str(
            self.cursor.execute("SELECT `is_cur_piar` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def is_prom(self, user_id):
        result = str(
            self.cursor.execute("SELECT `is_prom` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def get_cur_prom(self):
        result = str(self.cursor.execute("SELECT `user_id` FROM `users` WHERE `is_cur_prom` = ?", (1,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def get_cur_piar(self):
        result = str(self.cursor.execute("SELECT `user_id` FROM `users` WHERE `is_cur_piar` = ?", (1,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def get_piar(self):
        result = str(self.cursor.execute("SELECT `user_id` FROM `users` WHERE `is_piar` = ?", (1,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def get_prom(self):
        result = str(self.cursor.execute("SELECT `user_id` FROM `users` WHERE `is_prom` = ?", (1,)).fetchall())
        result = cleaner.remove_special_characters(result)
        return result

    async def get_group(self, user_id):
        admin = str(self.cursor.execute("SELECT `is_admin` from `users` where `user_id` = ?", (user_id,)).fetchall())
        cur_prom = str(
            self.cursor.execute("SELECT `is_cur_prom` from `users` where `user_id` = ?", (user_id,)).fetchall())
        cur_piar = str(
            self.cursor.execute("SELECT `is_cur_piar` from `users` where `user_id` = ?", (user_id,)).fetchall())
        roles = cleaner.remove_special_characters(admin + cur_prom + cur_piar)
        roles = int(str(roles.index("1"))) + 1
        return roles

    async def create_giveaway(self, name, link):
        self.cursor.execute(
            "INSERT INTO `giveaways` (giveaway_name, giveaway_link) VALUES (?, ?)",
            (name, link,))
        return self.conn.commit()

    async def get_giveaways(self):
        giveaways = str(self.cursor.execute("SELECT `giveaway_id` FROM `giveaways`", ).fetchall())
        result = cleaner.remove_special_characters(giveaways)
        return result

    async def get_giveaway_name(self, giveaway_id):
        giveaway = str(self.cursor.execute("SELECT `giveaway_name` FROM `giveaways` WHERE `giveaway_id` = ?",
                                           (giveaway_id,)).fetchall())
        return giveaway

    async def get_giveaway_link(self, giveaway_id):
        giveaway_link = str(self.cursor.execute("SELECT `giveaway_link` FROM `giveaways` WHERE `giveaway_id` = ?",
                                                (giveaway_id,)).fetchall())
        giveaway_link = giveaway_link[3:-4]
        return giveaway_link

    async def delete_giveaway(self, giveaway_id):
        self.cursor.execute("DELETE FROM `giveaways` WHERE `giveaway_id` = ?", (giveaway_id,))
        return self.conn.commit()

    async def giveaway_exist(self, giveaway_id):
        result = self.cursor.execute("SELECT `giveaway_name` FROM `giveaways` WHERE `giveaway_id` = ?", (giveaway_id,))
        return bool(len(result.fetchall()))

    async def add_giveaway(self, giveaway_name, giveaway_link):
        self.cursor.execute(
            "INSERT INTO `giveaways` (giveaway_name, giveaway_link) VALUES (?, ?)",
            (giveaway_name, giveaway_link))
        return self.conn.commit()
