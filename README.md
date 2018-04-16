# d-nginx-subdomains

This repo contains docker containers
and a docker compose file for running
an nginx web server for subdomain
one-pagers.

The services are just:
* nginx

If you want to do SSL you can, but you have to 
run Let's Encrypt outside of the container
and bind-mount your certificates into the 
container at `/etc/letsencrypt`.

Pretty simple, right?

# Config files

All `*.conf` files in the `conf.d/` directory will be picked up by nginx.

The config files must be named `*.conf`.


# Volumes

No data volumes are used.

* nginx static content is a bind-mounted host directory
* lets encrypt generates site certs, which will be bind-mounted into host directory

Here is the volumes directive in `docker-compose.yml`:

```
    volumes:
      - "./conf.d:/etc/nginx/conf.d"
      - "/etc/localtime:/etc/localtime:ro"
      - "/etc/letsencrypt:/etc/letsencrypt"
      - "./www:/usr/share/nginx/html:ro"
```

The first line sets the nginx config files,
the second line sets the time in the container
to the time in the host, the third mounts the 
SSL certificates, and the last mounts the 
live web content.

For multiple one-pagers, the last line will
get more complicated, and will need to match
the directories in the nginx config file:

```
    volumes:
      - "./conf.d:/etc/nginx/conf.d"
      - "/etc/localtime:/etc/localtime:ro"
      - "/etc/letsencrypt:/etc/letsencrypt"
      - "/www/site1.com/htdocs:/www/site1.com/htdocs:ro"
      - "/www/site2.com/htdocs:/www/site2.com/htdocs:ro"
      - "/www/site3.com/htdocs:/www/site3.com/htdocs:ro"
      - "/www/site4.com/htdocs:/www/site4.com/htdocs:ro"
```


# Backups

Site content comes from git.charlesreid1.com,
nothing to back up.

# Workflow

### Static Content Directory Layout

Directories with static content are bind-mounted
read-only into the container. To update the content
being served, just update the content directory
on the host.

(This enables you to use version control to 
track the live site contents.)

The section below covers how accomplish this layout.
You should have your web content laid out as follows
on the host:

```
/www
    example.com/
        htdocs/
            index.html
            ...
        example.com-src/
            README.md
            pelican/
            ...
        git/
            <contents of .git dir>
            ...

    example2.com/
        htdocs/
            ...
        example2.com-src/
            ...
        git/
            ...
```

In the container, you will have a mirrored directory
structure, but only `htdocs`:

```
/www
    example.com/
        htdocs/
            index.html
            ...

    example2.com/
        htdocs/
            ...
```



### Deploying Static Content with Git

You can use git to deploy static content, but take care
not to put your `.git` directory into the live 
web directory.

```
git clone \
  --separate-git-dir=/www/example.com/git \
  -b gh-pages \
  <url-of-static-site> \
  /www/example.com/htdocs
```

Let's walk through that:

* Clone command to deploy content fresh
* Separate git dir to keep git from being live
* Branch `gh-pages` (we decided to match Github's convention)
* Url of static site from git.charlesreid1.com
* The path of the final cloned repo (bind mounted into container)

See scripts for details.

### Updating Static Content with Git



Question: should we bake the site's 
static content into the container,
and require rebuild/redeploy when
site content changes?

Answer: No. We clone a local copy of 
the gh-pages branch, and bind-mount 
that into the container.

This enables webhooks to update 
the static site contents
without disturbing the container.

