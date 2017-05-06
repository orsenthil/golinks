Design
------

* [Full UI design](https://www.lucidchart.com/publicSegments/view/098604ec-b48c-48d6-9098-ba3a31f275a8/image.pdf)


Running via Docker
-----------------

	docker run -d -p 8000:5000 --net=host --env-file env-file.sh golinks:latest
