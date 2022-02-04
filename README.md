# Facebook Scrubber

The Facebook Scrubber allows you do scrub up your Facebook profile of content
you may have uploaded or been tagged in years ago but now want to remove. Using
the Facebook Scrubber, you can save (in chronological order) all of the photos
you uploaded or were tagged in, remove all tags from of your tagged photos,
and/or delete all of the posts you've made on Facebook.  This is probably useful
if you, like me, were raised in the Internet age and have way too many photos
and posts to delete manually.

There are alternative ways to do this, but from my cursory look across the
Internet, nothing seemed to work for me. For example:
* Regarding saving photos, most approaches relied on first scrolling through the
  photo gallery until reaching the end and then downloading all of the photos.
  For me, this never worked because Facebook never seemed to be able to load all
  of my photos. In my approach, I select the first photo in the gallery and then
  'click right' repeatedly, saving photos along the way.
* None of the approaches I've seen named saved photos chronologically.
* None of the approaches I've seen did all of the functionality I mentioned in
  the first paragraph in one codebase. I didn't want to go through and integrate
  a bunch of other people's code.

Note the code is not guaranteed to work for you if Facebook changed its page
structure, so just in case I recommend saving your photos using my code first
before going on and deleting/removing things. Last time I successfully ran all
of the code was on February 2022.

I don't save your password.

## Dependencies

First, download [chromedriver](https://chromedriver.chromium.org/home) (make
sure to put this executable in your `$PATH`).

Then, setup your virtual environment.

```bash
$ python3 -m virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Usage

There are two ways to run the scrubber. To run the scrubber normally, use the
command below.

```bash
$ python run.py -h
```

If you're running into bugs (see section below) and you want your iteration time
to be quicker, I recommend running the scrubber interactively. I personally like
running the scrubber interactively for the flexibility it provides too (ex. I
can initialize the scrubber, filter out posts that I want to keep manually, and
then run the scrubber to delete posts). To do this, use the following commands.

```bash
$ python
Python 3.8.9 (default, Jul 19 2021, 09:37:30)
[Clang 13.0.0 (clang-1300.0.27.3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from interactive import *
```

From this point, you can use commands like `scraper.delete_posts()` in the
Python interpreter at your own speed. For help on what to do, look at `run.py`.

## Bugs

* When saving photos, the code is unable to handle signals like SIGINT properly
  all the time, causing a temp directory to sometimes exist after the process
  exited.
* Some photos don't have a standard date (may only have a year). I don't handle
  these through code and just manually save/delete them.
* Some photos don't have a download button available. For now, I manually
  download these photos. (Is this really my bug? Or Facebook's...)
* Some photos don't have a menu button (lol). Again, not my bug. For now, I
  manually save/delete these photos too.
* Some photos don't even show up on Facebook. I skip these, and unfortunately
  can't even save them manually.

## Notes

* To get the CSS selector (ex. of the date of when a photo was posted), open
  Firefox, right-click the mouse, click "Inspect", find the element you want a
  CSS selector for, right-click the HTML tag of the element you want, and copy
  the CSS selector. For some reason, this doesn't work on Chrome well.
* You may have to play around with how much with `time.sleep` calls depending on
  your internet connection.

## Contact

You can contact me at <<edward@edwardahn.me>>, but I probably won't be fixing
the code to continue to work with Facebook's changing UI. I figured this
codebase could be a good reference point for someone else though.

I'm not responsible for any data lost.

