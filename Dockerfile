# Katevasma tou episimou container me python 3.9
FROM python:3.9-slim

# Thetei to fakelo ergasias
WORKDIR /app

# Antigrafi tou requirements arxeiou sto container
COPY requirements.txt .

# Egkatastasi twn requirements
RUN pip install --no-cache-dir -r requirements.txt

# Antigrafi olou tou kwdika sto container
COPY . .

# Expose tis portas pou ekteleitai
EXPOSE 8000

# Enarxi efarmogis
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]