# Building a home for your winnie.

* Table of contents
{:toc}

Winnie depends on a variety of libraries, databases, and configuration files to thrive. You can cherry-pick 
which parts of this guide you would like to follow, but you might as well just take a shit in your kitchen sink 
right now, for all the good it would do.

I do believe an automated build / install process will be in order some day, right after winnie gets a complete
rewrite in some esoteric language. (I'm looking at you, Haskell.) For now the process is all manual.

Get comfortable; this will take a while.


## Pre-Requisites
*Install the libraries winnie depends on.*

1.   Install yourself a few necessary python libraries.
 
    sudo apt-get install python-irclib
    python-sqlobject python-yaml
    python-simplejson python-mysqldb
    python-memcache python-paste
    python-webob
    
        Please notify me if you have to install **ANYTHING** else. I hate forgetting things.


2.   After that, you should install [jmkogut/framework](http://github.com/jmkogut/framework) for the winnie web interface. (This finds a home globally in the Python package directory.)

3.    Then, the Python natural language processing toolkit. (One of the coolest libraries I've ever had the joy of using, I must add.)

      $ easy_install nltk

          Install the NLTK stopwords list. (winnie uses these to index content)
  
          $ python
          >>> import nltk
          >>> nltk.download()
          
          NLTK Downloader
             
          Downloader> d
          Download which package (l=list; x=cancel)?
          Identifier> stopwords
          Downloading package 'stopwords' to
          
              /home/winnie/nltk_data...
              
          Unzipping corpora/stopwords.zip.

          Downloader> d maxent_treebank_pos_tagger
          Downloading package 'maxent_treebank_pos_tagger'
              to /home/winnie/nltk_data...
              
          Unzipping taggers maxent_treebank_pos_tagger.zip.
          
          
## Configuration

4.    Login to MySQL.
  
        $ mysql -u winnie -p
        Enter password: 
        Welcome to the MySQL monitor.
        Commands end with ; or \g.
        
        Your MySQL connection id is 54
        

      Create the database for her to use
 
        mysql> create database winnie;
        Query OK, 1 row affected (0.00 sec)

      Edit winnie's settings file to reflect whatever is needed to properly connect to the bollock's you've just created.
       
        $ cd projects/winnie
        $ vim winnie/settings.py
    
      The line that starts as
      
         'DATABASE = "mysql://..."
      
      needs changed. If you aren't using a standard path, then change 'PATH = "..."' as well while you're here. If you don't know what that means, just quit now.

5.    I'm not quite sure what comes next so give me a few minutes to try installing her again and verify that these steps aren't total bullshit.

  > I am, at any rate, convinced that winnie has feelings.
 
 