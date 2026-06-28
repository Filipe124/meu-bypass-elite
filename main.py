from fastapi import FastAPI, Query
from drission_page import ChromiumPage, ChromiumOptions
import os

app = FastAPI()

@app.get("/bypass")
def bypass(url: str = Query(..., description="URL do site alvo")):
    worker_url = os.getenv('WORKER_URL')
    
    co = ChromiumOptions()
    co.set_argument('--no-sandbox')
    co.set_argument('--headless=new')
    co.set_browser_path('/usr/bin/google-chrome')
    
    # Se houver um Worker configurado, usamos como proxy
    if worker_url:
        co.set_proxy(worker_url)
        
    page = ChromiumPage(co)
    try:
        # Define o header X-Target-URL se estiver usando o Worker
        if worker_url:
            # DrissionPage lida com headers de forma diferente, 
            # aqui simulamos o acesso direto pois o bypass de rede é feito pelo Drission
            page.get(url)
        else:
            page.get(url)
            
        # Espera e tenta resolver desafios do Cloudflare (Turnstile)
        page.wait.load_start()
        
        # Procura por botões de verificação comuns
        for btn_text in ['Verify you are human', 'Sou humano', 'Verificar']:
            btn = page.ele(f'@value={btn_text}')
            if btn:
                btn.click()
                page.wait(5)
                break
                
        return {"html": page.html, "status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        page.quit()
