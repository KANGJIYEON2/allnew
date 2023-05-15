import matplotlib.pyplot as plt
from wordcloud import WordCloud

plt.rcParams['font.family'] = 'Malgun Gothic'

filename = 'steve.txt'
myfile = open(filename, 'rt', encoding='utf-8')

text = myfile.read()

wordcloud = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf',
                      width=800,
                      height=800,
                      background_color='white')

wordcloud = wordcloud.generate(text)

print(type(wordcloud))
print('-' * 40)

word_freq = wordcloud.words_
print(type(word_freq))
print('-' * 40)

sorted_data = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
print(sorted_data)
print('-' * 40)

chart_data = sorted_data[:10]
print(chart_data)
print('-' * 40)

xtick = []
chart = []
for item in chart_data:
    xtick.append(item[0])
    chart.append(item[1])

mycolor = ['r', 'g', 'b', 'y', 'm', 'c', '#fff0f0', '#ccffbb', '#05ccff', '#11ccff']
plt.bar(xtick, chart, color=mycolor)
plt.title('Top 10 Word Frequencies')
filename = 'wordCloudEx01_01.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' file saved...')

plt.figure(figsize=(20, 20))
plt.imshow(wordcloud)
plt.axis('off')

filename = 'wordCloudEx01_02.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' file saved')
