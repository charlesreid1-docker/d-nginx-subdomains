# d-nginx-subdomains

This repo contains docker containers
and a docker compose file for running
an nginx web server for subdomain
one-pagers.

The services are just:

* nginx

This is also intended to be reverse proxied
by another frontend nginx server,
so this one-container pod will bind 
to a VPN IP address and establish
(unecrypted) HTTP connections over the 
(encrypted) VPN connection.

Pretty simple, right?

# Networking

The setup for this one-container docker pod 
is to have an nginx container bound to all
addresses inside the container (see nginx.conf
selection below) and then bind that port 
inside the container to a specific IP and port
on the host (see docker-compose selection below).

The nginx configuration file contains a listen
directive that binds nginx to all addresses 
inside the container:

```
server {
    listen *:7777;
```

Meanwhile, in the `docker-compose.yml` file,
we bind the container's port 7777 to the 
host's port 7777, but only on a private
IP address:

```
servies:
  stormy_nginx_subs:
    ...
    ports:
      - "10.5.0.2:7777:7777"
```


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
      - "/www/pages.charlesreid1.com/htdocs:/www/pages.charlesreid1.com/htdocs:ro"
      - "/www/hooks.charlesreid1.com/htdocs:/www/hooks.charlesreid1.com/htdocs:ro"
      - "/www/bots.charlesreid1.com/htdocs:/www/bots.charlesreid1.com/htdocs:ro"
```

The first line sets the nginx config files,
the rest set the static content locations.


# Backups

Site content comes from git.charlesreid1.com,
nothing to back up.

# Workflow

## Static Content Directory Layout

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


## Deploying Static Content with Git

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

## Updating Static Content with Git


```
git \
    --git-dir=/www/example.com/git \
    --work-tree=/www/example.com/htdocs/reponame \
    pull origin gh-pages
```
