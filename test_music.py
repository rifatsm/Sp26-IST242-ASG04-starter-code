"""
Instructor-provided test suite for ASG04 – Music Track Hierarchy.

Run with:
    python -m pytest test_music.py -v
or simply:
    pytest -v

All tests must pass for full credit.
"""

import pytest

from artist import Artist
from album import Album
from music_track import MusicTrack
from song import Song
from podcast import Podcast
from playlist import Playlist


# =============================================================================
#  Artist tests
# =============================================================================

class TestArtist:

    def test_constructor_stores_name(self):
        a = Artist("Kendrick Lamar", "Hip-Hop")
        assert a.name == "Kendrick Lamar"

    def test_constructor_stores_genre(self):
        a = Artist("Kendrick Lamar", "Hip-Hop")
        assert a.genre == "Hip-Hop"

    def test_str(self):
        a = Artist("Kendrick Lamar", "Hip-Hop")
        assert str(a) == "Kendrick Lamar, Hip-Hop"

    def test_str_different_artist(self):
        a = Artist("Joe Rogan", "Comedy")
        assert str(a) == "Joe Rogan, Comedy"

    def test_name_property_readonly(self):
        """The property should exist; there should be no public setter."""
        a = Artist("X", "Y")
        assert hasattr(a, "name")
        # Attempting to set should raise AttributeError (no setter defined)
        with pytest.raises(AttributeError):
            a.name = "Z"

    def test_genre_property_readonly(self):
        a = Artist("X", "Y")
        with pytest.raises(AttributeError):
            a.genre = "Z"


# =============================================================================
#  Album tests
# =============================================================================

class TestAlbum:

    def test_constructor_stores_title(self):
        al = Album("DAMN.", True, [2017, 2018])
        assert al.title == "DAMN."

    def test_constructor_stores_active(self):
        al = Album("DAMN.", True, [2017, 2018])
        assert al.active is True

    def test_constructor_stores_years(self):
        al = Album("DAMN.", True, [2017, 2018])
        assert al.years == [2017, 2018]

    def test_debut_year_returns_first(self):
        al = Album("F", True, [1995, 1996, 1997])
        assert al.debut_year == 1995

    def test_debut_year_single_entry(self):
        al = Album("G", False, [2020])
        assert al.debut_year == 2020

    def test_str_contains_title(self):
        al = Album("DAMN.", True, [2017, 2018])
        assert "DAMN." in str(al)

    def test_str_contains_active_flag(self):
        al = Album("DAMN.", True, [2017, 2018])
        assert "True" in str(al)

    def test_str_contains_debut_year(self):
        al = Album("DAMN.", True, [2017, 2018])
        assert "2017" in str(al)

    def test_str_inactive_album(self):
        al = Album("Jagged Little Pill", False, [1995, 1996])
        s = str(al)
        assert "Jagged Little Pill" in s
        assert "False" in s
        assert "1995" in s

    # --- ValueError on empty years ---

    def test_empty_years_raises_value_error(self):
        with pytest.raises(ValueError):
            Album("Ghost", False, [])

    def test_value_error_message_is_descriptive(self):
        """The error message should mention the album title or 'years'."""
        with pytest.raises(ValueError, match=r"(?i)(year|empty|non-empty|Ghost)"):
            Album("Ghost", False, [])

    # --- Defensive copy on input ---

    def test_years_input_defensive_copy(self):
        """Mutating the original list must NOT affect the stored years."""
        original = [2000, 2001]
        al = Album("Test", True, original)
        original.append(2002)
        assert len(al.years) == 2

    def test_years_input_defensive_copy_clear(self):
        original = [1999]
        al = Album("Test", False, original)
        original.clear()
        assert al.years == [1999]

    # --- Defensive copy on output ---

    def test_years_getter_returns_copy(self):
        """Mutating the returned list must NOT affect internal data."""
        al = Album("Test", True, [2000, 2001])
        returned = al.years
        returned.append(9999)
        assert len(al.years) == 2

    def test_years_getter_clear_does_not_affect_internal(self):
        al = Album("Test", False, [2010])
        al.years.clear()
        assert al.years == [2010]


# =============================================================================
#  MusicTrack abstract-contract tests
# =============================================================================

class TestMusicTrackAbstract:

    def test_cannot_instantiate_music_track_directly(self):
        """MusicTrack is abstract and must raise TypeError on direct creation."""
        with pytest.raises(TypeError):
            MusicTrack(
                Artist("X", "Y"),
                Album("Z", True, [2020]),
                200.0,
            )

    def test_subclass_without_play_time_formatted_raises(self):
        """A subclass missing play_time_formatted must raise TypeError."""
        with pytest.raises(TypeError):

            class IncompleteTrack(MusicTrack):
                pass  # play_time_formatted not implemented

            IncompleteTrack(
                Artist("X", "Y"),
                Album("Z", True, [2020]),
                200.0,
            )


# =============================================================================
#  Song tests
# =============================================================================

class TestSong:

    @pytest.fixture
    def humble(self):
        """220 seconds → 03:40"""
        return Song(
            Artist("Kendrick Lamar", "Hip-Hop"),
            Album("DAMN.", True, [2017, 2018]),
            220.0,
        )

    @pytest.fixture
    def you_oughta_know(self):
        """245 seconds → 04:05"""
        return Song(
            Artist("Alanis Morissette", "Alternative"),
            Album("Jagged Little Pill", False, [1995, 1996]),
            245.0,
        )

    # --- Inherited fields via Vehicle parent ---

    def test_artist_name(self, humble):
        assert humble.artist.name == "Kendrick Lamar"

    def test_artist_genre(self, humble):
        assert humble.artist.genre == "Hip-Hop"

    def test_album_title(self, humble):
        assert humble.album.title == "DAMN."

    def test_duration_seconds(self, humble):
        assert humble.duration_seconds == pytest.approx(220.0)

    def test_release_year(self, humble):
        assert humble.release_year == 2017

    def test_release_year_different_song(self, you_oughta_know):
        assert you_oughta_know.release_year == 1995

    # --- Concrete method inherited from MusicTrack ---

    def test_total_play_time_ten_plays(self, humble):
        assert humble.total_play_time(10) == pytest.approx(2200.0)

    def test_total_play_time_zero_plays(self, humble):
        assert humble.total_play_time(0) == pytest.approx(0.0)

    def test_total_play_time_one_play(self, humble):
        assert humble.total_play_time(1) == pytest.approx(220.0)

    # --- play_time_formatted: MM:SS ---

    def test_play_time_formatted_220_seconds(self, humble):
        assert humble.play_time_formatted() == "03:40"

    def test_play_time_formatted_245_seconds(self, you_oughta_know):
        assert you_oughta_know.play_time_formatted() == "04:05"

    def test_play_time_formatted_65_seconds(self):
        s = Song(Artist("A", "B"), Album("C", True, [2020]), 65.0)
        assert s.play_time_formatted() == "01:05"

    def test_play_time_formatted_zero_seconds(self):
        s = Song(Artist("A", "B"), Album("C", True, [2020]), 0.0)
        assert s.play_time_formatted() == "00:00"

    def test_play_time_formatted_exactly_one_minute(self):
        s = Song(Artist("A", "B"), Album("C", True, [2020]), 60.0)
        assert s.play_time_formatted() == "01:00"

    def test_play_time_formatted_59_seconds(self):
        s = Song(Artist("A", "B"), Album("C", True, [2020]), 59.0)
        assert s.play_time_formatted() == "00:59"

    # --- __str__ ---

    def test_str_contains_artist(self, humble):
        assert "(Kendrick Lamar, Hip-Hop)" in str(humble)

    def test_str_contains_album_title(self, humble):
        assert "DAMN." in str(humble)

    def test_str_contains_duration(self, humble):
        assert "03:40" in str(humble)

    def test_str_does_not_contain_explicit(self, humble):
        """Song __str__ should not mention 'explicit'."""
        assert "explicit" not in str(humble).lower()

    def test_str_does_not_contain_hh_mm_ss_format(self, humble):
        """Song uses MM:SS, not HH:MM:SS."""
        # Should NOT contain two colons
        assert str(humble).count(":") == 1 or "03:40" in str(humble)
        # More direct: the formatted time should be exactly 5 chars (MM:SS)
        assert humble.play_time_formatted() == "03:40"
        assert len(humble.play_time_formatted()) == 5

    # --- isinstance checks ---

    def test_song_is_instance_of_music_track(self, humble):
        assert isinstance(humble, MusicTrack)


# =============================================================================
#  Podcast tests
# =============================================================================

class TestPodcast:

    @pytest.fixture
    def jre_explicit(self):
        """9000 seconds → 02:30:00, explicit"""
        return Podcast(
            Artist("Joe Rogan", "Comedy"),
            Album("The Joe Rogan Experience", True, [2009, 2010]),
            9000.0,
            is_explicit=True,
        )

    @pytest.fixture
    def serial_default(self):
        """5400 seconds → 01:30:00, not explicit (default)"""
        return Podcast(
            Artist("Sarah Koenig", "Journalism"),
            Album("Serial", False, [2014, 2015]),
            5400.0,
        )

    # --- is_explicit field ---

    def test_explicit_true(self, jre_explicit):
        assert jre_explicit.is_explicit is True

    def test_explicit_defaults_to_false(self, serial_default):
        assert serial_default.is_explicit is False

    # --- Inherited fields ---

    def test_artist_name(self, jre_explicit):
        assert jre_explicit.artist.name == "Joe Rogan"

    def test_album_title(self, jre_explicit):
        assert jre_explicit.album.title == "The Joe Rogan Experience"

    def test_duration_seconds(self, jre_explicit):
        assert jre_explicit.duration_seconds == pytest.approx(9000.0)

    def test_release_year(self, jre_explicit):
        assert jre_explicit.release_year == 2009

    def test_release_year_serial(self, serial_default):
        assert serial_default.release_year == 2014

    # --- Concrete method inherited from MusicTrack ---

    def test_total_play_time(self, jre_explicit):
        assert jre_explicit.total_play_time(3) == pytest.approx(27000.0)

    def test_total_play_time_serial(self, serial_default):
        assert serial_default.total_play_time(2) == pytest.approx(10800.0)

    # --- play_time_formatted: HH:MM:SS ---

    def test_play_time_formatted_9000_seconds(self, jre_explicit):
        assert jre_explicit.play_time_formatted() == "02:30:00"

    def test_play_time_formatted_5400_seconds(self, serial_default):
        assert serial_default.play_time_formatted() == "01:30:00"

    def test_play_time_formatted_3661_seconds(self):
        p = Podcast(Artist("A", "B"), Album("C", True, [2020]), 3661.0)
        assert p.play_time_formatted() == "01:01:01"

    def test_play_time_formatted_3600_seconds(self):
        p = Podcast(Artist("A", "B"), Album("C", True, [2020]), 3600.0)
        assert p.play_time_formatted() == "01:00:00"

    def test_play_time_formatted_zero_seconds(self):
        p = Podcast(Artist("A", "B"), Album("C", True, [2020]), 0.0)
        assert p.play_time_formatted() == "00:00:00"

    def test_play_time_formatted_has_two_colons(self, jre_explicit):
        """HH:MM:SS must have exactly two colons."""
        assert jre_explicit.play_time_formatted().count(":") == 2

    def test_play_time_formatted_length_is_eight(self, jre_explicit):
        """HH:MM:SS must be exactly 8 characters."""
        assert len(jre_explicit.play_time_formatted()) == 8

    # --- __str__ ---

    def test_str_contains_artist(self, jre_explicit):
        assert "(Joe Rogan, Comedy)" in str(jre_explicit)

    def test_str_contains_album_title(self, jre_explicit):
        assert "The Joe Rogan Experience" in str(jre_explicit)

    def test_str_contains_formatted_duration(self, jre_explicit):
        assert "02:30:00" in str(jre_explicit)

    def test_str_contains_is_explicit_true(self, jre_explicit):
        assert "True" in str(jre_explicit)

    def test_str_contains_is_explicit_false(self, serial_default):
        assert "False" in str(serial_default)

    def test_str_contains_explicit_keyword(self, jre_explicit):
        assert "explicit" in str(jre_explicit).lower()

    # --- isinstance checks ---

    def test_podcast_is_instance_of_music_track(self, jre_explicit):
        assert isinstance(jre_explicit, MusicTrack)


# =============================================================================
#  Comparison / ordering tests
# =============================================================================

class TestMusicTrackComparison:

    @pytest.fixture
    def song_1995(self):
        return Song(
            Artist("Alanis Morissette", "Alternative"),
            Album("Jagged Little Pill", False, [1995, 1996]),
            245.0,
        )

    @pytest.fixture
    def podcast_2009(self):
        return Podcast(
            Artist("Joe Rogan", "Comedy"),
            Album("The Joe Rogan Experience", True, [2009, 2010]),
            9000.0,
            is_explicit=True,
        )

    @pytest.fixture
    def song_2017(self):
        return Song(
            Artist("Kendrick Lamar", "Hip-Hop"),
            Album("DAMN.", True, [2017, 2018]),
            220.0,
        )

    @pytest.fixture
    def podcast_1995(self):
        """Different type, same year as song_1995 — tests cross-type equality."""
        return Podcast(
            Artist("X", "Y"),
            Album("Vintage Show", False, [1995]),
            3600.0,
        )

    # --- __lt__ ---

    def test_lt_true(self, song_1995, podcast_2009):
        assert song_1995 < podcast_2009

    def test_lt_false_when_greater(self, song_2017, song_1995):
        assert not (song_2017 < song_1995)

    def test_lt_false_when_equal(self, song_1995, podcast_1995):
        assert not (song_1995 < podcast_1995)

    # --- __eq__ ---

    def test_eq_same_year_different_types(self, song_1995, podcast_1995):
        """A Song and a Podcast released in the same year should be equal."""
        assert song_1995 == podcast_1995

    def test_eq_same_type_same_year(self, song_1995):
        other = Song(
            Artist("B", "C"),
            Album("D", False, [1995]),
            100.0,
        )
        assert song_1995 == other

    def test_not_eq_different_years(self, song_1995, song_2017):
        assert song_1995 != song_2017

    # --- __gt__ (provided by @total_ordering) ---

    def test_gt(self, song_2017, podcast_2009):
        assert song_2017 > podcast_2009

    # --- __le__ (provided by @total_ordering) ---

    def test_le_when_less(self, song_1995, podcast_2009):
        assert song_1995 <= podcast_2009

    def test_le_when_equal(self, song_1995, podcast_1995):
        assert song_1995 <= podcast_1995

    # --- sorted() ---

    def test_sorted_ascending(self, song_1995, podcast_2009, song_2017):
        tracks = [song_2017, song_1995, podcast_2009]
        result = sorted(tracks)
        assert result[0].release_year == 1995
        assert result[1].release_year == 2009
        assert result[2].release_year == 2017

    def test_sorted_already_sorted_unchanged(self, song_1995, podcast_2009, song_2017):
        tracks = [song_1995, podcast_2009, song_2017]
        result = sorted(tracks)
        assert [t.release_year for t in result] == [1995, 2009, 2017]


# =============================================================================
#  Playlist tests
# =============================================================================

class TestPlaylist:

    @pytest.fixture
    def full_playlist(self):
        """Build the same four-track playlist as main.py."""
        p = Playlist()
        p.add_track(Song(
            Artist("Kendrick Lamar", "Hip-Hop"),
            Album("DAMN.", True, [2017, 2018]),
            220.0,
        ))
        p.add_track(Song(
            Artist("Alanis Morissette", "Alternative"),
            Album("Jagged Little Pill", False, [1995, 1996]),
            245.0,
        ))
        p.add_track(Podcast(
            Artist("Joe Rogan", "Comedy"),
            Album("The Joe Rogan Experience", True, [2009, 2010]),
            9000.0,
            is_explicit=True,
        ))
        p.add_track(Podcast(
            Artist("Sarah Koenig", "Journalism"),
            Album("Serial", False, [2014, 2015]),
            5400.0,
        ))
        return p

    # --- add_track ---

    def test_add_track_increases_count(self):
        p = Playlist()
        assert len(p.tracks) == 0
        p.add_track(Song(
            Artist("A", "B"),
            Album("C", True, [2020]),
            100.0,
        ))
        assert len(p.tracks) == 1

    def test_add_track_multiple(self, full_playlist):
        assert len(full_playlist.tracks) == 4

    # --- tracks property returns a copy ---

    def test_tracks_returns_copy(self):
        p = Playlist()
        p.add_track(Song(Artist("A", "B"), Album("C", True, [2020]), 100.0))
        external = p.tracks
        external.clear()
        assert len(p.tracks) == 1  # internal list unchanged

    def test_tracks_append_does_not_affect_playlist(self):
        p = Playlist()
        external = p.tracks
        external.append("this is not a MusicTrack")
        assert len(p.tracks) == 0

    # --- clear_playlist ---
    def test_clear_playlist_empties_list(self, full_playlist):
        full_playlist.clear_playlist()
        assert len(full_playlist.tracks) == 0

    def test_clear_playlist_does_not_set_none(self, full_playlist):
        """After clearing, add_track must still work — internal list is not None."""
        full_playlist.clear_playlist()
        # If _tracks were set to None, this would raise AttributeError
        full_playlist.add_track(Song(
            Artist("A", "B"),
            Album("C", True, [2020]),
            100.0,
        ))
        assert len(full_playlist.tracks) == 1

    def test_clear_playlist_then_re_add(self, full_playlist):
        full_playlist.clear_playlist()
        full_playlist.add_track(Song(
            Artist("X", "Y"),
            Album("Z", False, [2000]),
            180.0,
        ))
        full_playlist.add_track(Song(
            Artist("P", "Q"),
            Album("R", True, [2005]),
            200.0,
        ))
        assert len(full_playlist.tracks) == 2

    # --- sort_by_release_year ---

    def test_sort_by_release_year_ascending(self, full_playlist):
        full_playlist.sort_by_release_year()
        years = [t.release_year for t in full_playlist.tracks]
        assert years == sorted(years)

    def test_sort_by_release_year_specific_order(self, full_playlist):
        full_playlist.sort_by_release_year()
        tracks = full_playlist.tracks
        assert tracks[0].release_year == 1995
        assert tracks[1].release_year == 2009
        assert tracks[2].release_year == 2014
        assert tracks[3].release_year == 2017

    def test_sort_by_release_year_first_track_type(self, full_playlist):
        """After sorting, the first track (1995) should be a Song."""
        full_playlist.sort_by_release_year()
        assert isinstance(full_playlist.tracks[0], Song)

    def test_sort_by_release_year_last_track_type(self, full_playlist):
        """After sorting, the last track (2017) should be a Song."""
        full_playlist.sort_by_release_year()
        assert isinstance(full_playlist.tracks[3], Song)

    def test_sort_preserves_all_tracks(self, full_playlist):
        """Sorting must not drop or duplicate any tracks."""
        full_playlist.sort_by_release_year()
        assert len(full_playlist.tracks) == 4

    def test_sort_already_sorted_playlist(self):
        """Sorting an already-sorted playlist should leave it unchanged."""
        p = Playlist()
        p.add_track(Song(Artist("A", "B"), Album("Early", False, [1990]), 180.0))
        p.add_track(Song(Artist("C", "D"), Album("Later", True,  [2000]), 200.0))
        p.sort_by_release_year()
        years = [t.release_year for t in p.tracks]
        assert years == [1990, 2000]

    def test_sort_single_track_playlist(self):
        """A playlist with one track should sort without error."""
        p = Playlist()
        p.add_track(Song(Artist("A", "B"), Album("C", True, [2005]), 150.0))
        p.sort_by_release_year()
        assert p.tracks[0].release_year == 2005

    def test_sort_empty_playlist(self):
        """Sorting an empty playlist should not raise any error."""
        p = Playlist()
        p.sort_by_release_year()
        assert len(p.tracks) == 0

    # --- __str__ ---

    def test_str_contains_all_track_names(self, full_playlist):
        s = str(full_playlist)
        assert "DAMN." in s
        assert "Jagged Little Pill" in s
        assert "The Joe Rogan Experience" in s
        assert "Serial" in s

    def test_str_each_track_on_separate_line(self, full_playlist):
        s = str(full_playlist)
        lines = s.strip().split("\n")
        assert len(lines) == 4

    def test_str_empty_playlist_is_empty_string(self):
        p = Playlist()
        assert str(p) == ""

    def test_str_single_track_no_newline(self):
        p = Playlist()
        p.add_track(Song(Artist("A", "B"), Album("C", True, [2020]), 100.0))
        s = str(p)
        assert "\n" not in s


# =============================================================================
#  Integration / end-to-end tests
# =============================================================================

class TestIntegration:

    def test_full_workflow_before_sort_insertion_order(self):
        """Tracks should appear in insertion order before sorting."""
        kendrick = Artist("Kendrick Lamar", "Hip-Hop")
        alanis   = Artist("Alanis Morissette", "Alternative")
        rogan    = Artist("Joe Rogan", "Comedy")
        koenig   = Artist("Sarah Koenig", "Journalism")

        humble          = Song(kendrick, Album("DAMN.", True,  [2017, 2018]), 220.0)
        you_oughta_know = Song(alanis,   Album("Jagged Little Pill", False, [1995, 1996]), 245.0)
        jre_ep          = Podcast(rogan,  Album("The Joe Rogan Experience", True,  [2009, 2010]), 9000.0, is_explicit=True)
        serial_ep       = Podcast(koenig, Album("Serial", False, [2014, 2015]), 5400.0)

        p = Playlist()
        for track in [humble, you_oughta_know, jre_ep, serial_ep]:
            p.add_track(track)

        before = p.tracks
        assert before[0].album.title == "DAMN."
        assert before[1].album.title == "Jagged Little Pill"
        assert before[2].album.title == "The Joe Rogan Experience"
        assert before[3].album.title == "Serial"

    def test_full_workflow_after_sort_order(self):
        """After sorting, tracks must appear in ascending release-year order."""
        kendrick = Artist("Kendrick Lamar", "Hip-Hop")
        alanis   = Artist("Alanis Morissette", "Alternative")
        rogan    = Artist("Joe Rogan", "Comedy")
        koenig   = Artist("Sarah Koenig", "Journalism")

        humble          = Song(kendrick, Album("DAMN.", True,  [2017, 2018]), 220.0)
        you_oughta_know = Song(alanis,   Album("Jagged Little Pill", False, [1995, 1996]), 245.0)
        jre_ep          = Podcast(rogan,  Album("The Joe Rogan Experience", True,  [2009, 2010]), 9000.0, is_explicit=True)
        serial_ep       = Podcast(koenig, Album("Serial", False, [2014, 2015]), 5400.0)

        p = Playlist()
        for track in [humble, you_oughta_know, jre_ep, serial_ep]:
            p.add_track(track)

        p.sort_by_release_year()
        after = p.tracks

        assert after[0].album.title == "Jagged Little Pill"
        assert after[1].album.title == "The Joe Rogan Experience"
        assert after[2].album.title == "Serial"
        assert after[3].album.title == "DAMN."

    def test_full_workflow_types_survive_sort(self):
        """Polymorphic types must be preserved after sorting."""
        p = Playlist()
        p.add_track(Song(
            Artist("Kendrick Lamar", "Hip-Hop"),
            Album("DAMN.", True, [2017, 2018]),
            220.0,
        ))
        p.add_track(Song(
            Artist("Alanis Morissette", "Alternative"),
            Album("Jagged Little Pill", False, [1995, 1996]),
            245.0,
        ))
        p.add_track(Podcast(
            Artist("Joe Rogan", "Comedy"),
            Album("The Joe Rogan Experience", True, [2009, 2010]),
            9000.0,
            is_explicit=True,
        ))
        p.add_track(Podcast(
            Artist("Sarah Koenig", "Journalism"),
            Album("Serial", False, [2014, 2015]),
            5400.0,
        ))

        p.sort_by_release_year()
        after = p.tracks

        assert isinstance(after[0], Song)       # Jagged Little Pill, 1995
        assert isinstance(after[1], Podcast)    # JRE, 2009
        assert isinstance(after[2], Podcast)    # Serial, 2014
        assert isinstance(after[3], Song)       # DAMN., 2017

    def test_full_workflow_dually_status_preserved(self):
        """is_explicit values must survive the sort unchanged."""
        p = Playlist()
        p.add_track(Podcast(
            Artist("Joe Rogan", "Comedy"),
            Album("The Joe Rogan Experience", True, [2009, 2010]),
            9000.0,
            is_explicit=True,
        ))
        p.add_track(Podcast(
            Artist("Sarah Koenig", "Journalism"),
            Album("Serial", False, [2014, 2015]),
            5400.0,
            # is_explicit defaults to False
        ))

        p.sort_by_release_year()
        after = p.tracks

        assert after[0].is_explicit is True    # JRE (2009) comes first
        assert after[1].is_explicit is False   # Serial (2014) comes second

    def test_full_workflow_wheel_counts(self):
        """play_time_formatted() must reflect each track's actual duration."""
        p = Playlist()
        p.add_track(Song(
            Artist("Kendrick Lamar", "Hip-Hop"),
            Album("DAMN.", True, [2017, 2018]),
            220.0,
        ))
        p.add_track(Podcast(
            Artist("Joe Rogan", "Comedy"),
            Album("The Joe Rogan Experience", True, [2009, 2010]),
            9000.0,
            is_explicit=True,
        ))

        p.sort_by_release_year()
        after = p.tracks

        # JRE (2009) is now first — HH:MM:SS
        assert after[0].play_time_formatted() == "02:30:00"
        # DAMN. (2017) is now second — MM:SS
        assert after[1].play_time_formatted() == "03:40"

    def test_full_workflow_total_play_time(self):
        """total_play_time() must work correctly on sorted tracks."""
        p = Playlist()
        p.add_track(Song(
            Artist("Alanis Morissette", "Alternative"),
            Album("Jagged Little Pill", False, [1995, 1996]),
            245.0,
        ))
        p.add_track(Podcast(
            Artist("Sarah Koenig", "Journalism"),
            Album("Serial", False, [2014, 2015]),
            5400.0,
        ))

        p.sort_by_release_year()
        after = p.tracks

        assert after[0].total_play_time(2) == pytest.approx(490.0)    # Song 245 × 2
        assert after[1].total_play_time(3) == pytest.approx(16200.0)  # Podcast 5400 × 3

    def test_how_far_with_polymorphism(self):
        """
        total_play_time() is defined once in MusicTrack and inherited by both
        Song and Podcast — calling it on a mixed list should work for all.
        """
        tracks: list[MusicTrack] = [
            Song(Artist("A", "B"),    Album("C", True,  [2000]), 180.0),
            Podcast(Artist("D", "E"), Album("F", False, [2010]), 3600.0),
            Song(Artist("G", "H"),    Album("I", True,  [2020]), 240.0),
        ]
        expected = [180.0, 3600.0, 240.0]
        for track, exp in zip(tracks, expected):
            assert track.total_play_time(1) == pytest.approx(exp)