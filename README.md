# QNA-V
- Quotation Network Analysis -v Video
- `After-Hackathon` of `Seoul Editors Lab`
- Motto is [`Quis custodiet ipsos custodes?`](https://en.wikipedia.org/wiki/Quis_custodiet_ipsos_custodes%3F)

## Description
- Video clips which were uploaded by candidate's page (incl. camp's, party's, fan's) are friendly to itself. In case of presidential debate, they edited and posted clips in which their candidate won the opposing candidate logically. We can consider candidate's clips are positive-annotation of full video.
- Also, news media can upload the clips with their own editions. Sometimes, some press gets criticized by making biased edits (not only video but also text and image) to certain candidates.

![qnav-concept](https://raw.githubusercontent.com/dongkwan-kim/QNA-V/master/img/qnav-concept.jpg)

- QNA-V (Quotation Network Analysis -v Video) analyzes ratio of positive-annotated-clips of each candidate from all video files that news media uploaded. It can discover the political bias of news media.

## Attempts Log

### `2017.04.23 ~ 2017.04.24`
- We tried feature matching with OpenCV. Algorithm was [Brute-Force Matching with SIFT Descriptors](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html#brute-force-matching-with-sift-descriptors-and-ratio-test). It was too slow to get full data of a pair of video.
- Part of data is in `log/20170424`, branch is `v/bottleneck`
