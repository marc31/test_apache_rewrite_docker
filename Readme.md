# Apache mod_rewrite testing

This project is used for easily testing URL rewriting with Apache.
It utilizes the Docker image bitnami/apache.

## Instructions for Usage

### Step 1: Configure Hosts File

Firstly, you need to create an alias in your host file. Open the host file using your preferred text editor. For example:

```bash
sudo vi /etc/hosts
```

Then, add the desired URL alias, such as test.loc, to the host file:

```bash
# /etc/hosts
127.0.0.1 test.loc
```

Save and close the file.

### Step 2: Utilize the Environment

#### Open a terminal and execute the following command to initiate Docker:

```bash
docker compose up
```

This command will launch Docker, including the Apache server.

##### Monitor Apache Logs:

While Docker is running, you can monitor the Apache logs, including the rewrite log, in this terminal.

##### Start Watch Script:

In a separate terminal, execute the watch.sh script to automatically reload the Apache server whenever changes are made to `conf/my_vhost.conf`:

```bash
./watch.sh
```

This script will continuously watch for changes in the specified configuration file and reload Apache accordingly.

##### Implement Changes:

Now, proceed to make changes to the `conf/my_vhost.conf` file as required.

##### Test Changes with Curl:

After applying changes, utilize `curl` commands to verify the expected behavior. Use the following commands to test:

```bash
# curl without following redirection
curl http://test.loc/app/

# curl with following redirection
curl -L http://test.loc/app/

# curl with custom header
curl -H 'Accept-Language: en' http://test.loc/app/
```

Replace http://test.loc/app/ with the appropriate URL you wish to test.

##### Debugging

```conf
# Used for debugging, it displays variables and more
ErrorDocument 404 "Request: %{THE_REQUEST}, Lang: %{ENV:LANG} Referrer: %{HTTP_REFERER} Host: %{HTTP_HOST}"
RewriteRule ^ - [L,R=404]
```

##### Additional Note:

You can also leverage commands from the Makefile to streamline the process:

```bash
# Start Docker
make up

# Start the watch script
make watch
```

## Testing

Run the command

```bash
./tests.py
```

## Resources

Below are several resources related to Apache mod_rewrite and related topics such as logging and .htaccess files:

A helpful video on Apache mod_rewrite
https://www.youtube.com/watch?v=wtkuTRur-_c

The Apache URL Rewriting Guide
http://httpd.apache.org/docs/2.0/misc/rewriteguide.html

A cheatsheet for Mod_Rewrite variables
http://www.askapache.com/htaccess/mod_rewrite-variables-cheatsheet.html

The main documentation for Apache Mod_Rewrite
http://httpd.apache.org/docs/2.4/rewrite/

An introduction to Apache Mod_Rewrite
https://httpd.apache.org/docs/2.4/rewrite/intro.html

Information about Apache logging
http://httpd.apache.org/docs/2.4/mod/core.html#loglevel

Details on Apache mod_rewrite logging
http://httpd.apache.org/docs/2.4/mod/mod_rewrite.html#logging

A guide to .htaccess files
https://www.askapache.com/htaccess-file/htaccess-file/

A regex tester
https://regex101.com/

These resources should be beneficial for learning about and working with
Apache mod_rewrite and associated functionalities

## Docs

### Regex Reminder

| Syntax       | Description                                                      |
| ------------ | ---------------------------------------------------------------- |
| \            | Escape character                                                 |
| .            | Any character                                                    |
| ?            | Any character or absence of this character                       |
| ^            | The string starts with                                           |
| $            | The string ends with                                             |
| \*           | Repeats the previous sequence 0 or more times                    |
| +            | Repeats the previous sequence 1 or more times                    |
| ()           | Capture group allows creating variables called by $1 or $2 or $3 |
| [a-zA-Z0-9_] | equivalent to \w                                                 |
| [0-9]        | equivalent to \d, you can specify \d{1,3} between 1 and 3 times  |

### Base Reminder

RewriteEngine On should be included within an .htaccess file or within specific blocks like VirtualHost, Directory, or Location in the Apache configuration to activate the rewriting engine.

### RewriteRule

The order of rewrite rules is important because they are applied in succession.

RewriteRule Pattern Substitution [flag,...]

Pattern is the input URL that is matched.
Substitution is the replacement or revision to the URL.
By default, the substitution is a file path on the server but can be a URL if specified with the [PT] flag.
Flags like : L (for Last applied rule), R (for redirection means the client url change by default is a 302) are specified in the flag section.
Note that the protocol and the URL are not to be included in the Pattern because it is already known.

```conf
# This rule will be the last applied, and the client url will not change,
# but it will recieve the content from http://anotherurl.com
RewriteRule ^index\.html$ http://anotherurl.com [L]
```

Suppose we have the following folder structure within the web server:

```
www
|--mysite1.com
|   |--index.html
|--mysite2.com
|   |--index.html
```

```conf
# We can write inside .htaccess or inside the VirtualHost of mysite1.com.
# This means if a user goes to http://mysite1.com/foo/1, the URL will not change,
# but the user will see the index.html file from the ./mysite2.com/foo/1 directory.
RewriteRule ^foo/1$ ../mysite2.com/foo/1 [L]

# Same as the previous one.
RewriteRule ^foo/1$ http://mysite2.com/foo/1 [L]

# Without hardcoding the "1" ID of foo.
RewriteRule ^foo/([0-9]+)$ http://mysite2.com/foo/$1 [L]

# Same as the previous one.
RewriteRule ^foo/(\d+)$ http://mysite2.com/foo/$1 [L]

# Without hardcoding "foo" and the ID.
RewriteRule ^([A-Za-z]+)/(\d+)$ http://mysite2.com/$1/$2 [L]
```

In a RewriteRule, the character `-` signifies not to change anything (not to rewrite the URL).

```conf
# If the request corresponds to a file present on the server,
# do not rewrite the URL and do not apply any other rewrite rules (due to the L flag).
# The "^" pattern will catch all URLs.
RewriteCond %{REQUEST_FILENAME} -f
RewriteRule ^ - [L]
```

**Substitution rules can follow each other.**

```conf
# The C flag means continue, and the output of the first
# rule is used as the input of the second.
# if the user request http://mysite1.com/foo/1
# the first rule will be applied and rewrite it to
# http://mysite2.com/products/foo/1
# the second rule will convert the new URL to
# http://mysite2.com/p/foo/1
# in summary :
# http://mysite1.com/foo/1 => http://mysite2.com/products/foo/1 => http://mysite2.com/p/foo/1
# The URL changes in the user's browser because we have the R flag for the second rule.
RewriteRule ^([A-Za-z]+)/(\d+)$ http://mysite2.com/products/$1/$2 [C]
RewriteRule ^products/(.*) http://mysite2.com/p/$1 [L, R]
```

### RewriteCond

RewriteCond is applied one after the other with a logical "and" until the first RewriteRule is found.

RewriteCond StringToTest Regex [flag,...]
StringToTest string or var to test
Regex use to test the StringToTest
flag NC (for no case),... see flag section.

```conf
# Here, HTTP_HOST is a variable that returns www.mysite1.com
# This condition states that if HTTP_HOST starts with www.my followed by any word and then .com, then do something
RewriteCond ${HTTP_HOST} ^www\.my(\w+)\.com$ [NC]

# Now, we add another condition to combine them.
# Here, %1 refers to the first match of the previous condition, which is (\w+)
# If this match is "site2", then apply the next RewriteRule
RewriteCond %1 !^site2$ [NC]

# If the previous condition matches, we apply this rule.
# Note: We could have used %1 to retrieve the match from the first condition
RewriteRule ^([A-Za-z]+)/(\d+)$ http://mysite2.com/$1/$2 [C]
```

**We can use the [OR] flag to combine two conditions.**

```conf
# Checks if the requested filename is not a regular file or a directory.
# it redirects to the 404.html page.
# The [L] flag ensures that no further rules are processed.
RewriteCond %{REQUEST_FILENAME} -f [OR]
RewriteCond %{REQUEST_FILENAME} -d
RewriteRule .* 404.html [L]
```

### How to Set Environment Variables

```conf
# Sets the LANG variable to 'fr'
RewriteRule ^ - [E=LANG:fr]

# If the Accept-Language header starts with 'en',
# sets the LANG variable to 'en'
RewriteCond %{HTTP:Accept-Language} ^en [NC]
RewriteRule ^ - [E=LANG:en]


# Uses the LANG environment variable to rewrite url
RewriteRule ^ %{REQUEST_SCHEME}://%{HTTP_HOST}/app/%{ENV:LANG}/%2 [R,L]
```

### Flags

This list is not exhaustive. For more details, visit https://httpd.apache.org/docs/2.4/rewrite/flags.html

**If the R flag is not specified in a RewriteRule, it will result in an internal redirection, meaning the user won't see any change in the URL in their browser.**

```conf
# [L] : Last ensures that no further rules are processed.
# [END]: Works like [L] but prevents subsequent .htaccess parsing.

# [R] : Redirect 302 - Causes the Apache server to issue a 302 Redirect back to the client.
#        This will show the redirect URL in the client's browser.
# [R=301] : Permanent redirection - This will show the redirect URL in the client's browser.

# [C] : Causes mod_rewrite to concatenate multiple rules together where the output of one rule becomes the input of the next.

# [NC] : Case insensitive matching.

# [F] : 403 Forbidden status code.

# [B] : Causes the RewriteRule to escape non-alphanumeric characters prior to the rewrite transformation.

# [PT] : Causes Apache to treat the RewriteRule substitution string as a URI instead of a file path (which is the default). This flag will cause the RewriteRule to recognize the alias used in the substitution string.*

# [S] The [S] flag is used to skip rules that you don't want to run
```

These flags are used in RewriteRule directives to modify the behavior of Apache's mod_rewrite module. They control aspects like redirection, matching behavior, and transformation of URLs.

### RewriteBase

If the server serves the directory:

```
mysite.com
|--index.html
|--.htaccess
|   |--app
|   |   |--app.html
```

In the .htaccess file at the root of mysite.com:

```conf
# If the user visits http://mysite.com,
# then the file mysite.com/app/app.html will be displayed,
# but the URL will not change.
# Because the substitution pattern is relative to the local path
# under the mysite.com directory.
RewriteRule ^index.html$ /app/app.html [L]

# If we had written
RewriteRule ^index.html$ /app.html [L]
# Apache would assume http://mysite.com/app.html

# If we wanted to write something more general,
# it means that in the substitution pattern we add /app,
# which is equivalent to example 1.
# This is really done for directory access.
# Sets the base directory for mod_rewrite
RewriteBase /app
# RewriteRule example for using a new base directory
RewriteRule ^index.html$ app.html [L]
```

### RewriteOption

```conf
# Inherit parent RewriteRules and place them after rules listed within this file.
RewriteOptions Inherit

# Inherit parent RewriteRules and place them before rules listed within this file.
RewriteOptions InheritBefore

# Merge parent RewriteBase directives to apply to this htaccess directory
RewriteOption MergeBase
```

### RewriteMap

RewriteMap allows the use of a text file, a database, an external program, an internal function for rewriting.

RewriteMap MapName MapType:MapSource

MapName: arbitrary name for the map
MapType: one of: txt, rnd, dbm, int, prg, dbd
MapSource: source path to the map file

```conf
<VirtualHost *:80>
    RewriteEngine On

    # Define a text file
    RewriteMap SiteMap txt:/usr/local/mysite/siteMap.txt

    # Define a dbm
    RewriteMap dbmSiteMap dbm:/usr/local/mysite/dbmSiteMap.dbm

    # Define a rnd
    RewriteMap rndSiteMap rnd:/usr/local/mysite/rndSiteMap.txt

	# Define internal functions, one of: toupper, tolower, escape, unescape
	RewriteMap lc int:tolower

	# Define custom external application
	RewriteMap dd prg:/usr/local/mysite/myprogramme.sh

    <Directory /var/www/mysite.com>
        # Use SiteMap to rewrite the url from the siteMapfile (cf definition below)
        # f the asked foo does not exist into the db serve the list.html file
        # http://mysite.com/foo/bar => http://test1.loc
        # http://mysite.com/foo/oof => http://othersite.loc
        # http://mysite.com/foo/boo => http://bar2.loc
        RewriteRule ^foo/(.*)$ ${SiteMap:$1|http://mysite.com/foo/list.html} [R,L]

        # Same result as the previous one but with a db dbmSiteMap (cf definition below)
        # It's faster for Apache to use dbm than text file
        RewriteRule ^foo/(.*)$ ${dbmSiteMap:$1|http://mysite.com/foo/list.html} [R,L]

        # Use rndSiteMap to redirect to a random url (cf definition below)
        # http://mysite.com/foo/random => http://mysite.com/foo/bar1 or bar2 or bar3
        RewriteRule ^foo/random$ http://mysite.com/foo/${rndSiteMap} [L,R]

        # Use internal function for putting to lowercase
        RewriteRule ^foo/(.*)$ http://mysite.com/foo/${lc:$1}.html [R,L]

        # Use internal function for executing external program and to pass REQUEST_URI to it
        RewriteRule - ${dd:%{REQUEST_URI}}
    </Directory>

</VirtualHost *:80>
```

```conf
# /usr/local/mysite/rndSiteMap.txt
bar http://test1.loc
oof http://othersite.loc
boo http://bar2.loc
```

```conf
# /usr/local/mysite/rndSiteMap.txt
# Note: we have "bar1" twice to increase its probability of selection
foo bar1|bar2|bar3|bar1
```

You can convert a text file to dbm using

```bash
# https://httpd.apache.org/docs/2.4/fr/programs/httxt2dbm.html
httxt2dbm -in /usr/local/mysite/rndSiteMap.txt -out /usr/local/mysite/dbmSiteMap.dbm
```

### Directory Directive Slash or not

For directory and section documentation, please refer to:

    Apache Directory Directive: https://httpd.apache.org/docs/2.4/en/mod/core.html#directory
    Apache Sections Documentation: https://httpd.apache.org/docs/2.4/en/sections.html

For information on DirectorySlash, you can check:

    DirectorySlash Directive: https://httpd.apache.org/docs/2.4/mod/mod_dir.html#directoryslash

And for AllowNoSlash, refer to:

    AllowNoSlash Option: https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html#rewriteoptions

When using the Directory directive, Apache automatically redirects URLs without a trailing slash to URLs with a trailing slash, and it also ignores redirection rules. This behavior can be problematic if you want to serve a subdirectory such as "app" but still want URL redirection.

To disable this behavior, you need to:

```conf
<Directory "/opt/bitnami/apache/htdocs/app/">
    # -Indexes removes the list of files for a folder
    # FollowSymLinks is necessary to enable the rewrite engine on a Directory
    Options -Indexes +FollowSymLinks

    # Activate the rewrite engine
    RewriteEngine On

    # Do not automatically add a trailing slash to the directory
    DirectorySlash off
</Directory>
```

### Variables

http://www.askapache.com/htaccess/mod_rewrite-variables-cheatsheet.html

This list is not exhaustive.

| Name                                       | Description                                                                        | Example in the given                                                                      |
| ------------------------------------------ | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| %{HTTP_HOST}                               | The server name as requested by the client through the Host header                 | www.mysite.com                                                                            |
| %{SERVER_NAME}                             | The real name of the server                                                        | www.mysite.com                                                                            |
| %{REMOTE_ADDR}                             | The client's IP address                                                            |                                                                                           |
| %{SERVER_ADDR}                             | The server's IP address                                                            |                                                                                           |
| %{THE_REQUEST}                             | The complete request line (excluding headers)                                      | GET /forum/admin/index.php?page=db&start=30 HTTP/1.1                                      |
| %{HTTP_COOKIE}                             | A string containing all cookies sent by the client                                 | foo=bar; pref_order=asc                                                                   |
| %{SERVER_PORT}                             | The server's listening port (80 for HTTP and 443 for HTTPS)                        | 443                                                                                       |
| %{HTTP_ACCEPT}                             | The formats accepted by the client                                                 | text/xml,application/xml q=0.5                                                            |
| %{REMOTE_HOST}                             | The name of the client's machine or its address if the name is not available       |                                                                                           |
| %{REMOTE_PORT}                             | The port used by the client for the connection                                     |                                                                                           |
| %{REQUEST_URI}                             | The requested resource in the HTTP request                                         | /forum/admin/index.php                                                                    |
| %{HTTP_REFERER}                            | The referring URL of the user (not recommended as it's unreliable and falsifiable) |                                                                                           |
| %{QUERY_STRING}                            | The parameters passed in the URL                                                   | page=db&start=30                                                                          |
| %{DOCUMENT_ROOT}                           | The server's root as defined by the DocumentRoot directive                         | /usr/local/www/apache22/data/                                                             |
| %{REQUEST_METHOD}                          | The HTTP method used in the request                                                | GET                                                                                       |
| %{HTTP_USER_AGENT}                         | The client's user agent                                                            | Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11 |
| %{SCRIPT_FILENAME} and %{REQUEST_FILENAME} | The full path of the called script file                                            | /usr/local/www/apache22/data/forum/admin/index.php                                        |
| %{SERVER_PROTOCOL}                         | The description of the protocol used                                               | HTTP/1.1                                                                                  |
| %{HTTPS}                                   | A boolean indicating whether the secure protocol is being used                     | on                                                                                        |
| %{HTTP:X}                                  | Http header X                                                                      |                                                                                           |
| %{ENV:X}                                   | Environment Variables X                                                            |                                                                                           |
| %{SSL:X}                                   | Environment Variables SSL X (empty if no ssl)                                      |                                                                                           |
| %{TIME_YEAR}                               | A boolean indicating whether the secure protocol is being used                     |                                                                                           |
| %{TIME_MON}                                | A boolean indicating whether the secure protocol is being used                     |                                                                                           |
| %{TIME_DAY}                                | A boolean indicating whether the secure protocol is being used                     |                                                                                           |
| %{TIME_HOUR}                               | A boolean indicating whether the secure protocol is being used                     |                                                                                           |
| %{TIME_MIN}                                | A boolean indicating whether the secure protocol is being used                     |                                                                                           |
| %{TIME_SEC}                                | A boolean indicating whether the secure protocol is being used                     |                                                                                           |

### Usefull exemple

```conf
# Blocking directories
# Block access to URLs containing "admin" in the query string
RewriteCond %{QUERY_STRING} ^admin\w*$ [NC,OR]
# Block access to URLs ending with "admin/index.php" or "admin/index.html" in the query string
RewriteCond %{QUERY_STRING} ^admin\w*/index\.(php|html)$ [NC]
# For any URL matching the conditions above, return a 403 Forbidden status
RewriteRule .* - [F]

# Redirect to HTTPS
# Redirect all requests to HTTPS if not already using port 80
RewriteCond %{SERVER_PORT} !^80$
RewriteRule ^.*$ https://%{HTTP_HOST}%{REQUEST_URI} [R]

# Reject certain HTTP methods
# Block requests using specific HTTP methods such as HEAD, TRACE, DELETE, PUT
RewriteCond %{REQUEST_METHOD} ^(HEAD|TRACE|DELETE|PUT) [NC]
RewriteRule .* - [F]
```
