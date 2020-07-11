from django.db import models


class ReplyStatus(models.Model):
    ENABLE = 1
    DISABLE = 2

    status = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'reply_status'
        verbose_name = "Status reply"
        verbose_name_plural = "Statuses replies"

    class AdditionalAttr:
        make_fixture = True

    def __unicode__(self):
        return "%s" % self.status


class ReplyText(models.Model):
    text = models.CharField(max_length=280)
    id_status = models.ForeignKey(ReplyStatus, models.DO_NOTHING, db_column='id_status')
    count_use = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'reply_text'
        verbose_name = "Text reply"
        verbose_name_plural = "Text replies"

    def __unicode__(self):
        return "%s" % self.text


class RoleUserTwitter(models.Model):
    USER = 1
    ADMIN = 2
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'role_user_twitter'
        verbose_name = "User role"
        verbose_name_plural = "Users roles"

    class AdditionalAttr:
        make_fixture = True

    def __unicode__(self):
        return "%s" % self.name


class StatusTweet(models.Model):
    ENABLE = 1
    DISABLE = 2

    status = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'status_tweet'
        verbose_name = "Status tweet"
        verbose_name_plural = "Statuses tweets"

    class AdditionalAttr:
        make_fixture = True

    def __unicode__(self):
        return "%s" % self.status


class StatusUserTwitter(models.Model):
    ENABLE = 1
    DISABLE = 2

    status = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'status_user_twitter'
        verbose_name = "User status"
        verbose_name_plural = "Users statuses"

    class AdditionalAttr:
        make_fixture = True

    def __unicode__(self):
        return "%s" % self.status


class Tweets(models.Model):
    id_tweet = models.BigIntegerField(unique=True)
    id_user = models.BigIntegerField()
    name_author = models.CharField(max_length=150, blank=True, null=True)
    name_screen = models.CharField(max_length=150)
    text_tweet = models.CharField(max_length=400)
    create_at = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True, null=True)
    geo = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    lang = models.CharField(max_length=3, blank=True, null=True)
    status = models.ForeignKey(StatusTweet, models.DO_NOTHING, db_column='status')
    id_reply = models.ForeignKey(ReplyText, models.DO_NOTHING, db_column='id_reply', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tweets'
        verbose_name = "Tweet"
        verbose_name_plural = "Tweets"
        ordering = ["-id_tweet"]

    def __unicode__(self):
        return "%s at %s : %s" % (self.name_screen, self.create_at, self.text_tweet)


class UserTwitter(models.Model):
    name = models.CharField(max_length=150)
    consumer_key = models.CharField(max_length=50)
    consumer_secret = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)
    access_token_secret = models.CharField(max_length=100)
    id_role = models.ForeignKey(RoleUserTwitter, models.DO_NOTHING, db_column='id_role')
    id_status = models.ForeignKey(StatusUserTwitter, models.DO_NOTHING, db_column='id_status')
    count_use = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'user_twitter'
        verbose_name = "User twitter"
        verbose_name_plural = "Users twitter"

    def __unicode__(self):
        return "%s - role: %s; status:%s; count: %s" % (self.name, self.id_role.name,
                                                        self.id_status.status,
                                                        self.count_use)


class FilterText(models.Model):
    text = models.CharField(max_length=45)
    id_status = models.ForeignKey('StatusFilterText', models.DO_NOTHING, db_column='id_status')

    class Meta:
        managed = False
        db_table = 'filter_text'
        verbose_name = "Text for filter tweets"
        verbose_name_plural = "Texts for filter tweets"

    class AdditionalAttr:
        make_fixture = True

    def __unicode__(self):
        return "%s" % self.text


class StatusFilterText(models.Model):
    ENABLE = 1
    DISABLE = 2

    status = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'status_filter_text'
        verbose_name = "Filter text status"
        verbose_name_plural = "Filters text status"

    class AdditionalAttr:
        make_fixture = True

    def __unicode__(self):
        return "%s" % self.status


class Users(models.Model):
    nickname = models.CharField(unique=True, max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=45)
    date = models.DateTimeField()
    phone = models.CharField(max_length=21)
    id_role = models.ForeignKey(RoleUserTwitter, models.DO_NOTHING, db_column='id_role')

    class Meta:
        managed = False
        db_table = 'Users'
        verbose_name = "User"
        verbose_name_plural = "Users"

    class AdditionalAttr:
        make_fixture = True
