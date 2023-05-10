import datetime
import os
import tempfile

import pytest

from vk_url_scraper import VkScraper

vks = None


def test_login_fail():
    with pytest.raises(Exception):
        VkScraper("invalid", "combination")


def test_login_custom_file():
    session_filename = "test-session.json"
    VkScraper(
        os.environ["VK_USERNAME"],
        os.environ["VK_PASSWORD"],
        session_file=session_filename,
    )
    assert os.path.isfile(session_filename)
    os.unlink(session_filename)


def test_login_success():
    global vks
    vks = VkScraper(
        os.environ["VK_USERNAME"], os.environ["VK_PASSWORD"], os.environ.get("VK_TOKEN")
    )


def test_scrape_empty_urll():
    assert [] == vks.scrape("something")


def test_scrape_no_vk_parseable_info():
    assert len(vks.scrape("")) == 0
    assert len(vks.scrape("google.com")) == 0
    assert len(vks.scrape("vk.com")) == 0
    assert len(vks.scrape("vk.com/wall")) == 0
    assert len(vks.scrape("vk.com/photo")) == 0
    assert len(vks.scrape("vk.com/video")) == 0


def test_scrape_wall_url_with_text_only():
    res = vks.scrape("https://vk.com/wall-1_398461")
    assert len(res) == 1
    assert res[0]["id"] == "wall-1_398461"
    assert (
        res[0]["text"]
        == "[https://vk.com/wall-1_394596|Ранее] мы писали о жизненном цикле версий: vk.com/dev/constant_version_updates. Например, от поддержки версии API 5.50 должны были отказаться 1 сентября прошлого года, а от версии 5.80 — 14 октября. \n\nОбстоятельства сложились иначе — время отказаться от старых версий пришло только сейчас.\n\nС 19 августа 2021 года закончится срок жизни версий ниже 5.41.\nС 26 августа 2021 года перестанут поддерживаться версии ниже 5.61.\nСо 2 сентября 2021 года прекратится поддержка версий ниже 5.81.\n\nПожалуйста, успейте подготовиться к изменениям и убедиться, что в ваших приложениях ничего не сломается. Напомним, что с повышением версии у запросов может измениться формат ответов. Обо всех таких изменениях мы пишем [https://vk.com/dev/versions|здесь]."
    )
    assert str(res[0]["datetime"]) == str(datetime.datetime(2021, 8, 6, 11, 32, 26))
    assert len(res[0]["attachments"]) == 0


def test_scrape_wall_url_with_one_photo():
    res = vks.scrape("https://vk.com/wall-1_399495")
    assert len(res) == 1
    assert res[0]["id"] == "wall-1_399495"
    assert (
        res[0]["text"]
        == "Делимся расписанием конкурса [https://vk.com/wall-1_399468|«Код Петербурга»]. Все важные этапы — на одной схеме \n\nЕсли участвуете, обязательно сохраните себе. Так будет удобнее планировать работу над проектом, и вы точно не упустите лучший момент для отправки сервиса на модерацию."
    )
    assert str(res[0]["datetime"]) == str(datetime.datetime(2022, 6, 8, 11, 42))
    assert len(res[0]["attachments"]) == 1
    assert len(res[0]["attachments"].keys()) == 1
    assert list(res[0]["attachments"].keys()) == ["photo"]


def test_scrape_wall_url_with_photos():
    res = vks.scrape("https://vk.com/wall-120027872_473324")
    assert len(res) == 1
    assert res[0]["id"] == "wall-120027872_473324"
    assert (
        res[0]["text"]
        == "Хабаровск\nАллея героев\nПомолимся об укокоении воинов:\nАлександра, Игоря, Эдуарда, \nДионисия, Евгения, Александра, Артемия, Иннокентия, Андрея."
    )
    assert str(res[0]["datetime"]) == str(datetime.datetime(2022, 6, 15, 10, 37, 24))
    assert len(res[0]["payload"]) == 17
    assert len(res[0]["attachments"].keys()) == 1
    assert list(res[0]["attachments"].keys()) == ["photo"]
    assert len(res[0]["attachments"]["photo"]) == 9


def test_scrape_wall_url_with_photos_inner_videos_and_links_with_inner_photos():
    res = vks.scrape("https://vk.com/asdasdasd?w=wall-17315087_74182")
    assert len(res) == 1
    assert res[0]["id"] == "wall-17315087_74182"
    assert res[0]["text"] == ""
    assert str(res[0]["datetime"]) == str(datetime.datetime(2022, 3, 24, 11, 1, 9))
    assert len(res[0]["payload"]) == 17
    assert len(res[0]["attachments"].keys()) == 3
    for k in ["photo", "link", "video"]:
        assert k in list(res[0]["attachments"].keys())
    assert len(res[0]["attachments"]["photo"]) == 5
    assert len(res[0]["attachments"]["link"]) == 1
    assert len(res[0]["attachments"]["video"]) == 1


def test_scrape_download_multiple_media():
    res = vks.scrape("https://vk.com/w=wall-17315087_74182")

    with tempfile.TemporaryDirectory(dir="./") as tempdir:
        vks.download_media(res, tempdir)
        expect_files = {
            "wall-17315087_74182_0.jpg",
            "wall-17315087_74182_1.jpg",
            "wall-17315087_74182_2.jpg",
            "wall-17315087_74182_3.jpg",
            "wall-17315087_74182_4.jpg",
            "wall-17315087_74182_0.mp4",
        }
        found_files = set(os.listdir(tempdir))
        assert len(expect_files) == len(expect_files & found_files)


def test_scrape_photo_only():
    res = vks.scrape("https://vk.com/apiclub?z=photo-1_457242435%2Falbum-1_00%2Frev")
    assert len(res) == 1
    assert res[0]["id"] == "photo-1_457242435"
    assert (
        res[0]["text"]
        == "Делимся расписанием конкурса [https://vk.com/wall-1_399468|«Код Петербурга»]. Все важные этапы — на одной схеме \n\nЕсли участвуете, обязательно сохраните себе. Так будет удобнее планировать работу над проектом, и вы точно не упустите лучший момент для отправки сервиса на модерацию."
    )
    assert str(res[0]["datetime"]) == str(datetime.datetime(2022, 6, 7, 9, 43))
    assert len(res[0]["payload"]) == 15
    assert len(res[0]["attachments"].keys()) == 1
    assert list(res[0]["attachments"].keys()) == ["photo"]
    assert len(res[0]["attachments"]["photo"]) == 1


def test_scrape_video_only():
    res = vks.scrape("https://vk.com/video38556806_456251917?list=ba2b77043648ff3789")
    assert len(res) == 1
    assert res[0]["id"] == "video38556806_456251917"
    assert str(res[0]["datetime"]) == str(datetime.datetime(2022, 3, 24, 5, 42, 38))
    assert len(res[0]["payload"]) == 34
    assert len(res[0]["attachments"].keys()) == 1
    assert list(res[0]["attachments"].keys()) == ["video"]


def test_scrape_video_only2():
    res = vks.scrape("https://vk.com/video-17546758_456239898")
    with tempfile.TemporaryDirectory(dir="./") as tempdir:
        vks.download_media(res, tempdir)
        found_files = set(os.listdir(tempdir))
        assert "video-17546758_456239898_0.mp4" in found_files
