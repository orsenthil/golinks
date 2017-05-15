Create an Environment File
--------------------------

Create an Environment file with appropriate values.

    GOOGLE_CLIENT_ID=
    GOOGLE_CLIENT_SECRET=
    DEBUG=
    MYSQL_DB=
    LOCAL_ADMIN_USERPASS=

* If `LOCAL_ADMIN_USERPASS`, then this overrides `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`.
* If `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` is provided oauth based authentication is performed.
* If neither `LOCAL_ADMIN_USERPASS` or `GOOGLE OAUTH` is provided a default `LOCAL_ADMIN_USERPASS` generated and
shared with you in the console.


Running via Docker
-----------------

	docker run -d -p 8000:5000 --net=host --env-file env-file.sh golinks:latest
