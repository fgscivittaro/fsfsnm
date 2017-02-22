
# touch data.db
# sqlite3 data.db
# -- delete the players table
# DROP TABLE players 

## figure out how to update the table
CREATE TABLE players(
  name VARCHAR (255),
  team VARCHAR (255),
  G VARCHAR (255),
  PA VARCHAR (255),
  HR VARCHAR (255),
  R VARCHAR (255),
  RBI VARCHAR (255),
  SB VARCHAR (255),
  BBPer VARCHAR (255),
  KPer VARCHAR (255),
  ISO VARCHAR (255),
  BABIP VARCHAR (255),
  AVG VARCHAR (255),
  OBP VARCHAR (255),
  SLG VARCHAR (255),
  wOBA VARCHAR (255),
  wRCPlus VARCHAR (255),
  BSR VARCHAR (255),
  Off VARCHAR (255),
  Def VARCHAR (255),
  WAR VARCHAR (255)
  AB VARCHAR (255),
  PA VARCHAR (255),
  H VARCHAR (255),
  1B VARCHAR (255),
  2B VARCHAR (255),
  3B VARCHAR (255),
  HR VARCHAR (255),
  R VARCHAR (255),
  RBI VARCHAR (255),
  BB VARCHAR (255),
  IBB VARCHAR (255),
  SO VARCHAR (255),
  HBP VARCHAR (255),
  SF VARCHAR (255),
  SH VARCHAR (255),
  GDP VARCHAR (255),
  SB VARCHAR (255),
  CS VARCHAR (255),
  AVG VARCHAR (255)
  id INTEGER PRIMARY KEY,
);

#'AB','PA','H','1B','2B','3B','HR','R','RBI','BB','IBB','SO','HBP','SF','SH','GDP','SB','CS','AVG']
# Name,Team,G,PA,HR,R,RBI,SB,BBPer,KPer,ISO,BABIP,AVG,OBP,SLG,wOBA,wRCPlus,BSR,Off,Def,WAR

select * from players;

select * from players where id = 1;

playerid=(\d*)