from pathlib import Path
from html import escape
import re
p=Path(__file__).parent
starter={
'Website':['Professional business website','Up to 5 pages','Custom branding','Responsive mobile/tablet/desktop design','Modern UI design','Contact page','About page','Services/products page','WhatsApp integration','Google Maps integration','Contact/enquiry form','Social media links'],
'Technical':['Domain setup','Hosting setup','SSL/HTTPS','Basic security configuration','Website backups','Basic uptime monitoring','Basic performance optimization'],
'Visibility':['Basic on-page SEO','Google Search setup','Google Business Profile assistance','Search-friendly page titles and descriptions'],
'Maintenance':['Up to 2 small update requests per month','Bug fixes','Basic technical support']}
growth={
'Website':['Up to 10 pages','Custom landing pages','Conversion-focused design','Testimonials section','FAQ section','Lead-generation forms','Booking/enquiry integration','Gallery/portfolio','Blog/news section if required'],
'SEO & Visibility':['Improved on-page SEO','Keyword-focused page structure','Google Business Profile optimization assistance','Google Search Console setup','Analytics setup','Monthly SEO/visibility check'],
'Growth':['1 landing page per month','Lead tracking','Conversion tracking','Monthly performance report','Basic content assistance','CTA optimization'],
'Maintenance':['Up to 5 small update requests per month','Bug fixes','Security updates','Backups','Uptime monitoring','Performance checks','Priority support']}
premium={
'Website':['Up to 15 pages','Advanced landing pages','Advanced forms','Booking integrations','Portfolio/catalogue functionality','Multiple service pages','Advanced CTA optimization'],
'SEO':['Advanced on-page SEO','Keyword research','Internal linking','Monthly SEO improvements','Search performance monitoring','Technical SEO checks'],
'Marketing':['2 landing pages per month','Basic social-media content assistance','Promotional campaign pages','Offer/promotion updates','Conversion optimization','Monthly strategy session'],
'Maintenance':['Up to 10 small update requests per month','Priority bug fixes','Security monitoring','Backups','Performance monitoring','Priority support'],
'Reporting':['Monthly performance report','Traffic overview','Enquiry/lead overview','Conversion observations','Recommendations for the following month']}
one_time=['Professional website','Up to 7 pages','Responsive design','Custom branding','Contact form','WhatsApp integration','Google Maps','Social links','Basic SEO','Analytics setup','Domain setup','Hosting setup','SSL','Security configuration','Website testing','Launch','30 days post-launch bug support']
plans=[
 dict(name='Starter',price='5,000',description='For businesses that need a professional online presence.',cta='Get Started',context='A professional beginning',inheritance='A complete foundation for your business.',summary=['Up to 5 custom-branded pages','Responsive design & enquiry form','WhatsApp & Google Maps integration','Basic SEO & Google Search setup','Hosting setup, SSL & backups','2 small update requests / month'],groups=starter),
 dict(name='Growth',price='8,000',description='For businesses that want their website to actively generate enquiries.',cta='Grow My Business',context='MOST POPULAR',inheritance='Everything in Starter, plus:',summary=['Up to 10 pages, built to convert','1 landing page / month','Booking & lead-generation forms','Lead tracking & conversion tracking','Monthly report & visibility check','5 small updates / month · priority support'],groups=growth),
 dict(name='Premium',price='12,000',description='For businesses that want an ongoing digital team.',cta="Let's Grow",context='Your ongoing digital team',inheritance='Everything in Growth, plus:',summary=['Up to 15 pages & advanced forms','2 landing pages / month','Advanced SEO & keyword research','Social-media content assistance','Monthly strategy session & reporting','10 small updates / month · priority care'],groups=premium)
]
def features(items):return ''.join('<li>'+escape(i)+'</li>' for i in items)
cards=[]
for i,plan in enumerate(plans):
 featured=plan['name']=='Growth'
 badge='<span class="recommendation"><span aria-hidden="true">✧</span> MOST POPULAR</span>' if featured else '<span class="plan-context">'+escape(plan['context'])+'</span>'
 details=''
 if i:details='<p class="detail-inheritance">'+escape(plan['inheritance'])+' The higher page and monthly allowances replace the previous plan’s limits.</p>'
 for category,items in plan['groups'].items():
  details+='<h4>'+escape(category)+'</h4><ul>'+features(items)+'</ul>'
 cards.append(f'''<article class="price-card{' featured' if featured else ''}" aria-labelledby="{plan['name'].lower()}-title">
 <div class="plan-position"><span class="plan-number">0{i+1} /</span>{badge}</div>
 <h3 class="plan-name" id="{plan['name'].lower()}-title">{plan['name'].upper()}</h3>
 <p class="price">₹{plan['price']}<small>/month</small></p>
 <p class="price-desc">{escape(plan['description'])}</p>
 <button class="btn {'light' if featured else 'outline'}" data-project="{plan['name']} — ₹{plan['price']}/month">{escape(plan['cta'])}<span class="arrow" aria-hidden="true">↗</span></button>
 <p class="plan-inheritance">{escape(plan['inheritance'])}</p>
 <ul class="features">{features(plan['summary'])}</ul>
 <details class="plan-details"><summary>See all {plan['name']} features<span class="detail-toggle" aria-hidden="true">+</span></summary><div class="detail-body">{details}</div></details>
 </article>''')
rows={
'Website':[
('Number of pages','Up to 5','Up to 10','Up to 15'),
('Responsive design',True,True,True),('Custom branding',True,True,True),('WhatsApp integration',True,True,True),('Google Maps',True,True,True),('Contact forms','Standard','Lead-generation','Advanced'),('Booking integration',False,True,True),('Gallery/portfolio',False,True,'Portfolio / catalogue'),('Landing pages',False,'1 / month','2 / month')],
'Technical':[
('Domain setup',True,True,True),('Hosting','Setup','Setup','Setup'),('SSL',True,True,True),('Security','Basic configuration','Security updates','Security monitoring'),('Backups',True,True,True),('Uptime monitoring','Basic',True,True),('Performance optimization','Basic','Performance checks','Ongoing monitoring')],
'SEO & Visibility':[
('Basic SEO',True,True,True),('Advanced SEO',False,False,True),('Google Business Profile assistance','Setup assistance','Optimization assistance','Optimization assistance'),('Search Console',False,True,True),('Analytics',False,True,True),('Keyword research',False,False,True),('Monthly SEO improvements',False,False,True)],
'Growth':[
('Lead tracking',False,True,True),('Conversion tracking',False,True,True),('Monthly performance report',False,True,'Expanded reporting'),('Content assistance',False,'Basic','Basic'),('Social media assistance',False,False,'Basic content assistance'),('Strategy session',False,False,'Monthly')],
'Maintenance':[
('Monthly update allowance','2 small requests','5 small requests','10 small requests'),('Bug fixes',True,True,'Priority'),('Security updates',False,True,True),('Priority support',False,True,True)]
}
def cell(v):
 if v is True:return '<span class="included" aria-hidden="true">✓</span><span class="sr-only">Included</span>'
 if v is False:return '<span class="not-included" aria-hidden="true">—</span><span class="sr-only">Not included</span>'
 return '<span class="value">'+escape(v)+'</span>'
table_bodies=''
for group,rs in rows.items():
 table_bodies+='<tbody><tr class="category"><th scope="rowgroup">'+escape(group)+'</th><td colspan="3" aria-hidden="true"></td></tr>'
 for label,*values in rs:table_bodies+='<tr><th scope="row">'+escape(label)+'</th>'+''.join('<td>'+cell(v)+'</td>' for v in values)+'</tr>'
 table_bodies+='</tbody>'
table_headers=''
for plan in plans:
 table_headers+='<th scope="col">'+('<span class="table-recommended">Most popular</span>' if plan['name']=='Growth' else '')+'<span class="table-plan">'+plan['name']+'</span><span class="table-price">₹'+plan['price']+'<small>/month</small></span></th>'
section='''<section class="section pricing-section" id="pricing" aria-labelledby="pricing-title">
<div class="section-label"><span class="number">03 /</span><span class="eyebrow">Built for your next chapter</span></div>
<div class="section-heading"><h2 id="pricing-title">Simple Pricing.<br><span>Serious Online Presence.</span></h2><p>Choose the plan that fits your business. Get a professional online presence without the large upfront cost.</p></div>
<div class="monthly-caption"><span class="eyebrow">Monthly plans</span><span>A website. Ongoing care. Room to grow.</span></div>
<div class="pricing-grid monthly-grid">'''+''.join(cards)+'''</div>
<p class="pricing-terms"><span aria-hidden="true">ⓘ</span>Before you begin, confirm domain and hosting charges, taxes, third-party tools, and subscription terms in your proposal.</p>
<div class="compare-section" aria-labelledby="compare-title">
<div class="compare-heading"><div><h3 id="compare-title">Compare Plans</h3><p>The details, side by side. Find the right fit for your business.</p></div><div class="table-legend"><b>✓</b> Included &nbsp;&nbsp; <b>—</b> Not included</div></div>
<div class="table-shell"><div class="table-scroll" role="region" aria-label="Plan comparison table. Scroll horizontally to compare all plans." tabindex="0"><table class="comparison"><caption class="sr-only">Compare Starter, Growth and Premium monthly plans by feature.</caption><colgroup><col><col><col><col></colgroup><thead><tr><th scope="col">Feature</th>'''+table_headers+'''</tr></thead>'''+table_bodies+'''</table></div></div>
<div class="table-mobile-hint"><span aria-hidden="true">↔</span> Swipe to compare · feature names stay in view</div>
<p class="table-note">Monthly page and update allowances are plan-specific, not cumulative. Growth includes a monthly SEO/visibility check; Premium adds monthly SEO improvements. Hosting refers to setup; confirm recurring charges in your proposal.</p>
</div>
<div class="one-time-section" aria-labelledby="one-time-title"><div class="one-time-heading"><h3 id="one-time-title">Prefer to Pay Once?</h3><span class="eyebrow">One project. One payment.</span></div>
<article class="one-time-card" aria-labelledby="one-time-plan-title"><div class="one-time-main"><span class="one-time-tag">One-time package · not a subscription</span><h4 id="one-time-plan-title">ONE-TIME WEBSITE</h4><p class="one-time-price">₹25,000 <small>one-time</small></p><p class="one-time-subtitle">Own your website without a monthly subscription.</p><button class="btn" data-project="One-time Website — ₹25,000">Build My Website<span class="arrow" aria-hidden="true">↗</span></button></div><div class="one-time-inclusions"><p class="eyebrow">Everything you need to launch</p><ul class="one-time-features">'''+features(one_time)+'''</ul><p class="optional-maintenance">Optional maintenance after 30 days: <strong>₹4,000/month</strong><small>Separate and optional. Your website package is a one-time purchase.</small></p></div></article>
</div></section>'''
(p/'pricing-fragment.html').write_text(section)
s=(p/'index.html').read_text()
start=s.index('<section class="section pricing-section"')
end=s.index('</section>',start)+len('</section>')
old_section=s[start:end]
s=s[:start]+section+s[end:]
css=(p/'pricing.css').read_text()+'\n#pricing .comparison .category td{background:#f1f3f6!important;border-bottom:1px solid #e1e6ed}\n'
s=s.replace('</head>','<style id="pricing-component-styles">'+css+'</style></head>',1)
options='<option>Not sure yet</option>'+''.join('<option>'+escape(plan['name']+' — ₹'+plan['price']+'/month')+'</option>' for plan in plans)+'<option>One-time Website — ₹25,000</option>'
s=re.sub(r'(<select id="plan" name="plan">).*?(</select>)',lambda m:m[1]+options+m[2],s,count=1,flags=re.S)
(p/'index.html').write_text(s)
# Isolated, self-contained preview of the component: no navbar, hero, or footer.
head=s[:s.index('</head>')+7]
head=re.sub(r'<title>.*?</title>','<title>Adolescent Studio — Pricing Plans</title>',head)
head=head.replace('</head>','<style>body{margin:0}.wrap{width:min(1240px,100%)}#pricing{border-top:0;padding-top:65px}@media(max-width:700px){#pricing{padding-top:44px}}</style></head>')
modal=s[s.index('<dialog'):s.index('<script>')]
js=(p/'motion.js').read_text()
modal_js=js[js.index('  const dialog ='):js.rindex('})();')]
preview_js="(() => { const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');const ease='cubic-bezier(.22,1,.36,1)';"+modal_js+'})();'
standalone=head+'<body><main class="wrap">'+section+'</main>'+modal+'<script>'+preview_js+'</script></body></html>'
(p/'pricing-section.html').write_text(standalone)
print('Pricing updated. Feature counts:',len(starter['Website'])+len(starter['Technical'])+len(starter['Visibility'])+len(starter['Maintenance']),sum(map(len,growth.values())),sum(map(len,premium.values())),len(one_time))
print('Comparison rows:',sum(map(len,rows.values())))
