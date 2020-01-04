# Artifact Auction

## Testing

### Automated Testing

***Travis-CI*** continuous integration testing was used to ensure successful build passing at each push to ***GitHub***.
Initial difficulties were encountered with the library requirements of the AWS Cloud9 IDE. Once these requirements were removed from the requirements.txt file the build successfully passed. It was, however, necessary to remove requirements on a trial and error basis which resulted in several commits and failed builds at the early stages.
The following badge indicates the current Build status which, at the time of writing this ReadMe was passing.

[![Build Status](https://travis-ci.org/Shilldon/artifact-auction.svg?branch=master)](https://travis-ci.org/Shilldon/artifact-auction)

***Django*** built-in *unittest* library and *TestCase* subclass were used to test the backend models, forms and views. A total of 108 tests were written to ensure the backend code was thoroughly vetted.
This resulted in an average coverage of 93% well above the acceptable level.
Standard ***Django*** library commands were not tested.

<details>
<summary>Click here for the full coverage report.</summary>
```HTML5
Name                           Stmts   Miss  Cover
--------------------------------------------------
accounts/__init__.py               0      0   100%
accounts/admin.py                  3      0   100%
accounts/forms.py                 68     36    47%
accounts/models.py                16      1    94%
accounts/tests.py                  1      0   100%
accounts/url_reset.py              4      0   100%
accounts/views.py                 60     50    17%
artifact_auction/__init__.py       0      0   100%
artifact_auction/wsgi.py           4      4     0%
artifacts/__init__.py              0      0   100%
artifacts/admin.py                 7      0   100%
artifacts/forms.py                16      0   100%
artifacts/models.py               30      1    97%
artifacts/test_forms.py           48      0   100%
artifacts/test_models.py          39      1    97%
artifacts/test_views.py          106      0   100%
artifacts/views.py                83      4    95%
auctions/__init__.py               0      0   100%
auctions/admin.py                 12      3    75%
auctions/forms.py                 10      0   100%
auctions/models.py                53      6    89%
auctions/test_models.py           61      0   100%
auctions/test_views.py            88      0   100%
auctions/views.py                 80      0   100%
checkout/__init__.py               0      0   100%
checkout/admin.py                  7      0   100%
checkout/forms.py                 16      0   100%
checkout/models.py                21      0   100%
checkout/test_models.py           17      0   100%
checkout/test_views.py           159      8    95%
checkout/views.py                119      6    95%
collection/__init__.py             0      0   100%
collection/admin.py                2      0   100%
collection/contexts.py            11      0   100%
collection/models.py               2      0   100%
collection/test_views.py          54      0   100%
collection/views.py               30      4    87%
contact/__init__.py                0      0   100%
contact/admin.py                   1      0   100%
contact/forms.py                   6      0   100%
contact/models.py                  1      0   100%
contact/test_views.py             12      0   100%
contact/tests.py                   1      0   100%
contact/views.py                  15      0   100%
history/__init__.py                0      0   100%
history/admin.py                  11      0   100%
history/forms.py                   7      0   100%
history/models.py                 65      2    97%
history/test_models.py            72      5    93%
history/test_views.py             39      0   100%
history/views.py                  14      0   100%
home/__init__.py                   0      0   100%
home/admin.py                      2      0   100%
home/models.py                     2      0   100%
home/test_views.py                47      0   100%
home/views.py                     12      0   100%
reviews/__init__.py                0      0   100%
reviews/admin.py                   3      0   100%
reviews/forms.py                   9      0   100%
reviews/models.py                 11      0   100%
reviews/test_models.py            20      0   100%
reviews/test_views.py             53      0   100%
reviews/views.py                  28      0   100%
search/__init__.py                 0      0   100%
search/admin.py                    1      0   100%
search/forms.py                   34      1    97%
search/models.py                   1      0   100%
search/test_views.py             167      0   100%
search/views.py                   63      1    98%
--------------------------------------------------
TOTAL                           1924    133    93%
```
</details>

***Chrome DevTools Audit*** was also undertaken with positive results:
- Performance 100%
- Accessibility 100%
- Best Practices 93%
- SEO 89%

It was noted that the background and menu images delayed page load and, accordingly these images were further compressed and uploaded to AWS S3 Bucket to improve load times.

### Manual Testing

#### ***jquery***
As there was minimal ***jquery*** script most of which related to button presses, manual testing was undertaken for ***jquery*** code to ensure the correct responses.

#### Buttons and links
All navigation options, menus and links were tested manually.
It was also noted that the correct menu options are displayed depending on whether a user is logged in, is a superuser or is logged out.

#### Searching and filtering
As well as automated tests using the ***django*** testing framework manual filters and searches were undertaken to ensure correct results were returned.

### Mobile first design
Responsiveness of the site to differing display sizes was tested using ***Google Developer Tools*** and [Screenfly](http://quirktools.com/screenfly), resizing viewport to various resolutions:
- Desktop - 1280x1024,
- Galaxy S5 360x640,
- iPad - vertical 768x1024,
- iPad - horizontal 1024x768,
- iPhone5 320x568,
- iPhone7/6/8 375x667,
- iPhoneX 375x812,
- Laptop 1366x768
to ensure design responded appropriately.

### External feedback
After deploying to Heroku user feedback from a 10 person focus group was requested and acted upon.

Users were encouraged to create profiles, search for artifacts, make bids, change and update their profiles and request forgotten password resets to ensure functionality worked as expected.
Where errors were encountered ***Heroku*** logs were examined to identify and fix bugs.
