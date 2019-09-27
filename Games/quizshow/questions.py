from sqlalchemy import create_engine

CHOICES = ['red', 'green', 'blue', 'yellow']

class Question():

  def __init__(self, **kwargs):
    self.question = kwargs['question']
    self.id = kwargs['id']
    self.correct = kwargs['correct']
    self.answers = {}
    for c in CHOICES:
      self.answers[c] = kwargs[c]

  def checkAnswer(self, ans):
    return ans == self.correct

  def __eq__(self, o):
    return self.checkAnswer(o)

  def show(self):
    print('''
    Question: %s
    Correct answer: %s
    Red: %s
    Green: %s,
    Blue: %s,
    Yellow: %s
    ''' % (self.question, self.correct, self.answers['red'], self.answers['green'], self.answers['blue'], self.answers['yellow']))

def getQuestions(url):
  # 'sqlite:///quizShow.db'
  dbConnect = create_engine(url)
  dbConnection = dbConnect.connect()

  # If the number of rows marked used is greater than or equal to the number of rows avaliable, then reset all the rows
  if dbConnection.execute('SELECT COUNT(has_been_used) FROM go_time_trivia WHERE has_been_used=1').scalar() >= dbConnection.execute('SELECT COUNT(*) FROM go_time_trivia;').scalar():
    print('Resetting database...')
    dbConnection.execute('UPDATE go_time_trivia SET has_been_used = 0')

  query = dbConnection.execute('SELECT g.rowid, g.QUESTION, g.yellow, g.green, g.red, g.blue, g.correct_answer FROM go_time_trivia AS g WHERE g.has_been_used = 0 ORDER BY RANDOM() ASC')

  for r in query:
    dbConnection.execute('UPDATE go_time_trivia SET has_been_used = 1 WHERE rowid = %s;' % r['rowid'])
    yield Question(id=r['rowid'], red=r['red'], blue=r['blue'], green=r['green'], yellow=r['yellow'], correct=r['correct_answer'], question=r['question'])
