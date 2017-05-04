Design
------

* [Full UI design](https://www.lucidchart.com/publicSegments/view/098604ec-b48c-48d6-9098-ba3a31f275a8/image.pdf)

Similar Software
----------------

* https://github.com/maccman/go
* https://github.com/kellegous/go

TODO
----

1) Dockerfile and run in docker.


Running via Docker
-----------------

::

	docker run -d -p 8000:5000 --net=host --env-file env-file.sh golinks:latest
