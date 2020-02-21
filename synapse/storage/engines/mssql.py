# -*- coding: utf-8 -*-
# Copyright 2015, 2016 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct
import threading


class MSSqlEngine(object):
    single_threaded = True

    def __init__(self, database_module, database_config):
        self.module = database_module

        self._current_state_group_id = None
        self._current_state_group_id_lock = threading.Lock()

    def check_database(self, db_conn, allow_outdated_version: bool = False):
        pass

    def check_new_database(self, txn):
        """Gets called when setting up a brand new database. This allows us to
        apply stricter checks on new databases versus existing database.
        """

    def convert_param_style(self, sql):
        return sql.replace("%s", "?")

    def on_new_connection(self, db_conn):
        pass

    @property
    def can_native_upsert(self):
        """
        Do we support native UPSERTs? This requires SQLite3 3.24+, plus some
        more work we haven't done yet to tell what was inserted vs updated.
        """
        return False

    @property
    def supports_tuple_comparison(self):
        """
        Do we support comparing tuples, i.e. `(a, b) > (c, d)`? This requires
        SQLite 3.15+.
        """
        return False

    @property
    def supports_using_any_list(self):
        """Do we support using `a = ANY(?)` and passing a list
        """
        return False

    def is_deadlock(self, error):
        return False

    def is_connection_closed(self, conn):
        return False

    def lock_table(self, txn, table):
        return

    def get_next_state_group_id(self, txn):
        """Returns an int that can be used as a new state_group ID
        """
        # We do application locking here since if we're using sqlite then
        # we are a single process synapse.
        with self._current_state_group_id_lock:
            if self._current_state_group_id is None:
                txn.execute("SELECT COALESCE(max(id), 0) FROM state_groups")
                self._current_state_group_id = txn.fetchone()[0]

            self._current_state_group_id += 1
            return self._current_state_group_id

    @property
    def server_version(self):
        """Gets a string giving the server version. For example: '3.22.0'

        Returns:
            string
        """
        return 100500
