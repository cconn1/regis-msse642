# Vulnerability Analysis - Threat MOdel
**MSSE 642 — Hands-On Assignment #2**<br>
**Authors:** Mike Olson & Clayton Conn <br>
**Date:** 2026-05-29

---

# Part 1: Secure Design Document

## 1. High-Level Project Description

[Your 1-paragraph summary here - max 5 sentences describing the Hiking Club app in your own words]

## 2. Organization Description

[Your description of the Georgia Hiking Club - its structure, volunteers, mission, revenue model, etc.]

## 3. Deployment Environment

[Your chosen deployment approach - cloud, data center, hybrid, etc. with specific details about the infrastructure]

## 4. Secure Concepts Applicable to the Hiking Club Application

### 4.1 Authentication & Access Control

[Discussion of weak passwords, brute force attacks, multi-factor authentication needs]

### 4.2 Confidentiality & Data Protection

[Discussion of medical information privacy, encrypted data in transit and at rest]

### 4.3 Data Integrity & Tamper Detection

[Discussion of payment protection, event data integrity]

### 4.4 Authorization & Least Privilege

[Discussion of role-based access control, event ownership boundaries]

### 4.5 Audit & Accountability

[Discussion of access logging, administrative action tracking]

### 4.6 Availability & Resilience

[Discussion of DoS protection, session management, backup strategies]

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