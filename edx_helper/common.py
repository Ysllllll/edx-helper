# -*- coding: utf-8 -*-

"""
Common type definitions and constants for edx-helper

The classes in this module represent the structure of courses in edX.  The
structure is:

* A Course contains Sections
* Each Section contains Subsections
* Each Subsection contains Units

Notice that we don't represent the full tree structure for both performance
and UX reasons:

Course ->  [Section] -> [SubSection] -> [Unit] -> [Video]

In the script the data structures used are:

1. The data structures to represent the course information:
   Course, Section->[SubSection]

2. The data structures to represent the chosen courses and sections:
   selections = {Course, [Section]}

3. The data structure of all the downloadable resources which represent each
   subsection via its URL and the of resources who can be extracted from the
   Units it contains:
   all_units = {Subsection.url: [Unit]}

4. The units can contain multiple videos:
   Unit -> [Video]
"""


class Course(object):
    """
    Course class represents course information.
    """

    def __init__(self, course_id, course_name, course_url, course_state):
        """
        @param course_id: The id of a course in edX is composed by the path
            {organization}/{course_number}/{course_run}
        @type course_id: str or None

        @param course_name: Name of the course. The name is taken from course page
            h3 header.
        @type course_name: str

        @param course_url: URL of the course.
        @type course_url: str or None

        @param course_state: State of the course. One of the following values:
            * 'Not yet'
            * 'Started'
        @type course_state: str
        """
        self.course_id = course_id
        self.course_name = course_name
        self.course_url = course_url
        self.course_state = course_state

    def __repr__(self):
        url = self.course_url if self.course_url else "None"
        return self.course_name + ": " + url


class Section(object):
    """
    Representation of a section of the course.
    """

    def __init__(self, position, name, url, subsections):
        """
        @param position: Integer position of the section in the list of
            sections. Starts at 1.
        @type position: int

        @param name: Name of the section.
        @type name: str

        @param url: URL of the section. None when section contains no
            subsections.
        @type url: str or None

        @param subsections: List of subsections.
        @type subsections: [SubSection]
        """
        self.position = position
        self.name = name
        self.url = url
        self.subsections = subsections


class SubSection(object):
    """
    Representation of a subsection in a section.
    """

    def __init__(self, position, name, url):
        """
        @param position: Integer position of the subsection in the subsection
            list. Starts at 1.
        @type position: int

        @param name: Name of the subsection.
        @type name: str

        @param url: URL of the subsection.
        @type url: str
        """
        self.position = position
        self.name = name
        self.url = url

    def __repr__(self):
        return self.name + ": " + self.url


class Block(object):
    """
    Representation of a block of the course.
    """

    def __init__(self, position, block_id, name, block_type, url, children):
        """
        @param position: Integer position of the block in the list of blocks. Starts at 1.
        @type position: int

        @param block_id: id of the block.
        @type block_id: str

        @param name: name of the block.
        @type name: str

        @param block_type: type of the block.
        @type block_type: str
            available value: course, chapter, sequential, vertical

        @param url: url of the block.
        @type url: str
        """
        self.position = position
        self.block_id = block_id
        self.name = name
        self.block_type = block_type
        self.url = url
        self.children = children


class Unit(object):
    """
    Representation of a single unit of the course.
    """

    def __init__(self, videos, resources_urls):
        """
        @param videos: List of videos present in the unit.
        @type videos: [Video]

        @param resources_urls: List of additional resources that are come along
            with the unit. Resources include files with certain extensions
            and YouTube links.
        @type resources_urls: [str]
        """
        self.videos = videos
        self.resources_urls = resources_urls


class WebpageUnit(Unit):
    """
    Representation of a Webpage for unit in the course.
    Used for unit type: discussion, html, problem, etc, not video unit
    """

    def __init__(self, page_title, content):
        """ """
        super().__init__([], [])
        self.page_title = page_title
        self.content = content


class Video(object):
    """
    Representation of a single video.
    """

    def __init__(
        self, video_youtube_url, available_subs_url, sub_template_url, mp4_urls, video_data_metadata = None, origin_available_subs_url = None
    ):
        """
        @param video_youtube_url: Youtube link (if any).
        @type video_youtube_url: str or None

        @param available_subs_url: URL to the available subtitles.
        @type available_subs_url: str

        @param sub_template_url: ???
        @type sub_template_url: str

        @param mp4_urls: List of URLs to mp4 video files.
        @type mp4_urls: [str]
        """
        self.video_data_metadata = video_data_metadata
        self.origin_available_subs_url = origin_available_subs_url
        self.video_youtube_url = video_youtube_url
        self.available_subs_url = available_subs_url
        self.sub_template_url = sub_template_url
        self.mp4_urls = mp4_urls


class ExitCode(object):
    """
    Class that contains all exit codes of the program.
    """

    OK = 0
    MISSING_CREDENTIALS = 1
    WRONG_EMAIL_OR_PASSWORD = 2
    MISSING_COURSE_URL = 3
    INVALID_COURSE_URL = 4
    UNKNOWN_PLATFORM = 5
    NO_DOWNLOADABLE_VIDEO = 6


YOUTUBE_DL_CMD = ["youtube-dl", "--ignore-config"]
DEFAULT_CACHE_FILENAME = "cached_units.cache"
DEFAULT_FILE_FORMATS = [
    "e?ps",
    "pdf",
    "txt",
    "doc",
    "xls",
    "ppt",
    "srt",
    "docx",
    "xlsx",
    "pptx",
    "odt",
    "ods",
    "odp",
    "odg",
    "zip",
    "rar",
    "gz",
    "mp3",
    "R",
    "Rmd",
    "ipynb",
    "py",
]
