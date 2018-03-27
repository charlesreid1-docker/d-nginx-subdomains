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

Lets Encrypt should generate certificates at `/etc/letsencrypt/live/domain/`:

```
root@krash:/home/charles/codes/docker/pod-charlesreid1-site# ls -l /etc/letsencrypt/live/charlesreid1.blue/
total 4
lrwxrwxrwx 1 root root  41 Mar 27 01:03 cert.pem -> ../../archive/charlesreid1.blue/cert1.pem
lrwxrwxrwx 1 root root  42 Mar 27 01:03 chain.pem -> ../../archive/charlesreid1.blue/chain1.pem
lrwxrwxrwx 1 root root  46 Mar 27 01:03 fullchain.pem -> ../../archive/charlesreid1.blue/fullchain1.pem
lrwxrwxrwx 1 root root  44 Mar 27 01:03 privkey.pem -> ../../archive/charlesreid1.blue/privkey1.pem
-rw-r--r-- 1 root root 543 Mar 27 01:03 README
```

These certificate files will be bind-mounted into the nginx container.

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

