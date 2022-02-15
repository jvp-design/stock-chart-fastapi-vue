# Stock Chart FastAPI Vue
A simple FastAPI/Vue project to fetch stock data and display in a chart on the frontend.
This code is what was used for the blog posts found at https://jeffpohlmeyer.com/series/candlestick-fastapi-vue

## Running code
To run the code locally you'll need to have Python and Node installed on your machine.
Then after pulling from git, run the following
### Server
```
cd server
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
If on linux or mac, replace `env\Scripts\activate` with `source env/bin/activate`

### Client
```
cd client
npm i
npm run dev
```
