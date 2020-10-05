FROM python
WORKDIR /app
ENV DISCORD_BOT_TOKEN="unk" 
COPY . .
RUN pip install -r requirements.txt
CMD python pollutionbot.py
