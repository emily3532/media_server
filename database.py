#!/usr/bin/env python3
"""
MediaServer Database module.
Contains all interactions between the webapp and the queries to the database.
"""

import configparser
import json
import sys
from modules import pg8000


################################################################################
#   Welcome to the database file, where all the query magic happens.
#   My biggest tip is look at the *week 8 lab*.
#   Important information:
#       - If you're getting issues and getting locked out of your database.
#           You may have reached the maximum number of connections.
#           Why? (You're not closing things!) Be careful!
#       - Check things *carefully*.
#       - There may be better ways to do things, this is just for example
#           purposes
#       - ORDERING MATTERS
#           - Unfortunately to make it easier for everyone, we have to ask that
#               your columns are in order. WATCH YOUR SELECTS!! :)
#   Good luck!
#       And remember to have some fun :D
################################################################################

#############################
#                           #
# Database Helper Functions #
#                           #
#############################


#####################################################
#   Database Connect
#   (No need to touch
#       (unless the exception is potatoing))
#####################################################

def database_connect():
    """
    Connects to the database using the connection string.
    If 'None' was returned it means there was an issue connecting to
    the database. It would be wise to handle this ;)
    """
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'database' not in config['DATABASE']:
        config['DATABASE']['database'] = config['DATABASE']['user']

    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['database'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as operation_error:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(operation_error)
        return None

    # return the connection to use
    return connection


##################################################
# Print a SQL string to see how it would insert  #
##################################################

def print_sql_string(inputstring, params=None):
    """
    Prints out a string as a SQL string parameterized assuming all strings
    """

    if params is not None:
        if params != []:
            inputstring = inputstring.replace("%s", "'%s'")

    print(inputstring % params)


#####################################################
#   SQL Dictionary Fetch
#   useful for pulling particular items as a dict
#   (No need to touch
#       (unless the exception is potatoing))
#   Expected return:
#       singlerow:  [{col1name:col1value,col2name:col2value, etc.}]
#       multiplerow: [{col1name:col1value,col2name:col2value, etc.}, 
#           {col1name:col1value,col2name:col2value, etc.}, 
#           etc.]
#####################################################

def dictfetchall(cursor, sqltext, params=None):
    """ Returns query results as list of dictionaries."""

    result = []
    if (params is None):
        print(sqltext)
    else:
        print("we HAVE PARAMS!")
        print_sql_string(sqltext, params)

    cursor.execute(sqltext, params)
    cols = [a[0].decode("utf-8") for a in cursor.description]
    print(cols)
    returnres = cursor.fetchall()
    for row in returnres:
        result.append({a: b for a, b in zip(cols, row)})
    # cursor.close()
    return result


def dictfetchone(cursor, sqltext, params=None):
    """ Returns query results as list of dictionaries."""
    # cursor = conn.cursor()
    result = []
    cursor.execute(sqltext, params)
    cols = [a[0].decode("utf-8") for a in cursor.description]
    returnres = cursor.fetchone()
    result.append({a: b for a, b in zip(cols, returnres)})
    return result


#####################################################
#   Query (1)
#   Login
#####################################################

def check_login(username, password):
    """
    Check that the users information exists in the database.
        - True => return the user data
        - False => return None
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below in a manner similar to Wk 08 Lab to log the user in #
        #############################################################################

        sql = """SELECT * from mediaserver.userAccount WHERE username=%s AND password = %s;
        """
        print(username)
        print(password)
        r = dictfetchone(cur, sql, (username, password))
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Is Superuser? - 
#   is this required? we can get this from the login information
#####################################################

def is_superuser(username):
    """
    Check if the user is a superuser.
        - True => Get the departments as a list.
        - False => Return None
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """SELECT isSuper
                 FROM mediaserver.useraccount
                 WHERE username=%s AND isSuper"""
        print("username is: " + username)
        cur.execute(sql, (username))
        r = cur.fetchone()  # Fetch the first row
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (1 b)
#   Get user playlists
#####################################################
def user_playlists(username):
    """
    Check if user has any playlists
        - True -> Return all user playlists
        - False -> Return None
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        ###############################################################################
        # Fill in the SQL below and make sure you get all the playlists for this user #
        ###############################################################################
        sql = """select collection_id, collection_name, count(collection_name)
        from mediaserver.usermediaconsumption 
        natural join mediaserver.mediacollectioncontents 
        natural join mediaserver.mediacollection
        where username = %s
        group by collection_name, collection_id
        """
        print("username is: " + username)
        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting User Playlists:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (1 a)
#   Get user podcasts
#####################################################
def user_podcast_subscriptions(username):
    """
    Get user podcast subscriptions.
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #################################################################################
        # Fill in the SQL below and get all the podcasts that the user is subscribed to #
        #################################################################################

        sql = """select podcast_id, podcast_title, podcast_uri, podcast_last_updated
        from mediaserver.subscribed_podcasts 
        natural join mediaserver.useraccount 
        natural join mediaserver.podcast
        where username = %s"""

        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast subs:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (1 c)
#   Get user in progress items
#####################################################
def user_in_progress_items(username):
    """
    Get user in progress items that aren't 100%
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        ###################################################################################
        # Fill in the SQL below with a way to find all the in progress items for the user #
        ###################################################################################

        sql = """select media_id, play_count, progress, lastviewed, storage_location
        from mediaserver.usermediaconsumption 
        natural join mediaserver.mediacollectioncontents 
        natural join mediaserver.mediacollection
        natural join mediaserver.mediaitem
        where username = %s and progress != 100.00
        """

        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting User Consumption - Likely no values:", sys.exc_info()[0])
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all artists
#####################################################
def get_allartists():
    """
    Get all the artists in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
            a.artist_id, a.artist_name, count(amd.md_id) as count
        from 
            mediaserver.artist a left outer join mediaserver.artistmetadata amd on (a.artist_id=amd.artist_id)
        group by a.artist_id, a.artist_name
        order by a.artist_name;"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Artists:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all songs
#####################################################
def get_allsongs():
    """
    Get all the songs in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
            s.song_id, s.song_title, string_agg(saa.artist_name,', ') as artists
        from 
            mediaserver.song s left outer join 
            (mediaserver.Song_Artists sa join mediaserver.Artist a on (sa.performing_artist_id=a.artist_id)
            ) as saa  on (s.song_id=saa.song_id)
        group by s.song_id, s.song_title
        order by s.song_id"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Songs:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all podcasts
#####################################################
def get_allpodcasts():
    """
    Get all the podcasts in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
                p.*, pnew.count as count  
            from 
                mediaserver.podcast p, 
                (select 
                    p1.podcast_id, count(*) as count 
                from 
                    mediaserver.podcast p1 left outer join mediaserver.podcastepisode pe1 on (p1.podcast_id=pe1.podcast_id) 
                    group by p1.podcast_id) pnew 
            where p.podcast_id = pnew.podcast_id;"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Podcasts:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all albums
#####################################################
def get_allalbums():
    """
    Get all the Albums in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
                a.album_id, a.album_title, anew.count as count, anew.artists
            from 
                mediaserver.album a, 
                (select 
                    a1.album_id, count(distinct as1.song_id) as count, array_to_string(array_agg(distinct ar1.artist_name),', ') as artists
                from 
                    mediaserver.album a1 
			left outer join mediaserver.album_songs as1 on (a1.album_id=as1.album_id) 
			left outer join mediaserver.song s1 on (as1.song_id=s1.song_id)
			left outer join mediaserver.Song_Artists sa1 on (s1.song_id=sa1.song_id)
			left outer join mediaserver.artist ar1 on (sa1.performing_artist_id=ar1.artist_id)
                group by a1.album_id) anew 
            where a.album_id = anew.album_id;"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Albums:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (3 a,b c)
#   Get all tvshows
#####################################################
def get_alltvshows():
    """
    Get all the TV Shows in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all tv shows and episode counts #
        #############################################################################
        sql = """select 
            a.*, (select count(*) from mediaserver.tvshow natural join mediaserver.tvepisode where mediaserver.tvepisode.tvshow_id = a.tvshow_id) as count
        from 
            mediaserver.tvshow a left outer join mediaserver.tvshowmetadata amd on (a.tvshow_id=amd.tvshow_id)
        group by a.tvshow_id
        order by a.tvshow_id;
        """

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all movies
#####################################################
def get_allmovies():
    """
    Get all the Movies in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
            m.movie_id, m.movie_title, m.release_year, count(mimd.md_id) as count
        from 
            mediaserver.movie m left outer join mediaserver.mediaitemmetadata mimd on (m.movie_id = mimd.media_id)
        group by m.movie_id, m.movie_title, m.release_year
        order by movie_id;"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get one artist
#####################################################
def get_artist(artist_id):
    """
    Get an artist by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select *
        from mediaserver.artist a left outer join 
            (mediaserver.artistmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) amd
        on (a.artist_id=amd.artist_id)
        where a.artist_id=%s"""

        r = dictfetchall(cur, sql, (artist_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Artist with ID: '" + artist_id + "'", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (2 a,b,c)
#   Get one song
#####################################################
def get_song(song_id):
    """
    Get a song by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a song    #
        # and the artists that performed it                                         #
        #############################################################################

        #         sql = """select song_title, artist_name, length
        #         from mediaserver.song natural join mediaserver.song_artists natural join mediaserver.artist
        #         where song_id = %s

        sql = """
        SELECT s.song_id, s.song_title, s.length, string_agg(saa.artist_name,', ') as artists
            FROM mediaserver.song s left outer join
            (mediaserver.Song_Artists sa join mediaserver.Artist a on (sa.performing_artist_id = a.artist_id)) as saa
            on (s.song_id = saa.song_id)
            WHERE s.song_id = %s
            GROUP BY s.song_id, s.song_title, s.length
            ORDER BY s.song_id
        """

        r = dictfetchall(cur, sql, (song_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Songs:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (2 d)
#   Get metadata for one song
#####################################################
def get_song_metadata(song_id):
    """
    Get the meta for a song by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all metadata about a song       #
        #############################################################################

        sql = """select song_id, md_type_name, md_value
        from mediaserver.song join mediaserver.mediaitemmetadata on (song_id = media_id) 
        natural join mediaserver.metadata 
        natural join mediaserver.metadatatype
        where song_id = %s
        """

        r = dictfetchall(cur, sql, (song_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting song metadata for ID: " + song_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (6 a,b,c,d,e)
#   Get one podcast and return all metadata associated with it
#####################################################
def get_podcast(podcast_id):
    """
    Get a podcast by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a podcast #
        # including all metadata associated with it                                 #
        #############################################################################
        sql = """SELECT podcast_id, podcast_title, podcast_uri, podcast_last_updated, md_value, md_type_name 
        from mediaserver.Podcast 
        natural join mediaserver.PodcastMetadata
        natural join mediaserver.Metadata 
        natural join mediaserver.metadatatype
        where podcast_id = %s;
        """
        r = dictfetchall(cur, sql, (podcast_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast with ID: " + podcast_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (6 f)
#   Get all podcast eps for one podcast
#####################################################
def get_all_podcasteps_for_podcast(podcast_id):
    """
    Get all podcast eps for one podcast by their podcast ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # podcast episodes in a podcast                                             #
        #############################################################################

        sql = """SELECT media_id, podcast_episode_title, podcast_episode_URI, podcast_episode_published_date, podcast_episode_length
        from mediaserver.PodcastEpisode
        where podcast_id = %s
        order by podcast_episode_published_date DESC;
        """

        r = dictfetchall(cur, sql, (podcast_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Podcast Episodes for Podcast with ID: " + podcast_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (7 a,b,c,d,e,f)
#   Get one podcast ep and associated metadata
#####################################################
def get_podcastep(podcastep_id):
    # ////////////
    # //TODO//
    #
    """
    Get a podcast ep by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a         #
        # podcast episodes and it's associated metadata                             #
        #############################################################################
        sql = """SELECT media_id, podcast_episode_title, podcast_episode_URI, podcast_episode_published_date, podcast_episode_length, md_value, md_type_name
        from mediaserver.PodcastEpisode natural join mediaserver.mediaitemmetadata natural join mediaserver.MetaData natural join mediaserver.metadatatype
        where media_id = %s;
        """

        r = dictfetchall(cur, sql, (podcastep_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast Episode with ID: " + podcastep_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (5 a,b)
#   Get one album
#####################################################
def get_album(album_id):
    """
    Get an album by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about an album  #
        # including all relevant metadata                                           #
        #############################################################################

        sql = """select *
        from mediaserver.album a left outer join 
            (mediaserver.albummetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) amd
        on (a.album_id=amd.album_id)
        where a.album_id=%s"""

        # sql = """select album_title, md_type_name, md_value
        # from mediaserver.mediaitemmetadata join mediaserver.album on (media_id = album_id)
        # natural join mediaserver.metadata
        # natural join mediaserver.metadatatype
        # where album_id = %s
        # """

        r = dictfetchall(cur, sql, (album_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums with ID: " + album_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (5 d)
#   Get all songs for one album
#####################################################
def get_album_songs(album_id):
    """
    Get all songs for an album by the album ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # songs in an album, including their artists                                #
        #############################################################################

        sql = """select al.album_id, als.song_id, als.song_title, als.artists
        from mediaserver.album al left outer join 
            (mediaserver.album_songs natural join 
            (SELECT s.song_id, s.song_title, s.length, string_agg(saa.artist_name,', ') as artists
                FROM mediaserver.song s left outer join
                (mediaserver.Song_Artists sa join mediaserver.Artist a on (sa.performing_artist_id = a.artist_id)) as saa
                on (s.song_id = saa.song_id)
                GROUP BY s.song_id, s.song_title, s.length
                ORDER BY s.song_id) as sa) als on(al.album_id = als.album_id)
        where al.album_id = %s
        """

        r = dictfetchall(cur, sql, (album_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums songs with ID: " + album_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (5 c)
#   Get all genres for one album
#####################################################
def get_album_genres(album_id):
    """
    Get all genres for an album by the album ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # genres in an album (based on all the genres of the songs in that album)   #
        #############################################################################

        sql = """SELECT distinct(alsmd.md_value) as genre
        FROM mediaserver.album al left outer join 
        (mediaserver.album_songs natural join mediaserver.song s join
        (mediaserver.audiomedia natural join mediaserver.mediaitem natural join mediaserver.mediaitemmetadata 
        natural join mediaserver.metadata) smd on(s.song_id = smd.media_id)) alsmd
        on (al.album_id = alsmd.album_id)
        where al.album_id = %s
        order by genre
        """

        r = dictfetchall(cur, sql, (album_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums genres with ID: " + album_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   May require the addition of SQL to multiple 
#   functions and the creation of a new function to
#   determine what type of genre is being provided
#   You may have to look at the hard coded values
#   in the sampledata to make your choices
#####################################################
def define_genre_type(genre):
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = """select md_type_id
            from mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType
			where md_value = %s limit 1"""

        r = dictfetchall(cur, sql, (genre,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Songs with Genre ID: " + genre, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   Get all songs for one song_genre
#####################################################
def get_genre_songs(genre_id):
    """
    Get all songs for a particular song_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # songs which belong to a particular genre_id                               #
        #############################################################################

        sql = """select m.song_id as id, m.song_title as title, 'Song' as type
            from mediaserver.song m left outer join
                (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) mmd
            on (m.song_id=mmd.media_id)
			where md_value =%s
        """

        r = dictfetchall(cur, sql, (genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Songs with Genre ID: " + genre_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   Get all podcasts for one podcast_genre
#####################################################
def get_genre_podcasts(genre_id):
    """
    Get all podcasts for a particular podcast_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # podcasts which belong to a particular genre_id                            #
        #############################################################################
        sql = """
        select m.podcast_id as id , m.podcast_title as title, 'Podcast' as type
            from mediaserver.podcast m left outer join
                (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) mmd
            on (m.podcast_id=mmd.media_id)
			where md_value =%s
        """

        r = dictfetchall(cur, sql, (genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcasts with Genre ID: " + genre_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   Get all movies and tv shows for one film_genre
#####################################################
def get_genre_movies_and_shows(genre_id):
    """
    Get all movies and tv shows for a particular film_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # movies and tv shows which belong to a particular genre_id                 #
        #############################################################################
        sql = """
        select m.movie_id as id, m.movie_title as title, 'Movie' as type
            from mediaserver.movie m left outer join
                (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) mmd
            on (m.movie_id=mmd.media_id)
			where md_value =%s
        """

        r = dictfetchall(cur, sql, (genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Movies and tv shows with Genre ID: " + genre_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (4 a,b)
#   Get one tvshow
#####################################################
def get_tvshow(tvshow_id):
    """
    Get one tvshow in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a tv show #
        # including all relevant metadata       #
        # #############################################################################

        sql = """select *
        FROM mediaserver.tvshow NATURAL JOIN mediaserver.tvshowmetadata
        NATURAL JOIN mediaserver.metadata natural join mediaserver.metadatatype
        where tvshow_id = %s"""
        # sql = """
        # SELECT tvshow_title, md_type_id, md_value
        # FROM mediaserver.tvshow NATURAL JOIN mediaserver.tvshowmetadata
        # NATURAL JOIN mediaserver.metadata
        # WHERE tvshow_id = %s;
        # """

        r = dictfetchall(cur, sql, (tvshow_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (4 c)
#   Get all tv show episodes for one tv show
#####################################################
def get_all_tvshoweps_for_tvshow(tvshow_id):
    """
    Get all tvshow episodes for one tv show in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # tv episodes in a tv show                                                  #
        #############################################################################
        sql = """
        SELECT media_id, tvshow_episode_title, season, episode, air_date
        FROM mediaserver.tvepisode
        WHERE tvshow_id = %s;
        """

        r = dictfetchall(cur, sql, (tvshow_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get one tvshow episode
#####################################################
def get_tvshowep(tvshowep_id):
    """
    Get one tvshow episode in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select * 
        from mediaserver.TVEpisode te left outer join 
            (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) temd
            on (te.media_id=temd.media_id)
        where te.media_id = %s"""

        r = dictfetchall(cur, sql, (tvshowep_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################

#   Get one movie
#####################################################
def get_movie(movie_id):
    """
    Get one movie in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select *
        from mediaserver.movie m left outer join 
            (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) mmd
        on (m.movie_id=mmd.media_id)
        where m.movie_id=%s;"""

        r = dictfetchall(cur, sql, (movie_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Find all matching tvshows
#####################################################
def find_matchingtvshows(searchterm):
    """
    Get all the matching TV Shows in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
            select 
                t.*, tnew.count as count  
            from 
                mediaserver.tvshow t, 
                (select 
                    t1.tvshow_id, count(te1.media_id) as count 
                from 
                    mediaserver.tvshow t1 left outer join mediaserver.TVEpisode te1 on (t1.tvshow_id=te1.tvshow_id) 
                    group by t1.tvshow_id) tnew 
            where t.tvshow_id = tnew.tvshow_id and lower(tvshow_title) ~ lower(%s)
            order by t.tvshow_id;"""

        r = dictfetchall(cur, sql, (searchterm,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (9)
#   Find all matching Movies
#####################################################
def find_matchingmovies(searchterm):
    """
    Get all the matching Movies in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #  
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about movies    #
        # that match a given search term                                            #
        #############################################################################
        sql = """
        select 
            distinct m.movie_id, m.movie_title, m.release_year
        from 
            mediaserver.movie m left outer join mediaserver.mediaitemmetadata mimd on (m.movie_id = mimd.media_id)
	    where lower(m.movie_title) like lower(%s) 
        """

        searchterm = f"%{searchterm}%"

        r = dictfetchall(cur, sql, (searchterm,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Add a new Movie
#####################################################
def add_movie_to_db(title, release_year, description, storage_location, genre):
    """
    Add a new Movie to your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT 
            mediaserver.addMovie(
                %s,%s,%s,%s,%s);
        """

        cur.execute(sql, (storage_location, description, title, release_year, genre))
        conn.commit()  # Commit the transaction
        r = cur.fetchone()
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (8)
#   Add a new Song
#####################################################
def add_song_to_db(title, songlength, description, location, songgenre, artistid):
    """
    Get all the matching Movies in your media server
    """
    #########
    # TODO  #  
    #########

    #############################################################################
    # Fill in the Function  with a query and management for how to add a new    #
    # song to your media server. Make sure you manage all constraints           #
    #############################################################################

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT
            mediaserver.addSong(
                %s,%s,%s,%s,%s,%s);
        """

        cur.execute(sql, (location, description, title, songlength, songgenre, artistid))
        conn.commit()  # Commit the transaction
        r = cur.fetchone()
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding song:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get last Movie
#####################################################
def get_last_movie():
    """
    Get all the latest entered movie in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        select max(movie_id) as movie_id from mediaserver.movie"""

        r = dictfetchone(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


def get_last_song():
    """
    Get all the latest entered movie in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        select max(song_id) as song_id from mediaserver.song"""

        r = dictfetchone(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


# @ param 2d array [[key, search condition], [key2, search condition2]]
# @ return search results

def search_multi_albums(attributes):
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = """SELECT distinct al.album_id as id, al.album_title as title, 'Album' as type
        FROM mediaserver.album al left outer join 
        (mediaserver.album_songs natural join mediaserver.song s natural join 
		 (mediaserver.song_artists sa join mediaserver.artist a on sa.performing_artist_id=a.artist_id) 
		 join
        (mediaserver.audiomedia natural join mediaserver.mediaitem natural join mediaserver.mediaitemmetadata 
        natural join mediaserver.metadata) smd on(s.song_id = smd.media_id)) alsmd
        on (al.album_id = alsmd.album_id)
        WHERE """
        if attributes != None:
            i = 0
            while i < len(attributes) - 1:
                if attributes[i][0] == 'album':
                    sql += f" lower(al.album_title) like '%%{attributes[i][1]}%%' and "
                elif attributes[i][0] == "id":
                    sql += " al.album_id = " + attributes[i][1] + " and "
                elif attributes[i][0] == "song":
                    sql += f" lower(alsmd.song_title) like '%%{attributes[i][1]}%%' and "
                elif attributes[i][0] == "artist":
                    sql += f" lower(alsmd.artist_name) like '%%{attributes[i][1]}%%' and "
                elif attributes[i][0] == "genre":
                    sql += f" lower(md_value) like '%%{attributes[i][1]}%%' and "
                i+=1
            if attributes[i][0] == 'album':
                sql += f" lower(al.album_title) like '%%{attributes[i][1]}%%'"
            elif attributes[i][0] == "id":
                sql += " al.album_id = " + attributes[i][1]
            elif attributes[i][0] == "song":
                sql += f" lower(alsmd.song_title) like '%%{attributes[i][1]}%%'"
            elif attributes[i][0] == "artist":
                sql += f" lower(alsmd.artist_name) like '%%{attributes[i][1]}%%'"
            elif attributes[i][0] == "genre":
                sql += f" lower(md_value) like '%%{attributes[i][1]}%%'"


        r = dictfetchall(cur,sql,)
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

def search_multi_songs(attributes):
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = """SELECT distinct alsmd.song_id as id, alsmd.song_title as title, 'Song' as type
		FROM mediaserver.album al left outer join (mediaserver.album_songs natural join mediaserver.song s natural join 
		 (mediaserver.song_artists sa join mediaserver.artist a on sa.performing_artist_id=a.artist_id) 
		 join
        (mediaserver.audiomedia natural join mediaserver.mediaitem natural join mediaserver.mediaitemmetadata 
        natural join mediaserver.metadata) smd on(s.song_id = smd.media_id)) alsmd
        on (al.album_id = alsmd.album_id)
        where"""
        if attributes != None:
            i = 0
            while i < len(attributes) - 1:
                if attributes[i][0] == "song":
                    sql += f" lower(alsmd.song_title) like '%%{attributes[i][1]}%%' and "
                elif attributes[i][0] == 'album':
                    sql += f" lower(al.album_title) like '%%{attributes[i][1]}%%' and "
                elif attributes[i][0] == "length":
                    if "<" or ">" in attributes[i][0]:
                        sql += " alsmd.length " + attributes[i][1] + " and "
                    else:
                        sql += " alsmd.length = " + attributes[i][1]+ " and "
                elif attributes[i][0] == "artist":
                    sql += f" lower(alsmd.artist_id) like '%%{attributes[i][1]}%%' and "
                i+=1
            if attributes[i][0] == "song":
                sql += f" lower(alsmd.song_title) like '%%{attributes[i][1]}%%'"
            elif attributes[i][0] == 'album':
                sql += f" al.album_title like '%%{attributes[i][1]}%%'"
            elif attributes[i][0] == "length":
                if "<" or ">" in attributes[i][0] :
                    sql += " alsmd.length " + attributes[i][1]
                else:
                    sql += " alsmd.length = " + attributes[i][1]
            elif attributes[i][0] == "artist":
                sql += f" lower(alsmd.artist_id) like '%%{attributes[i][1]}%%'"


        r = dictfetchall(cur,sql,)
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None




def search_multi_movies(attributes):
    """
    Get all the matching Movies in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = """
            select distinct m.movie_id as id, m.movie_title as title, m.release_year as year, 'Movie' as type
            from mediaserver.movie m left outer join
                (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) mmd
            on (m.movie_id=mmd.media_id)
            where
        	    """

        if attributes != None:
            i = 0
            while i < len(attributes) - 1:
                if attributes[i][0].lower() == 'genre':
                    sql += f" md_value = '{attributes[i][1]}' and "

                elif attributes[i][0].lower() == 'movie':
                    sql += f" lower(m.movie_title) like '%%{attributes[i][1]}%%' and "

                elif attributes[i][0].lower() == 'year':
                    if '>' or '<' in attributes[i][0]:
                        sql += f"m.release_year {attributes[i][1]} and "
                    else:
                        sql += f"m.release_year == {attributes[i][1]} and "
                i+=1
            if attributes[i][0].lower() == 'genre':
                sql += f" md_value = '{attributes[i][1]}' "

            elif attributes[i][0].lower() == 'movie':
                sql += f" lower(m.movie_title) like '%%{attributes[i][1]}%%'"

            elif attributes[i][0].lower() == 'year':
                if '>' or '<' in attributes[i][0]:
                    sql += f"m.release_year {attributes[i][1]}"
                else:
                    sql += f"m.release_year = {attributes[i][1]}"

        r = dictfetchall(cur,sql,)
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies Shows:", sys.exc_info()[0])
        raise
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None



def search_multi_shows(attributes):
    """
    Get all the matching Movies in your media server
    """

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = """
            select distinct m.tvshow_id as id, m.tvshow_title as title, 'Tv Show' as type, (select count(*) from mediaserver.tvshow natural join mediaserver.tvepisode where mediaserver.tvepisode.tvshow_id = m.tvshow_id) as count, 'Tv Show' as type
            from mediaserver.tvshow m left outer join
                (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) mmd
            on (m.tvshow_id=mmd.media_id)
            where 
        	    """


        if attributes != None:
            i = 0
            while i < len(attributes) - 1:
                if attributes[i][0].lower() == 'genre':
                    sql += f" md_value = '{attributes[i][1]}' and "

                elif attributes[i][0].lower() == 'tvshow':
                    sql += f" lower(m.tvshow_title) like '%%{attributes[i][1]}%%' and "

                elif attributes[i][0].lower() == 'episodes':
                    if '>' or '<' in attributes[i][0]:
                        sql += f"(select count(*) from mediaserver.tvshow natural join mediaserver.tvepisode where mediaserver.tvepisode.tvshow_id = m.tvshow_id) {attributes[i][1]} and "
                    else:
                        sql += f"(select count(*) from mediaserver.tvshow natural join mediaserver.tvepisode where mediaserver.tvepisode.tvshow_id = m.tvshow_id) = {attributes[i][1]} and "
                i+=1
            if attributes[i][0].lower() == 'genre':
                sql += f" md_value = '{attributes[i][1]}' "

            elif attributes[i][0].lower() == 'tvshow':
                sql += f" lower(m.tvshow_title) like '%%{attributes[i][1]}%%' "

            elif attributes[i][0].lower() == 'episodes':
                if '>' or '<' in attributes[i][0]:
                    sql += f"(select count(*) from mediaserver.tvshow natural join mediaserver.tvepisode where mediaserver.tvepisode.tvshow_id = m.tvshow_id) {attributes[i][1]} "
                else:
                    sql += f"(select count(*) from mediaserver.tvshow natural join mediaserver.tvepisode where mediaserver.tvepisode.tvshow_id = m.tvshow_id) = {attributes[i][1]}  "

        r = dictfetchall(cur, sql, )

        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None

def search_multi_podcasts(attributes):
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = """
                select 
                    distinct m.podcast_id as id, m.podcast_title as title, m.podcast_last_updated, 'Podcast' as type
                from mediaserver.podcast m
                join mediaserver.mediaitemmetadata mimd on (m.podcast_id = mimd.media_id)
                natural join mediaserver.metadatatype natural join mediaserver.metadata
                where """

        if attributes != None:
            i = 0
            while i < len(attributes) - 1:
                if attributes[i][0].lower() == 'genre':
                    sql += f" md_value LIKE '%%{attributes[i][1]}%%' and"

                elif attributes[i][0].lower() == 'description':
                    sql += f" md_value like '%%{attributes[i][1]}%%' and "

                elif attributes[i][0].lower() == 'podcast':
                    sql += f" lower(m.podcast_title) like '%%{attributes[i][1]}%%' and "

                elif attributes[i][0].lower() == 'date':
                    if '>' or '<' in attributes[i][0]:
                        sql += f"m.podcast_last_updated {attributes[i][1]} and "
                    else:
                        sql += f"m.podcast_last_updated = {attributes[i][1]} and "
                i+=1
            if attributes[i][0].lower() == 'genre':
                sql += f" md_value LIKE '%%{attributes[i][1]}%%' "

            elif attributes[i][0].lower() == 'description':
                sql += f" md_value like '%%{attributes[i][1]}%%' "

            elif attributes[i][0].lower() == 'podcast':
                sql += f" lower(m.podcast_title) like '%%{attributes[i][1]}%%' "

            elif attributes[i][0].lower() == 'date':
                if '>' or '<' in attributes[i][0]:
                    sql += f"m.podcast_last_updated {attributes[i][1]}' "
                else:
                    sql += f"m.podcast_last_updated = {attributes[i][1]}  "
        r = dictfetchall(cur, sql, )
        # i = 0
        # while i < len(ls) - 1:
        #     sql += "lower(mediaserver.tvshow.tvshow_title) like "
        #     sql += "'%%" + ls[i] + "%%' and "
        #     i += 1
        # sql += "lower(mediaserver.tvshow.tvshow_title) like "
        # sql += "'%%" + ls[len(ls) - 1] + "%%'"
        # sql += " limit 5"
        # r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


def get_multi_search(input):
    # input formatted like [type: condition, type2: condition2, ...]

    #     1. split by comma

    input = input.split(" ")

    splitInput = []

    for x in input:
      currentSplit = x.split(":")
      print(currentSplit)
      if (len(currentSplit) == 1):  # If user hasn't given a key
          currentInput = []
          currentInput.append("no_key")  # make 'no_key' the first input of the tuple
          currentInput.append(currentSplit[0].strip().lower())
          splitInput.append(currentInput)
      elif (len(currentSplit) != 2):
          print("Invalid format.")
      else:
          currentInput = []
          currentInput.append(currentSplit[0].strip().lower())
          currentInput.append(currentSplit[1].strip().lower())
          splitInput.append(currentInput)

    #  instead of returning it should just run the functions ...currentInput

    print(splitInput)
    for attr in splitInput:
        if 'movie' in attr:
            return search_multi_movies(splitInput)
        elif 'tvshow' in attr:
            return search_multi_shows(splitInput)
        elif 'song' in attr:
            return search_multi_songs(splitInput)
        elif 'album' in attr:
            return search_multi_albums(splitInput)
        elif 'podcast' in attr:
            return search_multi_podcasts(splitInput)

def fuzzy_movie(ls):
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # gf
        # ["g", "f", "r"]
        # Try executing the SQL and get from the database
        sql = """select * from mediaserver.movie where """

        i = 0
        while i < len(ls) - 1:
            sql += "lower(mediaserver.movie.movie_title) like "
            sql += f"'%%{ls[i]}%%' and "
            i += 1
        sql += "lower(mediaserver.movie.movie_title) like "
        sql += f"'%%{ls[len(ls) - 1]}%%'"
        sql += " limit 5"
        print(sql)
        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


def fuzzy_tvshow(ls):
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # gf
        # ["g", "f", "r"]
        # Try executing the SQL and get from the database
        sql = """select * from mediaserver.tvshow where """

        i = 0
        while i < len(ls) - 1:
            sql += "lower(mediaserver.tvshow.tvshow_title) like "
            sql += "'%%" + ls[i] + "%%' and "
            i += 1
        sql += "lower(mediaserver.tvshow.tvshow_title) like "
        sql += "'%%" + ls[len(ls) - 1] + "%%'"
        sql += " limit 5"
        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None




#  FOR MARKING PURPOSES ONLY
#  DO NOT CHANGE

def to_json(fn_name, ret_val):
    """
    TO_JSON used for marking; Gives the function name and the
    return value in JSON.
    """
    return {'function': fn_name, 'res': json.dumps(ret_val)}

