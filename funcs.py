import pandas as pd
from geopy import distance

# загрузка данных
def load_data():
    data = pd.read_csv('df.csv', converters={'coords':eval})
    return data

# расстояние между координатами
def get_distance(location, coords):
    return [distance.distance(location, coord).km for coord in coords]

# возвращает в виде словаря n строк с наименьшими значениями расстояния
def data_to_dicts(data, location, n=3):
    data['distance'] = get_distance(location, data['coords']) # расстояние между полученной локацией и координатами баров
    data = data.where(pd.notnull(data), None) 
    return data.nsmallest(n, 'distance').to_dict('records') # возврвщает 

# форматирование ответов
def make_answer(dicts):
    messages = []
    z = {'name':'{name}', 'address':'Адрес: {address}', 'average_rating':'Рейтинг: {average_rating} ({number_of_reviews})',
     'place_in_rating':'{place_in_rating}', 
     'award_text':'{award_text}', 'years_text':'{years_text}', 'distance_from':'{distance_from}',
     'f1':'{f1}', 'f2':'{f2}', 'f3':'{f3}',
     'start':'Работает с {start} до {end}', 'curl':'{curl}'}
    for d in dicts:
      message = ''
      for k,v in z.items():
        if d[k]:
          message += z[k].format(**d) + '\n'
      messages.append(message)
    return messages  

def get_bars(location):
    data = load_data()
    dicts = data_to_dicts(data, location)
    messages = make_answer(dicts)
    return messages
