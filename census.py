##WordCloud of bootleg performances, just out of curiosity
##The bootlegging site can be found at https://livebootlegconcert.blogspot.com/
##DISCLAIMER:
##This code does not under any conditions endorse bootlegging, as it is illegal
##and threatens the integrity of the music industry, which is already struggling
##as a result of lockdown and defunding of the arts. Please use this code with
##caution, as this brief project was purely made out of curiosity.

import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from matplotlib import pyplot as plt

URL = 'https://livebootlegconcert.blogspot.com/'

def import_artists():

    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        sidebar = BeautifulSoup(soup.find('aside').prettify(), features='lxml')
        bands = sidebar.findAll('a', {'dir': 'ltr'})
        freqs = sidebar.findAll('span', {'dir': 'ltr'})
        freq_dict = {}
        for band, freq in zip(bands, freqs):
            band_text = band.text.strip()
            if not (band_text[0] == '_' or band_text[:8] == 'Festival' or band_text == None):
                freq_int = int(freq.text.strip()[1:-1])
                freq_dict[band_text] = freq_int    
        return freq_dict

def color_func(dictionary):

    maximum = max(dictionary.values())
    def color_func_inner(word, font_size, position, orientation, random_state=None, **kwargs):
        return 'hsl(%d, 80%%, 50%%)' % (360 * dictionary[word]/maximum)
    return color_func_inner

if __name__ == '__main__':

    freq_dict = import_artists()
    print(sum(freq_dict.values()))
    wordcloud = WordCloud(background_color = 'black', width = 2000, height = 1400, color_func = color_func(freq_dict)).generate_from_frequencies(freq_dict)
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('.\wordcloud.png', dpi = 300)
    plt.show()
