# Facebook Scrubber

The Facebook Scrubber allows you do scrub up your Facebook profile of content
you may have uploaded or been tagged in years ago but now want to remove. Using
the Facebook Scrubber, you can save (in chronological order) all of the photos
you uploaded or were tagged in, delete all of the photos you uploaded, remove
all tags from of your tagged photos, and/or delete all of the posts you've made
on Facebook.  This is probably useful if you, like me, were raised in the
Internet age and have way too many photos and posts to delete manually.

There are alternative ways to do this, but from my cursory look across the
Internet, nothing seemed to work for me. For example:
* Regarding saving photos, most approaches relied on first scrolling through the
  photo gallery until reaching the end, and then downloading all of the photos.
  For me, this never worked because Facebook never seemed to be able to load all
  of my photos. In my approach, I select the first photo in the gallery and then
  'click right' until I get to the last photo, saving photos along the way.
* None of the approaches I've seen named saved files chronologically.
* None of the approaches I've seen did all of the functionality I mentioned in
  the first paragraph in one codebase. I didn't want to go through and integrate
  a bunch of other people's code.

Note the code is not guaranteed to work for you if Facebook changed its HTML
structure, so just in case I recommend saving your photos using my code first
before going on and deleting things. Last time I successfully ran all of the
code was on January 21, 2022.

I don't save your password. See for yourself by reading the code.

## Dependencies

* [chromedriver](https://chromedriver.chromium.org/home) (make sure to put this
  executable in your `$PATH`)

## Installation

```bash
python3 -m virtualenv venv
source activate venv/bin/activate
pip install -r requirements.txt
```

## Usage

For usage information, use the command below.

```bash
python fbscrubber.py -h
```

If you're running into bugs (see below) and you want your iteration time to be
quicker, I recommend commenting out the last two lines of the main file, opening
up the Python interpreter, and manually running the code in the main function.
This way, if an image doesn't download, you can just manually skip it in the
opened browser and resume the process by calling the `save_photos` function.

## Bugs

* The code is unable to handle signals properly all the time, causing a temp
  directory to exist after the process exited.
* Some photos don't have a standard date (may only have a year). I don't handle
  these through code and just manually save them.
* Some photos don't have a download button available. For now, I manually
  download these photos. (Is this really my bug? Or Facebook's...)
* Some photos don't have a menu button (lol). Again, not my bug. For now, I
  manually save these photos too.
* Some photos don't even show up on Facebook. I skip these, and unfortunately
  can't even save them manually.

## Contact

You can contact me at <<edward@edwardahn.me>>, but I probably won't be fixing
the code to continue to work with Facebook's changing UI. I figured this
codebase could be a good reference point for someone else though.

Goes without saying, but I'm not responsible for any data lost.

