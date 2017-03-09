DROP TABLE regular_data;
DROP TABLE batted_ball_data;
DROP TABLE marcel;
DROP TABLE regression;

CREATE TABLE marcel
              (id int primary key, player_id int,name text,year text,age text,g int,ab int,
                pa int,h int,singles int,doubles int,triples int,homerun int,
                runs int,runs_batted_in int,bb int,ibb int,so int,hbp int,sf int,
                sh int,gdp int,sb int,cs int,avg int,obp int,slg int,woba int);

CREATE TABLE regression
              (id int primary key,name text,player_id int,team text,avg_distance int,
                k_rate int,bb_rate int,avg_exit_vel int,barrels_per_bbe int,
                LD_per int,x_wOBA,year int);

CREATE TABLE regular_data
             (id int primary key, player_id int, name text, team text, g int, ab int, pa int,
             h int,singles int, doubles int, triples int, homerun int, 
             runs int, runs_batted_in int,
             bb int, ibb int, so int, hbp int, sf int, sh int, gdp int,
             sb int, cs int, avg int, shift boolean, noshift boolean, 
             trad_shift boolean, nontrad_shift boolean, year text);

CREATE TABLE batted_ball_data
             (id int primary key, player_id int, name text, team text, babip int, gb_fb int, ld_per int,
              gb_per int, fb_per int, iffb_per int, hr_fb int, ifh int, ifhper int, 
              buh int, buh_per int, pull_per int, cent_per int, oppo_per int,
              soft_per int, med_per int, hard_per int, year text);


CREATE INDEX marcel_player_id ON marcel (player_id);
CREATE INDEX regression_player_id ON regression (player_id);
CREATE INDEX regular_data_player_id ON regular_data (player_id);
CREATE INDEX batted_ball_data_player_id ON batted_ball_data (player_id);
