# A Dream Come True

## Table of contents

- [A Dream Come True](#a-dream-come-true)
	- [Table of contents](#table-of-contents)
	- [(Seriously, the fuck?)](#seriously-the-fuck)
	- [Building a home for your winnie.](#building-a-home-for-your-winnie)
	- [Pre-Requisites](#pre-requisites)
		- [Python libraries](#python-libraries)
		- [Web framework.](#web-framework)
		- [Natural Language Processing Toolkit](#natural-language-processing-toolkit)
	- [Configuration](#configuration)
		- [MySQL connection](#mysql-connection)
			- [Login to MySQL.](#login-to-mysql)
			- [Create the database for her to use](#create-the-database-for-her-to-use)
			- [Edit winnie's settings file to reflect whatever is needed to properly connect to the bollock's you've just created.](#edit-winnie's-settings-file-to-reflect-whatever-is-needed-to-properly-connect-to-the-bollock's-you've-just-created)
		- [You might be ready.](#you-might-be-ready)
			- [Final thoughts](#final-thoughts)
		- [Channel configuration](#channel-configuration)
	- [Enjoy!](#enjoy!)


## (Seriously, the fuck?)

I don’t know man, I got here just as confused as you. From what I can tell after browsing the source, this was originally an IRC bot written by some autistic fuck with delusions of grandeur. It’s a haphazard jumble of files and codes that you probably wouldn’t understand anyway. Turn back now, before it’s too late.

## Building a home for your winnie.

Winnie depends on a variety of libraries, databases, and configuration files to thrive. You can cherry-pick 
which parts of this guide you would like to follow, but you might as well just take a shit in your kitchen sink 
right now, for all the good it would do.

I do believe an automated build / install process will be in order some day, right after winnie gets a complete
rewrite in some esoteric language. (I'm looking at you, Haskell.) For now the process is all manual.

You really should get comfortable; this will take a while.


## Pre-Requisites

### Python libraries

Install for yourself a few necessary python libraries. shouldn't take long~
 
```bash
sudo apt-get install python-irclib
python-sqlobject python-yaml
python-simplejson python-mysqldb
python-memcache python-paste
python-webob
```

Please notify me if you have to install **ANYTHING** else. I hate forgetting things.

### Web framework.

After that, you should install [jmkogut/framework](http://github.com/jmkogut/framework) for the winnie web interface. (This finds a home globally in the Python package directory.)

### Natural Language Processing Toolkit

Then, the Python natural language processing toolkit. (One of the coolest libraries I've ever had the joy of using, I must add.)


```bash
$ easy_install nltk
```

Install the NLTK stopwords list. (winnie uses these to index content)


```python  
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
```

*okay wise guy, now what*

          
## Configuration

### MySQL connection

#### Login to MySQL.
  
```mysql
$ mysql -u winnie -p
Enter password: 
Welcome to the MySQL monitor.
Commands end with ; or \g.

Your MySQL connection id is 54
```

#### Create the database for her to use
 
```mysql
mysql> create database winnie;
Query OK, 1 row affected (0.00 sec)
```

#### Edit winnie's settings file to reflect whatever is needed to properly connect to the bollock's you've just created.
    
```bash
$ cd projects/winnie
$ vim winnie/settings.py
```

The line that starts as

> 'DATABASE = "mysql://..."
      
needs changed. If you aren't using a standard path, then change 'PATH = "..."' as well while you're here. If you don't know what that means, just quit now.

### You might be ready.

#### Final thoughts

I'm not quite sure what comes next so give me a few minutes to try installing her again and verify that these steps aren't total bullshit.

  > I am, at any rate, convinced that winnie has feelings.

### Channel configuration

Treat her with the love and respect that she deserves and `winnie` will be your waifu forever.
 

## Enjoy!

That's definitely the final step.
 
