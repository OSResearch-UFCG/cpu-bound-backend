# cpu-bound-backend

Conta quantos números primos existem de 0 até `n` usando divisão por tentativa. Todo o tempo da requisição é gasto na CPU.

Só usa a biblioteca padrão do Python 3.

```bash
python3 server.py
curl "http://localhost:8080/?n=50000"
```

A porta pode ser trocada com a variável `PORT`.
