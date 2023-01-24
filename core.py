from googleapiclient.errors import HttpError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configparser import ConfigParser
from gphotospy import authorize
from gphotospy.album import *
from gphotospy.media import *
import os
import requests
from PIL import Image


class Core:

    def __init__(self):
        self.configur = ConfigParser()
        self.configur.read('config.ini')
        self.root_path = self.configur.get("general", "root_path")
        self.url = self.configur.get("general", "url")
        self.client_secret = self.configur.get("general", "secret_file")
        self.photos_service = authorize.init(self.client_secret)
        self.album_manager = Album(self.photos_service)
        self.media_manager = Media(self.photos_service)

        # configure webdriver
        self.options = Options()
        self.options.headless = False  # hide GUI
        self.options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
        self.options.add_argument("start-maximized")  # ensure window is full-screen

        self.driver = webdriver.Chrome(options=self.options)

        self._session = requests.session()

    def get_images_src(self, url):
        self.driver.get(url)

        # wait for load
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div["
                                                                                      "2]/app-root/app-layout/search"
                                                                                      "-artwork/projects-list/div")))

        self.driver.minimize_window()

        elements = self.driver.find_elements(By.CLASS_NAME, "d-block")

        link_list = []

        for element in elements:
            link_list.append(str(element.get_attribute('src')).replace("smaller_square", "large"))

        return link_list

    def download_data_by_query(self, query, amount):
        data = self.get_images_src(self.url + query)
        count = 0
        file_list = []

        for i in data:
            if count > int(amount):
                break

            url_to_get = i

            # logic to not pick up videos
            split = i.split("large")[0]
            if len(split) > 63:
                formatted = split.replace(split.split("/")[10], "")
                url_to_get = formatted[:len(formatted)-1] + "large" + i.split("large")[1]

            # download to local machine
            r = self._session.get(url_to_get, timeout=10)

            if not os.path.exists(self.root_path):
                os.mkdir(self.root_path)

            file = os.path.join(self.root_path, str(count) + ".jpg")
            with open(file, "wb") as code:
                code.write(r.content)

            # more efficient would be to read size before writing to disk, but this works
            im = Image.open(file)
            w, h = im.size
            if w <= 400 or h <= 400:
                continue

            file_list.append(file)
            count += 1

        # if we have the album id in config
        if self.configur.get("general", "album_id") != "0":
            # first remove all old items from album if the album has any
            list_iterator = list(self.media_manager.search_album(self.configur.get("general", "album_id")))
            items = []
            for item in list_iterator:
                if item is None:
                    continue
                items.append(item.get("id"))

            if len(items) > 1:
                self.album_manager.batchRemoveMediaItems(self.configur.get("general", "album_id"), items)

            # then add new items
            for file in file_list:
                self.media_manager.stage_media(file)
                self.media_manager.batchCreate(album_id=self.configur.get("general", "album_id"))
        else:
            try:
                new_album = self.album_manager.create(self.configur.get("general", "album_name"))
            except HttpError as e:
                print("Failed to create new album.\n{}".format(e))
            else:
                id_album = new_album.get("id")
                self.configur.set("general", "album_id", id_album)
                with open('config.ini', 'w') as configfile:  # save
                    self.configur.write(configfile)
                for file in file_list:
                    self.media_manager.stage_media(file)
                    self.media_manager.batchCreate(album_id=self.configur.get("general", "album_id"))
