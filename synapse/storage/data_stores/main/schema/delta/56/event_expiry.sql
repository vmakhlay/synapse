/* Copyright 2019 The Matrix.org Foundation C.I.C.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

-- CREATE TABLE IF NOT EXISTS event_expiry (
--     event_id TEXT PRIMARY KEY,
--     expiry_ts BIGINT NOT NULL
-- );

IF NOT EXISTS
   (  SELECT [name]
      FROM sys.tables
      WHERE [name] = 'event_expiry'
   )
   CREATE TABLE event_expiry (
        event_id NVARCHAR(4000) PRIMARY KEY,
        expiry_ts BIGINT NOT NULL
   );

CREATE INDEX event_expiry_expiry_ts_idx ON event_expiry(expiry_ts);
