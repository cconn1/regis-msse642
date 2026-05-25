# Vibe Coding Assignment #1
**OWASP A03:2025 — Software Supply Chain Failures**

*AUTHOR: CLAYTON CONN*

*CLASS: MSSE 642 - SOFTWARE ASSURANCE*

*DATE: 5/24/2026*

---

## 1. Overview: Vibe Coding Tool
 
For this assignment I used **Claude (claude.ai)** as my primary vibe coding tool. With it, I was able to create a single self-contained HTML file that opens directly in a browser. No server or install is required to run this app. 
 
I chose Claude for a few reasons. I had played around with self-contained HTML files in a few personal projects and really like the idea to give users who aren't as tech savvy the ability to double click and run the app locally. Claude handles the full stack in a single file really well with HTML, CSS and JavaScript all together. Second, I have really appreciated the workflow of conversing with Claude on what I want to build first rather than coding right away. 
 
The alternative I considered was Replit, which was used in the example SQL injection demo. Replit is excellent for shareable web apps with a live URL, but for a local educational tool that needs to run without a network connection or account, a single HTML file in VS Code in my opinion is more practical.
 
 
 ## 2. Description of the Program
 
The app is an **interactive, step-by-step supply chain attack simulator** built as a single HTML file. It covers three of the most common and impactful supply chain attackS from OWASP A03:2025:
 
1. **Typosquatting** — installing a malicious package due to a misspelled name
2. **Dependency Confusion** — a public package hijacking an internal one via version number manipulation (Birsan, 2021)
3. **Compromised Build Pipeline** — malicious code injected into CI/CD actions or build scripts
The design was intentionally modeled after the SQL injection demo from class — a side-by-side **Vulnerable vs. Secure** comparison — but extended with a **guided walkthrough format**. Instead of clicking a button and seeing an instant result, users step through each attack in three stages with Next/Back navigation, a progress bar, and step indicators. Each step includes:
 
- A narrative explanation of what's happening and why
- A simulated terminal output showing the vulnerable behavior
- A corresponding secure implementation showing how that specific step gets blocked, including real-world tooling such as GitHub Dependabot (InfoQ, 2019)


![Landing page showing the three attack tabs and the Typosquatting intro card](../images/VC1-landing-page.png)

*Figure 1. Landing page — attack selector tabs across the top, intro card with attack description, severity tags, and the step progress indicator.*


The goal was to make it feel less like reading what supply chain attacks are, and more like walking through the attack as it unfolds — so students understand *why* each control exists, not just *what* to do.

![Step 2 of the Typosquatting walkthrough — vulnerable terminal output on the left showing credential exfiltration, secure panel on the right showing the hash mismatch error](../images/VC1-typosquatting-step2.png)

*Figure 2. Typosquatting Step 2 — the vulnerable install silently exfiltrates credentials; the secure install fails with a hash mismatch before any code runs.*


![Dependency Confusion attack — Step 1 showing the public vs. private registry conflict](../images/VC1-dependency-confusion.png)

*Figure 3. Dependency Confusion Step 1 — illustrating how pip selects the attacker's higher-versioned public package over the internal one.*
 
![Attack Summary tab showing the reference table of all three attacks and defenses](../images/VC1-summary-tab.png)

*Figure 4. Summary tab — a reference table comparing all three attack types, how they work, and the key defense for each.*
## 3. The Vulnerability: A03:2025 — Software Supply Chain Failures
 
Software Supply Chain Failures is a **new entry in the OWASP Top 10 for 2025**, ranked #3 (OWASP, 2025). It covers attacks that target the tools, packages, and processes used to build software — rather than the software itself. The core idea is that modern applications depend on hundreds of third-party libraries, and compromising even one of them affects every downstream user. A simple pip install command or automated build can be sabotaged by bad actors if careful safeguards aren't included and executed. 

### Why It Matters Now
 
The attack surface has grown dramatically. The average Python project pulls in 50+ transitive dependencies — packages your direct dependencies depend on, which you likely never reviewed (Calmops, 2025). In the new world of AI as well, AI doesn't check to ensure that all dependencies and libraries added are safe. AI can unknowingly add hijacked packages and developers that don't look can let these attempts slip through. 

### Recent Attacks Using This Vulnerability
 
Two of the most significant recent attacks illustrate how severe supply chain vulnerabilities can be:
 
- **PyTorch Lightning (April 2026)** — Versions 2.6.2 and 2.6.3 of PyTorch Lightning — an open source Python framework with over 31,000 GitHub stars — were compromised as part of the "Mini Shai-Hulud" campaign. The malicious package included a hidden `_runtime` directory with an obfuscated JavaScript payload designed to steal credentials from developer environments. PyPI quarantined the project after discovery (The Hacker News, 2026; Bank Info Security, 2026).
- **Three simultaneous attacks on npm, PyPI, and Docker Hub (April 21–23, 2026)** — Three separate supply chain campaigns hit three major package registries within 48 hours, all targeting API keys, cloud credentials, SSH keys, and CI/CD pipeline tokens. The coordinated timing across multiple platforms signaled a shift toward organized supply chain hacking campaigns (GitGuardian, 2026; RapidFort, 2026).

The pattern around supply chain attacks remains consistent: malicious code gets embedded in trusted packages, and it lingers in production environments stealing valuable data. 
 
---

## 4. Problems Encountered and How I Solved Them

**Problem 1: Keeping it self-contained.**
One design constraint was that the app needed to run without a server or internet connection — just open the HTML file. I wanted it to run this way for ease of use and zero setup instructions, simply open the HTML file and you can view the fully working app.
 
**Problem 2: The initial design was too complex and hard to learn from.**
The first version of the app had seven different attack scenarios accessible via a button panel, with instant output that appeared all at once. When testing the app, it felt more like reading an interacitve textbook. With some correction, the app now steps users through supply chain attacks and how they actually work within each environment for users to understand how they worked. 

**Problem 3: The dark terminal aesthetic felt old and inaccessible.**
The first two versions used a black/green terminal color scheme that made sense for a security tool but felt tough for students to understand security concepts. I switched to a brighter academic aesthetic — cream background, navy accents, Inter and Lora typography — inspired by the Helix academic research lab template on Lovable. This made the tool feel more like a learning environment than a professional security dashboard.

## 5. References
 
Bank Info Security. (2026, May). Mass supply-chain attack slams npm and PyPI, hits Mistral AI. *Bank Info Security*. https://www.bankinfosecurity.com/mass-supply-chain-attack-slams-npm-pypi-hits-mistral-ai-a-31672
 
Birsan, A. (2021, February 9). *Dependency confusion: How I hacked into Apple, Microsoft, and dozens of other companies*. Medium. https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610
 
Calmops. (2025, December 17). *Dependency security and vulnerability scanning in Python: Protecting your supply chain*. https://calmops.com/programming/python/dependency-security-vulnerability-scanning/
 
GitGuardian. (2026, April 23). *No off season: Three supply chain campaigns hit npm, PyPI, and Docker Hub in 48 hours*. https://blog.gitguardian.com/three-supply-chain-campaigns-hit-npm-pypi-and-docker-hub-in-48-hours/
 
InfoQ. (2019, February). GitHub Dependabot brings automated security fixes to all public repos. *InfoQ*. https://www.infoq.com/news/2019/02/github-dependabot-security
 
OWASP. (2025). *OWASP Top 10:2025 — A03: Software supply chain failures*. https://owasp.org/Top10/2025/
 
RapidFort. (2026, April 4). *PyPI, npm, and the new frontline of software supply chain attacks*. https://www.rapidfort.com/blog/pypi-npm-and-the-new-frontline-of-software-supply-chain-attacks
 
The Hacker News. (2026, April). PyTorch Lightning and Intercom-client hit in supply chain attacks to steal credentials. *The Hacker News*. https://thehackernews.com/2026/04/pytorch-lightning-compromised-in-pypi.html