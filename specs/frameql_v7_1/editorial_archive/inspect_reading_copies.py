from pathlib import Path
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;O=W/'output';D=W/'audit'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1280,'height':1000},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content((O/'frameql_language_vnext_working_draft_v0_4.html').read_text(),wait_until='domcontentloaded')
 page.get_by_role('heading',name='9. Ordered families and contextual ordered expressions',exact=True).scroll_into_view_if_needed()
 page.screenshot(path=str(D/'language_order_preview.png'))
 page.set_content((O/'a_primer_on_frameql_v2_3_working_draft_v0_1.html').read_text(),wait_until='domcontentloaded')
 page.get_by_role('heading',name='Why Output Dimensions Are Not Always Enough',exact=True).scroll_into_view_if_needed()
 page.screenshot(path=str(D/'primer_example_preview.png'))
 page.set_content((O/'columna_o3_governed_analytical_order_v0_2.html').read_text(),wait_until='domcontentloaded')
 page.get_by_role('heading',name='2. The two levels of order',exact=True).scroll_into_view_if_needed()
 page.screenshot(path=str(D/'order_math_preview.png'))
 print('Browser page errors:',errors)
 browser.close()
