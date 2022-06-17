import os, pytest, datetime
from vk_url_scraper import VkScraper
from .util import assert_equal_lists

vks = None

def test_login_fail():
    with pytest.raises(Exception) as exc_info:
        VkScraper("invalid", "combination")


def test_login_success():
    global vks
    vks = VkScraper(os.environ["VK_USERNAME"], os.environ["VK_PASSWORD"])


def test_scrape_empty_urll():
    assert [] == vks.scrape("something")


def test_scrape_wall_url_with_text_only():
    res = vks.scrape("https://vk.com/wall-1_398461")
    assert len(res) == 1
    assert res[0]["id"] == "wall-1_398461"
    assert res[0]["text"] == "[https://vk.com/wall-1_394596|Ранее] мы писали о жизненном цикле версий: vk.com/dev/constant_version_updates. Например, от поддержки версии API 5.50 должны были отказаться 1 сентября прошлого года, а от версии 5.80 — 14 октября. \n\nОбстоятельства сложились иначе — время отказаться от старых версий пришло только сейчас.\n\nС 19 августа 2021 года закончится срок жизни версий ниже 5.41.\nС 26 августа 2021 года перестанут поддерживаться версии ниже 5.61.\nСо 2 сентября 2021 года прекратится поддержка версий ниже 5.81.\n\nПожалуйста, успейте подготовиться к изменениям и убедиться, что в ваших приложениях ничего не сломается. Напомним, что с повышением версии у запросов может измениться формат ответов. Обо всех таких изменениях мы пишем [https://vk.com/dev/versions|здесь]."
    assert res[0]["datetime"] == datetime.datetime(2021, 8, 6, 13, 32, 26)
    assert len(res[0]["attachments"]) == 0


def test_scrape_wall_url_with_one_photo():
    res = vks.scrape("https://vk.com/wall-1_399495")
    assert len(res) == 1
    assert res[0]["id"] == "wall-1_399495"
    assert res[0]["text"] == "Делимся расписанием конкурса [https://vk.com/wall-1_399468|«Код Петербурга»]. Все важные этапы — на одной схеме \n\nЕсли участвуете, обязательно сохраните себе. Так будет удобнее планировать работу над проектом, и вы точно не упустите лучший момент для отправки сервиса на модерацию."
    assert res[0]["datetime"] == datetime.datetime(2022, 6, 8, 13, 42)
    assert len(res[0]["attachments"]) == 1
    assert len(res[0]["attachments"].keys()) == 1
    assert list(res[0]["attachments"].keys()) == ["photo"]



def test_scrape_wall_url_with_photos():
    res = vks.scrape("https://vk.com/wall-120027872_473324")
    assert len(res) == 1
    assert res[0]["id"] == "wall-120027872_473324"
    assert res[0]["text"] == "Хабаровск\nАллея героев\nПомолимся об укокоении воинов:\nАлександра, Игоря, Эдуарда, \nДионисия, Евгения, Александра, Артемия, Иннокентия, Андрея."
    assert res[0]["datetime"] == datetime.datetime(2022, 6, 15, 12, 37, 24)
    assert len(res[0]["payload"]) == 16
    assert len(res[0]["attachments"].keys()) == 1
    assert list(res[0]["attachments"].keys()) == ["photo"]
    assert len(res[0]["attachments"]["photo"]) == 9



def test_scrape_wall_url_with_photos_inner_videos_and_links_with_inner_photos():
    res = vks.scrape("https://vk.com/asdasdasd?w=wall-17315087_74182")
    assert len(res) == 1
    assert res[0]["id"] == "wall-17315087_74182"
    assert res[0]["text"] == ""
    assert res[0]["datetime"] == datetime.datetime(2022, 3, 24, 12, 1, 9)
    assert len(res[0]["payload"]) == 15
    assert len(res[0]["attachments"].keys()) == 3
    assert_equal_lists(
        list(res[0]["attachments"].keys()),
        ["photo", "link", "video"]
    )
    assert len(res[0]["attachments"]["photo"]) == 5
    assert len(res[0]["attachments"]["link"]) == 1
    assert len(res[0]["attachments"]["video"]) == 1


def test_scrape_photo_only():
    res = vks.scrape("https://vk.com/apiclub?z=photo-1_457242435%2Falbum-1_00%2Frev")
    assert len(res) == 1
    assert res[0]["id"] == "photo-1_457242435"
    assert res[0]["text"] == "Делимся расписанием конкурса [https://vk.com/wall-1_399468|«Код Петербурга»]. Все важные этапы — на одной схеме \n\nЕсли участвуете, обязательно сохраните себе. Так будет удобнее планировать работу над проектом, и вы точно не упустите лучший момент для отправки сервиса на модерацию."
    assert res[0]["datetime"] == datetime.datetime(2022, 6, 7, 11, 43)
    assert len(res[0]["payload"]) == 15
    assert len(res[0]["attachments"].keys()) == 1
    assert list(res[0]["attachments"].keys()) == ["photo"]
    assert len(res[0]["attachments"]["photo"]) == 1

def test_scrape_video_only():
    res = vks.scrape("https://vk.com/video38556806_456251917?list=ba2b77043648ff3789")
    assert len(res) == 1
    assert res[0]["id"] == "video38556806_456251917"
    assert res[0]["datetime"] == datetime.datetime(2022, 3, 24, 6, 42, 38)
    assert len(res[0]["payload"]) == 31
    assert len(res[0]["attachments"].keys()) == 1
    assert list(res[0]["attachments"].keys()) == ["video"]
    assert 'G4YDIOBUGQ3DKMQ' in res[0]["attachments"]["video"][0]

def test_scrape_video_only2():
    res = vks.scrape("https://vk.com/video-1_456239018")
    print(res[0]["attachments"]["video"][0])