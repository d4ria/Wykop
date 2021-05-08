def get_hate_words():
    with open('../wykop_scraper/hatebase.txt', encoding='utf-8') as f:
        hate_words = []
        for line in f:
            hate_word = line.split("Polish")[0].split('(')[0].strip()
            hate_words.append(hate_word)

    return hate_words

hate_words = get_hate_words()

curse_words = ['chuj', 'cipa', 'cipę', 'cipe', 'cipą',
'cipie', 'dopierdoli',
'dopierdolił', 'dopierdolil', 'dopierdolę', 'dopierdole', 'dopierdoli',
'dopierdolić', 'dopierdolic',
'dupa', 'dupie', 'dupą', 'dupcia', 'dupeczka', 'dupy', 'dupe', 'huj',
'jeb', 'koorwa', 'kórwa', 'kurestwo',
'kurew', 'kurwa', 'kurwaa', 'kurwami', 'kurwą', 'kurwe',
'kurwę', 'kurwie', 'kurwiska', 'kurwo', 'kurwy', 'kurwach', 'kurwami', 'kurwiarz', 'kurwiący', 'kurwica', 'kurwić', 'kurwic',
'kurwidołek', 'kurwik', 'kurwiki', 'kurwiszcze', 'kurwiszon',
'kurwiszona', 'kurwiszonem', 'kurwiszony', 'kutas', 'kutasa', 'kutasie',
'kutasem', 'kutasy', 'kutasów', 'kutasow', 'kutasach', 'kutasami', 'obsrywać', 'obsrywac', 'obsrywający',
'obsrywajacy', 'odpieprzy', 'odpieprzył',
'odpieprzyl', 'odpieprzyła', 'odpieprzyla', 'opieprzający', 'piczka', 'pieprznięty', 'pieprzniety',
'pieprzony', 'pierdel', 'pierdlu', 'pierdol', 'pierdołki', 'pierdzący', 'pierdzieć',
'pierdziec', 'pizda', 'pizdą', 'pizde', 'pizdę', 'piździe', 'pizdzie',
'pizdnąć', 'pizdnac', 'pizdu', 'pierdala',
'poruchac', 'poruchać', 'przepierdolić', 'przepierdolic', 'przypierdoli', 'przypierdolić',
'przypierdolic', 'qrwa',
'rozpierdolić', 'rozpierdolic', 'rozpierdole', 'rozpierdoli',
'rozpierducha', 'skurwić', 'skurwiel', 'skurwiela', 'skurwielem',
'skurwielu', 'skurwysyn', 'skurwysynów', 'skurwysynow', 'skurwysyna',
'skurwysynem', 'skurwysynu', 'skurwysyny', 'skurwysyński',
'skurwysynski', 'skurwysyństwo', 'skurwysynstwo', 'pieprza', 'srać', 'srac', 'srający', 'srajacy', 'srając', 'srajac', 'sraj',
'sukinsyn', 'sukinsyny', 'sukinsynom', 'sukinsynowi', 'sukinsynów',
'sukinsynow', 'śmierdziel', 'udupić',
'wkurw',  'wpizdu', 'wypieprzy',
'wypieprzyła', 'wypieprzyla', 'wypieprzył', 'wypieprzyl', 'wypierdal', 'zapieprzyć',
'zapieprzyc', 'zapieprzy', 'zapieprzył', 'zapieprzyl', 'zapieprzyła',
'zapieprzyla', 'zapieprzą', 'zapieprzy', 'zapieprzymy',
'zapieprzycie', 'zapieprzysz', 'zapierniczać',
'zapierniczający', 'zasrać', 'zasranym', 'zasrywać', 'zasrywający',
'zesrywać', 'zesrywający']

curse_words = curse_words + [
    'idiot',
    'cwel',
    'ciul',
    'grubas',
    'suka',
    'zakolak',
    'dzban',
]
