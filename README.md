# Wattpad ebook scraper

Scrape Wattpad stories into epub files for offline reading.

Please use this for personal use only.

## Usage

List one or more story URLs as command line arguments

```
$ python3 scrape.py http://www.wattpad.com/story/9876543-example-story http://www.wattpad.com/story/9999999-example-story-2
```

Or feed it a list of story URLs, one per line, via standard input.

```
$ python3 scrape.py < list_of_story_urls.txt
```

You may convert the epub to a mobi file with `kindlegen` or similar tools if desired.

## Details

This uses documented and undocumented portions of the Wattpad API. The undocumented portions of the API allow downloading story text, which conceivably could break in the future.

The story details API call is also undocumented and is from the internal v3 API used by the Android app. This would be a very useful API call to make public.

The chapters are assembled into an epub with epubbuilder, but nothing is really done to clean up the HTML. Epub files are supposed to be fully valid XHTML.

## Dependencies

Depends on [epubbuilder](https://github.com/footley/epubbuilder), [requests](http://python-requests.org), [python-dateutil](http://labix.org/python-dateutil) and [smartypants](https://pypi.python.org/pypi/smartypants/).

Install them with `pip3`:

```
$ pip3 install genshi lxml epubbuilder requests python-dateutil smartypants
```

## TODO

*   Verify the user input to actually be a valid story URL (regex).
*   Story/group description is text, not HTML. Remove HTML parsing of it.
*   Actually include `createDate`, `modifyDate`, `categories`, and `rating` in the epub output. Currently they are extracted but ignored.
*   If `modifyDate` is stored into the epub, and if it is possible to rewrte existing epubs (not currently possible with epubbuilder), then only modified portions of stories could be redownloaded.
*   Slow down downloads to comply with the requirement that "any automated system [...] that accesses the Website in a manner that sends more request messages to the Wattpad.com servers in a given period of time than a human can reasonably produce in the same period by using a conventional on-line web browser" from the [terms of service](http://www.wattpad.com/terms).
    -   That said, this probably violates the rest of the ToS everywhere else, but may as well be nice and not thrash sites with fast downloads.
*   Clean up XHTML output for epub, remove extra HTML attributes.
*   Actually do error checking on API responses
    -   Handle stories not existing, etc.
