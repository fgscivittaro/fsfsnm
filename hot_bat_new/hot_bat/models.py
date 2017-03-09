# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    username = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Marcel(models.Model):
    id = models.IntegerField(primary_key=True)
    player_id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    age = models.TextField(blank=True, null=True)
    g = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    singles = models.IntegerField(blank=True, null=True)
    doubles = models.IntegerField(blank=True, null=True)
    triples = models.IntegerField(blank=True, null=True)
    homerun = models.IntegerField(blank=True, null=True)
    runs = models.IntegerField(blank=True, null=True)
    runs_batted_in = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    ibb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    avg = models.IntegerField(blank=True, null=True)
    obp = models.IntegerField(blank=True, null=True)
    slg = models.IntegerField(blank=True, null=True)
    woba = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{}, {}'.format(self.name, self.year)

    class Meta:
        managed = False
        db_table = 'marcel'


class Regression(models.Model):
    id = models.IntegerField(primary_key=True)
    player_id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    team = models.TextField(blank=True, null=True)
    avg_distance = models.IntegerField(blank=True, null=True)
    k_rate = models.IntegerField(blank=True, null=True)
    bb_rate = models.IntegerField(blank=True, null=True)
    avg_exit_vel = models.IntegerField(blank=True, null=True)
    barrels_per_bbe = models.IntegerField(blank=True, null=True)
    ld_per = models.IntegerField(db_column='LD_per', blank=True, null=True)  # Field name made lowercase.
    x_woba = models.TextField(db_column='x_wOBA', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{}, {}'.format(self.name, self.year)

    class Meta:
        managed = False
        db_table = 'regression'


class RegularData(models.Model):
    id = models.IntegerField(primary_key=True)
    player_id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    team = models.TextField(blank=True, null=True)
    g = models.IntegerField(blank=True, null=True)
    ab = models.IntegerField(blank=True, null=True)
    pa = models.IntegerField(blank=True, null=True)
    h = models.IntegerField(blank=True, null=True)
    singles = models.IntegerField(blank=True, null=True)
    doubles = models.IntegerField(blank=True, null=True)
    triples = models.IntegerField(blank=True, null=True)
    homerun = models.IntegerField(blank=True, null=True)
    runs = models.IntegerField(blank=True, null=True)
    runs_batted_in = models.IntegerField(blank=True, null=True)
    bb = models.IntegerField(blank=True, null=True)
    ibb = models.IntegerField(blank=True, null=True)
    so = models.IntegerField(blank=True, null=True)
    hbp = models.IntegerField(blank=True, null=True)
    sf = models.IntegerField(blank=True, null=True)
    sh = models.IntegerField(blank=True, null=True)
    gdp = models.IntegerField(blank=True, null=True)
    sb = models.IntegerField(blank=True, null=True)
    cs = models.IntegerField(blank=True, null=True)
    avg = models.IntegerField(blank=True, null=True)
    shift = models.NullBooleanField()
    noshift = models.NullBooleanField()
    trad_shift = models.NullBooleanField()
    nontrad_shift = models.NullBooleanField()
    year = models.TextField(blank=True, null=True)

    def find_type(self):
        '''
        Find which type of shift is being used on the instance of the player's
        data.
        '''

        type_shift = 'Overall'

        if self.shift==True:
            type_shift = 'Shift'
        elif self.noshift==True:
            type_shift = 'No Shift'
        elif self.trad_shift==True:
            type_shift = 'Traditional Shift'
        elif self.nontrad_shift==True:
            type_shift = 'Non-Traditional Shift'

        return type_shift

    def __str__(self):
        return '{}, {}, {}'.format(self.name, self.find_type(), self.year)

    class Meta:
        managed = False
        db_table = 'regular_data'
        verbose_name_plural = 'Regular Data'


class BattedBallData(models.Model):
    id = models.IntegerField(primary_key=True)
    player_id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    team = models.TextField(blank=True, null=True)
    babip = models.IntegerField(blank=True, null=True)
    gb_fb = models.IntegerField(blank=True, null=True)
    ld_per = models.IntegerField(blank=True, null=True)
    gb_per = models.IntegerField(blank=True, null=True)
    fb_per = models.IntegerField(blank=True, null=True)
    iffb_per = models.IntegerField(blank=True, null=True)
    hr_fb = models.IntegerField(blank=True, null=True)
    ifh = models.IntegerField(blank=True, null=True)
    ifhper = models.IntegerField(blank=True, null=True)
    buh = models.IntegerField(blank=True, null=True)
    buh_per = models.IntegerField(blank=True, null=True)
    pull_per = models.IntegerField(blank=True, null=True)
    cent_per = models.IntegerField(blank=True, null=True)
    oppo_per = models.IntegerField(blank=True, null=True)
    soft_per = models.IntegerField(blank=True, null=True)
    med_per = models.IntegerField(blank=True, null=True)
    hard_per = models.IntegerField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}, {}'.format(self.name, self.year)

    class Meta:
        managed = False
        db_table = 'batted_ball_data'
        verbose_name_plural = 'Batted Ball Data'