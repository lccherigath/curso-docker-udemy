import psycopg2
import redis
import json
import os
# from bottle import route, run, request
from bottle import Bottle, request

# @route('/', method='GET')
# def test():
#   return 'app ok'

class Sender(Bottle):
  def __init__(self):
    super().__init__()
    self.route('/', method='POST', callback=self.send)

    redis_host = os.getenv('REDIS_HOST', 'queue')
    self.fila = redis.StrictRedis(host=redis_host, port=6379, db=0)

    # variavel = os.getenv('VARIAVEL', 'valor_padrao_caso_nao_encontrada')
    db_host = os.getenv('DB_HOST', 'db')
    db_user = os.getenv('DB_USER', 'postgres')
    db_name = os.getenv('DB_NAME', 'sender')
    # Data Source Name
    DSN = f'dbname={db_name} user={db_user} host={db_host}'
    self.conn = psycopg2.connect(DSN)

  def register_message(self, assunto, mensagem):
    SQL = 'insert into emails (assunto, mensagem) values (%s, %s)'
    # conn = psycopg2.connect(DSN)
    cur = self.conn.cursor()
    cur.execute(SQL, (assunto, mensagem))
    self.conn.commit()
    cur.close()
    # conn.close()

    # Redis
    msg = {'assunto': assunto, 'mensagem': mensagem}
    self.fila.rpush('sender', json.dumps(msg))

    print('Mensagem registrada!')

  # @route('/', method='POST')
  def send(self):
    assunto = request.forms.get('assunto')
    mensagem = request.forms.get('mensagem')

    self.register_message(assunto, mensagem)

    return f'Mensagem enfileirada! Assunto: {assunto} Mensagem: {mensagem}'


if __name__ == '__main__':
  sender = Sender()
  sender.run(host='0.0.0.0', port=8080, debug=True)
