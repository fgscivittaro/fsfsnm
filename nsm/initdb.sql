DROP TABLE players;
DROP TABLE data;

CREATE TABLE players
            (id int, ispitcher boolean)


CREATE TABLE data
             (id int, name text, team text, g int, ab int, pa int,
             h int,singles int, doubles int, triples int, homerun int, 
             runs int, runs_batted_in int,
             bb int, ibb int, so int, hbp int, sf int, sh int, gdp int,
             sb int, cs int, avg int, shift boolean, noshift boolean, 
             trad_shift boolean, nontrad_shift boolean);




