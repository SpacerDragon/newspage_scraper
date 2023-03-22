# web scraper to get news from some newschannels
# designed for those who don't read a lot of news
# feel free to copy and make your own changes.

# Author: Per Idar Rød
# Creation date: 24.02.2023
# Contact me on email: post@peridar.net


# importing modules needed
import pandas as pd
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from users import user_dict
from tabulate import tabulate
from datetime import date

# uncomment this line and move these to another file for privacy
# from creds import sender_email, password, sender_server

# or just put in the real info here.
# dymmy-creds replace with real data
sender_email = 'sender@gmail.com'
password = 'password'
sender_server = 'smpt.outlook.com'


# ---- main class to get the data from news pages.-------------
class Newspaper:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def get_soup(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/58.0.3029.110 Safari/537.36"}
        response = requests.get(self.url, headers=headers)
        # webpage = response.content
        if response.ok:
            self.soup = BeautifulSoup(response.content, "html.parser")
        else:
            print('Failed to retrieve data from', self.url)
            return

    def get_data(self):
        raise NotImplementedError


# ----- Child classes for each news page ----------------------
# using set in each of these to avoid duplicate entries

# get news from dagen
class Dagen(Newspaper):
    def __init__(self):
        super().__init__('https://www.dagen.no/')
        self.get_soup()

    def get_data(self):
        dagen = []
        seen_headlines = set()
        if self.soup:
            articles = self.soup.find_all('article', 'teaser')[:10]
            if len(dagen) == 0:
                for article in articles:
                    title = article.find('h3').text.strip()
                    link = article.find('a')['href']
                    if title not in seen_headlines:
                        dagen.append([title, link])
                        seen_headlines.add(title)
                        if len(dagen) >= 5:
                            break
        return dagen


# get news from Haugesunds Avis
class H_avis(Newspaper):
    def __init__(self):
        super().__init__('https://www.h-avis.no/avaldsnes/')
        self.get_soup()

    def get_data(self):
        h_avis = []
        seen_headlines = set()
        if self.soup:
            articles = self.soup.find_all('article', 'teaser_container')[:10]
            if len(h_avis) == 0:
                for article in articles:
                    title = article.find('h2').text.strip().replace('\n', ' ')
                    link = article.find('a')['href']
                    if title not in seen_headlines:
                        h_avis.append([title,
                                       'https://www.h-avis.no/avaldsnes'
                                       + link])
                        seen_headlines.add(title)
                        if len(h_avis) >= 5:
                            break
        return h_avis


# get news from Jærbladet
class Jbl(Newspaper):
    def __init__(self):
        super().__init__('https://www.jbl.no')
        self.get_soup()

    def get_data(self):
        jbl = []
        seen_headlines = set()
        if self.soup:
            articles = self.soup.find_all('article')[:10]
            for article in articles:
                title = article.find('a').find('h2').text
                link = article.find('a')['href']
                # print(title)
                # print('https://www.jbl.no' + link)
                if title and link:
                    if title not in seen_headlines:
                        jbl.append([title, 'https://www.jbl.no' + link])
                        seen_headlines.add(title)
                        if len(jbl) >= 5:
                            break
        return jbl


# get news from Jerusalem Post
class Jerusalem(Newspaper):
    def __init__(self):
        super().__init__('https://www.jpost.com/breaking-news')
        self.get_soup()

    def get_data(self):
        jerusalem = []
        seen_headlines = set()
        if self.soup:
            # print(self.soup)
            articles = self.soup.find_all('div',
                                          'breaking-news-link-container')[:10]
            for article in articles:
                title = article.find('a')['title']
                link = article.find('a')['href']
                if title and link:
                    if title not in seen_headlines:
                        jerusalem.append([title, link])
                        seen_headlines.add(title)
                        if len(jerusalem) >= 5:
                            break
        return jerusalem


# get news from Os og Fusa posten
class Os_Fusa_Posten(Newspaper):
    def __init__(self):
        super().__init__('https://www.osogfusa.no/')
        self.get_soup()

    def get_data(self):
        os_fusa = []
        seen_headlines = set()
        if self.soup:
            articles = self.soup.find_all('article', 'teaser')[:10]
            for i in articles:
                title = i.find('h3').text.strip()
                link = i.find('a')['href']
                if title not in seen_headlines:
                    os_fusa.append([title, link])
                    seen_headlines.add(title)
                    if len(os_fusa) >= 5:
                        break

        return os_fusa


# get news from Ringerikes Blad
class Ringblad(Newspaper):
    def __init__(self):
        super().__init__('https://www.ringblad.no/')
        self.get_soup()

    def get_data(self):
        ringblad = []
        seen_headlines = set()
        if self.soup:
            articles = self.soup.find_all('article')[:10]
            for article in articles:
                title = article.find('h2').text
                link = article.find('a')['href']
                if title not in seen_headlines:
                    ringblad.append([title, 'https://www.ringblad.no' + link])
                    seen_headlines.add(title)
                    if len(ringblad) >= 5:
                        break

        return ringblad


# get news from vg
class VG(Newspaper):
    def __init__(self):
        super().__init__('https://www.vg.no/')
        self.get_soup()

    def get_data(self):
        vg = []
        seen_headlines = set()
        if self.soup:
            articles = self.soup.find_all('div', 'article-container')[:10]
            for article in articles:
                title = article.find('h2').text.replace('\n', ' ')
                link = article.find('a')['href']
                if title not in seen_headlines:
                    vg.append([title, link])
                    seen_headlines.add(title)
                    if len(vg) >= 5:
                        break
        return vg


# Wall Street Journal
class Wsj(Newspaper):
    def __init__(self):
        super().__init__('https://www.wsj.com')
        self.get_soup()

    def get_data(self):
        wsj = []
        seen_headlines = set()
        if self.soup:
            articles = self.soup.find_all('article')[:10]
            for article in articles:
                if article.find('a').text and article.find('a')['href']:
                    title = article.find('a').text.strip()
                    link = article.find('a')['href']
                    if title not in seen_headlines:
                        wsj.append([title, link])
                        seen_headlines.add(title)
                        if len(wsj) >= 5:
                            break
        return wsj


# ---- Fuctions -----------------

# create dataframe


def make_df(data, names):
    if data:
        df = pd.DataFrame(data, columns=names)
        pd.set_option('display.colheader_justify', 'left', 'max_colwidth', 50)

        return df
    else:
        return


# some css for the email
css = """
<style>
table {
    border-collapse: collapse;
    margin-bottom: 20px;
}
th, td {
    padding: 8px;
    text-align: left;
}
th {
    background-color: #dddddd;
}
td {
    border: 1px solid #dddddd;
}
td:first-child {
    width: 30%;
}
td:last-child {
    width: 80%;
}
</style>
"""


# sending mail function
def send_mail(user_email, dataframes):

    message = MIMEMultipart()
    message['Subject'] = "Nyheter"
    message['From'] = sender_email
    message['To'] = user_email

    # Get the current date
    today = date.today().strftime('%d.%m.%Y')

    # Add headline to the message
    headline = MIMEText(f'<h2>Dagens Nyheter {today}</h2><br>', 'html')
    message.attach(headline)

    # main message = dataframes
    for dataframe in dataframes:
        # Convert DataFrame to HTML table
        html = MIMEText(css + dataframe.to_html(index=False, border=1), 'html')
        message.attach(html)

    # footer
    footer = MIMEText(
        '<h3><br>Ha en fin dag.<br>Mvh Per Idar.</h3>\
        <br><br><br><br><br><br><br>', 'html')
    message.attach(footer)

    # send mail
    with smtplib.SMTP(sender_server, 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, user_email, message.as_string())


# function to get dataframes from each newspaper
def get_df_from_newspaper(obj, newspaper_name, column_names):
    obj.get_soup()
    newspaper_data = obj.get_data()
    df = make_df(newspaper_data, column_names)
    if df is not None:
        print(f'\n{newspaper_name}')
        print(tabulate(df, tablefmt='rounded_grid',
                       maxcolwidths=[50, 100], showindex=False))
    return df


def main():

    # create empty dictionary
    df_dict = {}

    # fill the dataframes with news
    # Dagen
    df_dagen = get_df_from_newspaper(Dagen(), 'Dagen', ['Dagen', 'Link'])
    if df_dagen is not None:
        df_dict['dagen'] = df_dagen

    # Haugesunds avis
    df_h_avis = get_df_from_newspaper(H_avis(), 'Haugesunds Avis',
                                      ['Haugesunds Avis - Avaldsnes', 'Link'])
    if df_h_avis is not None:
        df_dict['h_avis'] = df_h_avis

    # Jerusalem Post
    df_jerusalem = get_df_from_newspaper(Jerusalem(), 'Jerusalem Post',
                                         ['Jerusalem Post', 'Link'])
    if df_jerusalem is not None:
        df_dict['jerusalem'] = df_jerusalem

    # Jærbladet
    df_jbl = get_df_from_newspaper(Jbl(), 'Jærbladet',
                                   ['Jærbladet', 'Link'])
    if df_jbl is not None:
        df_dict['jbl'] = df_jbl

    # Os og Fusa posten
    df_os_fusa = get_df_from_newspaper(Os_Fusa_Posten(), 'Os og Fusa Posten',
                                       ['Os og Fusa Posten', 'Link'])
    if df_os_fusa is not None:
        df_dict['os_fusa'] = df_os_fusa

    # Ringerikes Blad
    df_ringblad = get_df_from_newspaper(Ringblad(), 'Ringerikes Blad',
                                        ['Ringerikes Blad', 'Link'])
    if df_ringblad is not None:
        df_dict['ringblad'] = df_ringblad

    # VG
    df_vg = get_df_from_newspaper(VG(), 'VG', ['VG', 'Link'])
    if df_vg is not None:
        df_dict['vg'] = df_vg

    # Wall Street Journal
    df_wsj = get_df_from_newspaper(Wsj(), 'Wall Street Journal',
                                   ['Wall Street Journal', 'Link'])
    if df_wsj is not None:
        df_dict['wsj'] = df_wsj

    # -------------------------------------------

    # check for dataframes
    for df, key in [(df_dagen, 'dagen'), (df_h_avis, 'h_avis'),
                    (df_jerusalem, 'jerusalem'), (df_jbl, 'jærbladet'),
                    (df_os_fusa, 'os_fusa'), (df_ringblad, 'ringblad'),
                    (df_vg, 'vg'), (df_wsj, 'wsj')]:
        if df is not None:
            df_dict[key] = df

    # Loop over the users and their newspapers
    for _, data in user_dict.items():
        news = data['newspapers']
        user_email = data['email']
        user_dataframes = []

        # loop through and find out what newspapers, and how many
        # headlines each user wants for each newspaper
        for news, num_headlines in news.items():
            if news in df_dict:
                df_subset = df_dict[news].head(num_headlines)\
                    .reset_index(drop=True)
                user_dataframes.append(df_subset)

        # send each user their news
        if user_dataframes:
            send_mail(user_email, user_dataframes)
            print('E-mail sent')
        else:
            print('E-mail sending failed')

    print('Finished')


if __name__ == '__main__':
    main()

