import aiohttp
import asyncio
import uvicorn
from fastai import *
from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
total_sum = 0
num = 0
export_file_url = 'https://drive.google.com/uc?export=download&id=1ng7FzcGT6cdYti8_ncdCY9pGXxHOSvs2'
export_file_name = 'text_classifier.pkl'

classes = ['black', 'grizzly', 'teddys']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    await download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    global total_sum, num
    req = await request.form()
    input_text= req['input-text']

    p = learn.predict(input_text)
    prediction = str(p[0])
    confidence = p[2].tolist()
    
    print("Negative Level: " + str(confidence[0]))
    print("Neutral Level: " + str(confidence[1]))
    print("Positive Level: " + str(confidence[2]))

    if prediction == "negative":
        prediction = 1
    elif prediction == "neutral":
        prediction = 3
    else:
        prediction = 5
        
    score=int(prediction)
    total_sum+=score
    num+=1
    average= round((total_sum/num),2)
    
    if prediction == 1:
        return JSONResponse({'result': "That's not nice. <br/>Rating: " + str(average)}) 
    elif prediction == 3:
        return JSONResponse({'result': "Okay.. <br/>Rating: " + str(average)})
    else:
         return JSONResponse({'result': "Keep it up! <br/>Rating: " + str(average)}) 


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
