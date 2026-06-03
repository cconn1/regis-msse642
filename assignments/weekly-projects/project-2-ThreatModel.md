# Vulnerability Analysis - Threat MOdel
**MSSE 642 — Hands-On Assignment #2**<br>
**Authors:** Mike Olson & Clayton Conn <br>
**Date:** 2026-05-29

---

# Part 1: Secure Design Document

## 1. High-Level Project Description

The Hiking Club app connects Georgia Hiking Club members with trip leaders running hikes across Atlanta, the surrounding region, and destinations worldwide, welcoming members of all ages and fitness levels. Hikes are rated by difficulty so members can match their skill level to events before registering. The club is a non-profit, all-volunteer organization with no physical office; the web application is the core of the entire business, maintained by a single CTO. Member profiles store medical conditions and fitness notes that trip leaders use to screen registrations, making confidentiality a central requirement. The app also handles payment collection for annual membership dues and paid excursions, meaning financial data is a key asset to protect.

## 2. Organization Description

The Georgia Hiking Club (GHC) is a non-profit organization based in Alanta, Georgia. The mission of GHC is to connect residents and visitors with guided hiking experiences across the region and beyond. The club operates entirely through volunteers with no salaried positions and no physical office. Club officers manage day-to-do operations, including the CTO who is responsible for maintaining the web server and application. The club's is funded through business sponsors and annual membership fees paid by members. The web application is the business, all communication, registration, payment and record keeping flows through it. The reliability and security of the application directly determine the clubs ability to operate. 

## 3. Deployment Environment

The Georgia Hiking Club application is deployed on a cloud hosting platform (e.g., AWS or similar) managed by the CTO. The architecture separates public-facing and private components across two network tiers. The front-end web server sits in a public subnet and serves the member, admin, and guest web clients over HTTPS. The backend database server is isolated in a private subnet with no direct public internet access, accessible only from the web server via firewall rules. TLS certificates are provisioned on the web server to encrypt all data in transit. Payment processing is handled by a third-party PCI DSS-compliant payment processor; card data never touches the club's own servers. Automated backups of the database are scheduled nightly and retained for 2 years.

## 4. Secure Concepts Applicable to the Hiking Club Application

### 4.1 Authentication & Access Control

The GHC design document notes that complex passowrds are not enforces and that the site had been previously compromised through a brute-force attack. Authentication has become a high-priority security concern for this application. Without password complexity requiremnts or rate limiting an attacker is met with little resistance to no resistance.

A contributing factor to brute force vulnerability is weakness within the login page itself. In chapter 23, Hoffman explains that when applications return distinct error messages to incorrect login attempts, differences can confirm email addresses that match user accounts. The two variable guessing has now been diminshed into a one variable problem. A simple fix is generic login error messages, complex password requiremnts, and a rate limit for login attempts. 

### 4.2 Confidentiality & Data Protection

The hiking club app stores two main categories of sensitive user data, member medical conditions and fitness notes. System misconfiguration or a comprimised account both represnt a safety risk. 

Data protection is managed through user authorization and the rule of least privlige. Relating to the hiking club app, only admin users and trip leaders should have access to that specific data. Hoffman identifies that trust-by-default is a recurring anti-pattern when it comes to authorization. The fix to such an issue is that the server must derive the user's role upon every request. Role checks should never rely on data supplied by the client. Leas privlige applies to event rosters as well, team leaders should only be able to view medical information of members who are attending their event. 

### 4.3 Data Integrity & Tamper Detection

Payment data and event records must be protected from unauthorized modification and access. Payment specific data is left to a third party, so payment data never touches the hiking club servers. 

Data integrity vulnerabilities come into play when considering CSRF and SQL injection attacks. Both attacks can give bad actors the ability to modify and corrupt private hiking club data. 

### 4.4 Audit & Accountability

Audit logging gives GHC the ability to maintain a record of all actions within the application. Without it, actions taken within the system are unverifiable after the fact. This protects from the repudiation threat within the STRIDE model, the ability to take an action and credibly claim it never happend.

All admin actions should be logged with the admin users ID, a timestamp, and affected resource. 

### 4.5 Availability & Resilience

The brute-force attack documented in the design document is also a Denial of Service threat (DoS). Automated scripts consume server resources slowing or even crashing the system. With no fallback system, sustained unavailiabilty means a near halt in business. 

Rate liiting and account lockouts on the login endpoint are a primary defense. Cloud-based DDoS protection handles high volume attacks within the infrastructure, and session timeouts reduce token exposure. 
---

# Part 2: Hiking Club Threat Model Assessment

## Architectural Description of Software System

### System Components

- Front End Web Server
- Backend Database Server
- Admin Web Client (HTML)
- Member Web Client (HTML)
- Guest Web Client (HTML)

### Front End Web Server

#### Guest Browsing
- Functionality and user stories

#### Authentication
- Member and admin authentication mechanisms

#### Authorization
- Permission controls by role

### Backend Database Server

[Database isolation and firewall requirements]

### Admin Client

#### Trip Leader Permissions
- a. Event creation and management
- b. CRUD operations on own events
- c. Member status tracking
- d. Waitlist management
- e. Member removal
- f. Confidential member information access
- g. Member reporting
- h. Event capacity settings

#### System Admin Permissions
- a. User account management
- b. Trip leader account management
- c. Database integrity checks
- d. Payment portal setup
- e. Treasury portal access

### Member Client

- Event viewing and registration
- Profile management
- Limited member information access

### Guest Client

- Public event listings
- No authentication required

---

## Deliverable Part 2A: Architecture Diagram

### Diagram Components

1. Systems and Components
   - a. Front End Web Server
   - b. Backend Database Server
   - c. Member Client
   - d. Admin Client
   - e. Firewall(s)
   - f. At least two networks
   - g. IP addresses (public and private)

2. Data Flow
   - Arrows showing communication between components

3. Trust Boundaries
   - Dashed lines depicting boundaries

[INSERT DIAGRAM HERE]

---

## Deliverable Part 2B: STRIDE Threat Model

### Threat 1: Spoofing Identity

[Description of how attackers could impersonate users or systems - paragraph discussing the threat in context of Hiking Club]

### Threat 2: Tampering with Data

[Description of unauthorized modification - payment data, event details, member profiles]

### Threat 3: Repudiation of Actions

[Description of denial of actions - administrative actions, financial transactions]

### Threat 4: Information Disclosure

[Description of unauthorized access - medical information, financial data, member profiles]

### Threat 5: Denial of Service

[Description of system unavailability - brute force attacks, resource exhaustion]

### Threat 6: Elevation of Privilege

[Description of unauthorized permission escalation - member accessing admin functions]

---

## Deliverable Part 2C: OWASP Threat Model

### 1. Assessment Scope — What's on the Line?

[Description of assets at risk, data involved, critical functions, business impact]

#### Critical Assets
- Member data (medical conditions, fitness levels)
- Payment information
- Event management systems
- User account credentials

#### Business Impact
- Loss of trust
- Financial fraud
- Safety risks to hikers
- Operational disruption

### 2. Vulnerabilities — What Are They?

[Identification of specific weaknesses and potential attack vectors]

#### Authentication Vulnerabilities
- Weak password enforcement
- No multi-factor authentication
- Session hijacking risks

#### Authorization Vulnerabilities
- Insufficient role-based access control
- Privilege escalation opportunities

#### Data Protection Vulnerabilities
- Unencrypted sensitive data
- SQL injection risks
- Insecure payment handling

#### Infrastructure Vulnerabilities
- Public database access
- Insufficient firewall rules
- No DDoS protection

### 3. Countermeasures — What Can You Do About It?

[Solutions and mitigation strategies for each vulnerability]

#### Authentication Controls
- Enforce strong password policies
- Implement multi-factor authentication
- Secure session management with timeouts

#### Authorization Controls
- Implement role-based access control
- Enforce ownership boundaries for events
- Regular access audits

#### Data Protection Controls
- Encrypt data in transit (TLS/SSL)
- Encrypt sensitive data at rest
- Use parameterized queries to prevent SQL injection
- Integrate PCI DSS-compliant payment processor

#### Infrastructure Controls
- Isolate database in private network
- Implement firewall rules
- Add DDoS protection and rate limiting
- Implement comprehensive logging and monitoring

### 4. Prioritized Risks — List Them in Order

#### Priority 1 (Critical)
- [Highest risk threat - explain why critical]
- Impact: [potential damage]
- Likelihood: [probability of occurrence]
- Remediation: [action to take]

#### Priority 2 (High)
- [High risk threat]
- Impact: [potential damage]
- Likelihood: [probability of occurrence]
- Remediation: [action to take]

#### Priority 3 (Medium)
- [Medium risk threat]
- Impact: [potential damage]
- Likelihood: [probability of occurrence]
- Remediation: [action to take]

#### Priority 4 (Low)
- [Lower risk threat]
- Impact: [potential damage]
- Likelihood: [probability of occurrence]
- Remediation: [action to take]

---

## References