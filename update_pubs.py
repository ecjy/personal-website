import re, sys, io

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Remove entry #26 (conference abstract, alz.064035)
# ============================================================
anchor = '10.1002/alz.064035'
idx = content.find(anchor)
if idx < 0:
    print("ERROR: Could not find alz.064035 anchor")
    sys.exit(1)

block_start = content.rfind('<div class="pub-item">', 0, idx)
block_end = content.find('<div class="pub-item">', block_start + 1)
if block_start < 0 or block_end < 0:
    print("ERROR: Could not find entry #26 block boundaries")
    sys.exit(1)

content = content[:block_start] + content[block_end:]
print("Removed entry #26 (conference abstract alz.064035)")

# ============================================================
# 2. New paper: U-shaped resting heart rate (Brain Commun 2025)
#    Insert BEFORE the first 2025 pub-item
# ============================================================
heart_rate_paper = (
    '<div class="pub-item">\n'
    '                    <div class="pub-year">2025</div>\n'
    '                    <div class="pub-content">\n'
    '                        <div class="pub-title">"U-shaped association of resting heart rate with cognitive decline"</div>\n'
    '                        <div class="pub-authors">ESJ Tan, MA Sim, L Li, A Toh, EJY Chong, SP Chan, CN Kan, XT Tan, J Cui, S Hilal, JR Chong, MKP Lai, N Venketasubramanian, BY Tan, AM Richards, LH Ling, CLH Chen</div>\n'
    '                        <div class="pub-journal">Brain Communications 7 (6), fcaf413</div>\n'
    '                        <div class="pub-stats">\n'
    '                            <a href="https://doi.org/10.1093/braincomms/fcaf413" target="_blank" class="cite-badge" style="text-decoration: none; color: inherit; display: inline-flex; align-items: center; gap: 4px; border: 1px solid rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg> DOI: 10.1093/braincomms/fcaf413</a>\n'
    '                            <button class="pub-summary-toggle" onclick="toggleSummary(this)"><span class="toggle-icon">+</span> Summary</button>\n'
    '                        </div>\n'
    '                        <div class="pub-summary-body"><div class="pub-summary-inner">This longitudinal study examined the relationship between resting heart rate (RHR) and cognitive decline in a memory clinic cohort. A U-shaped association was identified, where both very low and very high RHR were linked to greater cognitive decline over follow-up, suggesting that extreme heart rate values may reflect underlying cardiovascular or autonomic dysfunction affecting brain health.</div></div>\n'
    '                    </div>\n'
    '                </div>\n'
    '                '
)

marker_2025 = '<div class="pub-item">\n                    <div class="pub-year">2025</div>'
first_2025 = content.find(marker_2025)
if first_2025 < 0:
    print("ERROR: Could not find first 2025 pub-item")
    sys.exit(1)

content = content[:first_2025] + heart_rate_paper + content[first_2025:]
print("Added U-shaped heart rate paper (Brain Commun 2025)")

# ============================================================
# 3. New paper: PECAM-1 cerebrovascular disease (JAHA 2024)
#    Insert BEFORE the first 2024 pub-item
# ============================================================
pecam_paper = (
    '<div class="pub-item">\n'
    '                    <div class="pub-year">2024</div>\n'
    '                    <div class="pub-content">\n'
    '                        <div class="pub-title">"Associations of Circulating Platelet Endothelial Cell Adhesion Molecule-1 Levels With Progression of Cerebral Small-Vessel Disease, Cognitive Decline, and Incident Dementia"</div>\n'
    '                        <div class="pub-authors">MA Sim, ESJ Tan, SP Chan, Y Cai, YL Chai, JR Chong, EJY Chong, C Robert, N Venketasubramanian, BY Tan, MKP Lai, S Hilal, CLH Chen</div>\n'
    '                        <div class="pub-journal">Journal of the American Heart Association 13 (22), e035133</div>\n'
    '                        <div class="pub-stats">\n'
    '                            <a href="https://doi.org/10.1161/JAHA.124.035133" target="_blank" class="cite-badge" style="text-decoration: none; color: inherit; display: inline-flex; align-items: center; gap: 4px; border: 1px solid rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg> DOI: 10.1161/JAHA.124.035133</a>\n'
    '                            <button class="pub-summary-toggle" onclick="toggleSummary(this)"><span class="toggle-icon">+</span> Summary</button>\n'
    '                        </div>\n'
    '                        <div class="pub-summary-body"><div class="pub-summary-inner">This study investigated circulating PECAM-1 (CD31) levels as a biomarker for cerebral small-vessel disease (SVD) progression in a memory clinic cohort. Higher PECAM-1 levels were associated with greater white matter hyperintensity burden, faster cognitive decline, and increased risk of incident dementia, suggesting endothelial dysfunction as a key mechanism linking vascular injury to cognitive impairment.</div></div>\n'
    '                    </div>\n'
    '                </div>\n'
    '                '
)

marker_2024 = '<div class="pub-item">\n                    <div class="pub-year">2024</div>'
first_2024 = content.find(marker_2024)
if first_2024 < 0:
    print("ERROR: Could not find first 2024 pub-item")
    sys.exit(1)

content = content[:first_2024] + pecam_paper + content[first_2024:]
print("Added PECAM-1 paper (JAHA 2024)")

# ============================================================
# Write output
# ============================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

titles = re.findall(r'class="pub-title">', content)
print("Total publications now:", len(titles))