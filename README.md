# pod-charlesreid1-site

This repo contains docker compose file for running
the charlesreid1.com site.

The services are:
* nginx
* Lets Encrypt

Pretty simple, right?

## Volumes

No data volumes are used.

* nginx static content is a bind-mounted host directory
* lets encrypt container generates site certs into bind-mounted host directory
* nginx certificates come from docker secrets (?)

```
  web:
    volumes:
      - ./letsencrypt_certs:/etc/nginx/certs
      - ./letsencrypt_www:/var/www/letsencrypt

  letsencrypt:
    image: certbot/certbot
    command: /bin/true
    volumes:
      - ./letsencrypt_certs:/etc/letsencrypt
      - ./letsencrypt_www:/var/www/letsencrypt
```

## Certs and Secrets

Lets Encrypt generates certs in a container 
with a one-liner, dumps them to bind-mounted 
host directory.

This file can be generated 

## Backups

Site content comes from github.
Nothing to back up.

## Static Content

Question: should we bake the site's 
static content into the container,
and require rebuild/redeploy when
site content changes?

Answer: No. We clone a local copy of 
the gh-pages branch, and bind-mount 
that into the container.

Updating the site is as simple as 
`git pull origin gh-pages`.

