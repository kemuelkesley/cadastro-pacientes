import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        # Go to login page
        await page.goto("http://localhost:8000/logar_usuario/")
        await page.wait_for_timeout(2000)
        await page.screenshot(path="static/screenshots/login.png")
        
        # Login
        await page.fill('input[name="username"]', 'admin')
        await page.fill('input[name="password"]', 'admin')
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(2000)
        
        # Dashboard
        await page.goto("http://localhost:8000/dashboard/")
        await page.wait_for_timeout(2000)
        await page.screenshot(path="static/screenshots/dashboard.png")
        
        # Pacientes (Contatos / clinica_list)
        await page.goto("http://localhost:8000/clinica_list/")
        await page.wait_for_timeout(2000)
        await page.screenshot(path="static/screenshots/pacientes.png")
        
        # Médicos
        await page.goto("http://localhost:8000/medicos/")
        await page.wait_for_timeout(2000)
        await page.screenshot(path="static/screenshots/medicos.png")
        
        # Agendamentos
        await page.goto("http://localhost:8000/listar_agendamentos/")
        await page.wait_for_timeout(2000)
        await page.screenshot(path="static/screenshots/agendamentos.png")
        
        # Financeiro
        await page.goto("http://localhost:8000/financeiro/")
        await page.wait_for_timeout(2000)
        await page.screenshot(path="static/screenshots/financeiro.png")
        
        await browser.close()

asyncio.run(run())
