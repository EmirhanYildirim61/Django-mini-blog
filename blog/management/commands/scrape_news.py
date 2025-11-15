import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

NEWS_URL = "https://www.ign.com/reviews/games"

try:
    ADMIN_USER = User.objects.get(pk=1)
except:
    print("Hata: ID=1 olan admin kullanıcısı bulunamadı. Lütfen bir süperkullanıcı oluşturun.")
    ADMIN_USER = None

class Command(BaseCommand):
    help = 'ign.com sitesinden en son haberleri çeker ve veritabanına ekler.'

    def handle(self, *args, **kwargs):
        if not ADMIN_USER:
            self.stdout.write(self.style.ERROR('Admin kullanıcısı bulunamadığı için işlem iptal edildi.'))
            return
        
        self.stdout.write(self.style.NOTICE('Haberler çekiliyor...'))

        driver = None

        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OD X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        # }

        try:
            driver = webdriver.Safari()
            driver.get(NEWS_URL)
            self.stdout.write(self.style.NOTICE('JavaScript\'in çalışması için 5 saniye bekleniyor...'))
            time.sleep(5)

            scroll_count = 5
            for i in range(scroll_count):
                self.stdout.write(self.style.NOTICE(f'Aşağı kaydırılıyor... ({i+1}/{scroll_count})'))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-cy='content-item']"))
            # )
            html_source = driver.page_source

            soup = BeautifulSoup(html_source, 'html.parser')
            new_cards = soup.find_all('div', attrs={'data-cy': 'content-item'})

            if not new_cards:
                self.stdout.write(self.style.WARNING('Hiç haber kartı bulunamadı. Sitenin yapısı değişmiş olabilir.'))
                return
            
            added_new_count = 0

            for card in new_cards:
                link_tag = card.find('a')
                header_tag = card.find('span', attrs={'data-cy': 'item-title'})
                summary_tag = card.find('div', attrs={'data-cy': 'item-subtitle'})

                if not (link_tag and header_tag and summary_tag):
                    continue

                news_header = header_tag.get_text().strip()
                news_summary = summary_tag.get_text().strip()
                news_link = link_tag['href']

                if news_link.startswith('/'):
                    news_link = "http://www.ign.com" + news_link

                try:
                    Post.objects.create(
                        title=news_header,
                        content=news_summary,
                        author=ADMIN_USER,
                        source_url=news_link
                    )
                    added_new_count += 1
                except Exception as e:
                    pass
            self.stdout.write(self.style.SUCCESS(f'İşlem tamamlandı. {added_new_count} yeni haber eklendi.'))
        
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Siteye bağlanırken bir hata oluştu: {e}'))

        finally:
            if driver:
                driver.quit()