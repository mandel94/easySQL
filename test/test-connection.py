import os

import mysql.connector
from easySQL.mysql.connect import establish_connection
from easySQL.mysql.connect import APIConnection

config = {"user": os.environ.get("MYSQLUSER"),
          "password": os.environ.get("MYSQLUSERPSSWD"),
          "database": "nba"}

api = APIConnection(**config)

api.show_tables()
api.drop_tables("player", "season", if_exists=False)

table_def = {}
table_def["stat"] = 'CREATE TABLE stat \
         (stat_id INT UNSIGNED NOT NULL, \
          player_id VARCHAR(15), \
          player_name VARCHAR(30), \
          ranker TINYINT UNSIGNED, \
          game_season TINYINT UNSIGNED, \
          date_game DATE, \
          season CHAR(7), \
          age TINYINT UNSIGNED, \
          team_id CHAR(3), \
          game_location ENUM("Home", "Away"), \
          opp_id CHAR(3), \
          net_score SMALLINT SIGNED, \
          win_loss ENUM("W", "L"), \
          gs BOOLEAN, \
          mp TIME, \
          fg TINYINT UNSIGNED, \
          fga TINYINT UNSIGNED, \
          fg_pct FLOAT(4, 3), \
          fg3 TINYINT UNSIGNED, \
          fg3a TINYINT UNSIGNED,\
          fg3_pct FLOAT(4, 3), \
          ft TINYINT UNSIGNED, \
          fta TINYINT UNSIGNED,\
          ft_pct FLOAT(4, 3), \
          orb TINYINT UNSIGNED, \
          drb TINYINT UNSIGNED, \
          trb TINYINT UNSIGNED, \
          ast TINYINT UNSIGNED, \
          stl TINYINT UNSIGNED, \
          blk TINYINT UNSIGNED, \
          tov TINYINT UNSIGNED, \
          pf TINYINT UNSIGNED,\
          pts TINYINT UNSIGNED, \
          game_score FLOAT(4, 1), \
          plus_minus TINYINT SIGNED, \
          CONSTRAINT pk_stat PRIMARY KEY (player_id) \
          );'
table_def["player"] = 'CREATE TABLE player \
         (player_id VARCHAR(15) NOT NULL, \
          name VARCHAR(25), \
          field_position VARCHAR(30), \
          height SMALLINT UNSIGNED, \
          weight SMALLINT UNSIGNED, \
          experience TINYINT UNSIGNED, \
          country VARCHAR(20), \
          CONSTRAINT pk_player PRIMARY KEY (player_id) \
          );'
table_def["season"] = 'CREATE TABLE season \
         (season_id CHAR(7) NOT NULL, \
          league CHAR(3), \
          champion VARCHAR(30), \
          most_valuable_player VARCHAR(15), \
          rookie_of_the_year VARCHAR(15), \
          leader_in_points_scored VARCHAR(15), \
          leader_in_total_rebounds VARCHAR(15), \
          leader_in_assists VARCHAR(15), \
          leader_in_win_shares VARCHAR(15), \
          CONSTRAINT pk_season PRIMARY KEY (season_id), \
          CONSTRAINT fk_season_mvp FOREIGN KEY (most_valuable_player) \
              REFERENCES player (player_id), \
          CONSTRAINT fk_season_rookyear FOREIGN KEY (rookie_of_the_year) \
              REFERENCES player (player_id), \
          CONSTRAINT fk_season_leadpoints FOREIGN KEY (leader_in_points_scored) \
              REFERENCES player (player_id), \
          CONSTRAINT fk_season_leadrebs FOREIGN KEY (leader_in_total_rebounds) \
              REFERENCES player (player_id), \
          CONSTRAINT fk_season_leadassist FOREIGN KEY (leader_in_assists) \
              REFERENCES player (player_id), \
          CONSTRAINT fk_season_leadwin FOREIGN KEY (leader_in_win_shares) \
              REFERENCES player (player_id) \
          );'
for tbl in table_def.keys():
    api.create_table(table_def[tbl])

api.show_tables()






