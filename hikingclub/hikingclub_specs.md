# Hiking Club Software Project Description

## Background

Atlanta, GA is a major metropolitan city characterized by continual business
growth and urban sprawl, resulting in long commutes for most workers. While
Atlanta has tourist attractions, it is not considered a major tourist
destination. However, the climate and proximity to many national and state
parks, as well as the Appalachian Trail foothills, make hiking a popular
activity for both residents and visitors.

Atlanta is a place where people like to "get out of town to be in nature."

## Organization Overview

The Georgia Hiking Club (GHC) is a non-profit hiking club that allows members
to participate in guided trips in Atlanta, surrounding areas, and locations
throughout the country and the world.

The all-volunteer club does not have a physical office or salaried positions.
It does have officers who manage the club, including a CTO who manages the web
server and web application.

The club budget comes from:

- Business sponsorships
- Annual membership fees

## Core System

The Hiking Club Web Application is the core of the business. All club business
is conducted through the web application, and the organization could not exist
without it.

## Hike Diversity and Difficulty

GHC appeals to all ages and fitness levels, so hikes are diverse:

- Beginner hikes for members with limited experience or lower fitness
- Advanced hikes for highly fit or elite-level hikers

Hikes are rated for difficulty so members can choose hikes appropriate for
their fitness level.

## Similarities to Meetup

On the surface, Hiking Club operations are similar to Meetup:

- Trip leaders (similar to Meetup event organizers) post trips that members can
  join.
- Trips can be local or anywhere in the world.
- Two trip types are offered:
  - Free local trips in Atlanta and surrounding areas (under a 3-hour drive)
  - Paid excursions across the country and around the world
- Any member can sign up for local free trips.
- Group size is constrained by minimum and maximum capacity.
- Three user roles are supported:
  - Regular members: register for events and update their own profile
  - Trip leaders: post events and view leader-only member details
  - Administrators: make changes to all information in the system

## Problems Identified in Earlier Iteration

Although an earlier design resembled Meetup, stakeholders identified issues
that threatened the organization:

- Low-cost participation led to full events and long waiting lists, while many
  registered members became no-shows. This left events under capacity and
  blocked waitlisted members unnecessarily.
- Members registered for events beyond their physical ability, creating safety
  and group-management concerns.
- Administrators needed the ability to ban members who violated club policies.
- Leaders lacked visibility into participant medical conditions that might
  require first aid support during hikes.

## Authentication and Security

Members, trip leaders, and administrators log in through an authentication
page using username (email) and password.

Current security gaps:

- Complex passwords are not enforced.
- The site has been compromised by a brute-force attack.

## Member and Event Data Management

The application maintains detailed member records, especially event attendance
history.

For each event, leaders can mark participants as:

- Finish
- Did not Finish
- No Show

Leaders can also add participant notes to support screening for future events.
Leaders now have the ability to reject event registrations when appropriate.

## Confidential Health and Performance Data

Each member profile includes:

- Existing medical conditions
- Performance notes (fitness level)

The hiking club ensures this information remains confidential.

## Payments and Financial Workflow

A payment portal was added to support membership dues collection.

Members can:

- Pay through the portal
- View payment history
- See upcoming payment deadlines

The portal also collects payments for selected paid excursions.

Trip leaders can run reports to identify members who missed payment deadlines.
This enables leaders to:

- Drop unpaid members from the trip
- Refund money already paid
- Move waitlisted members into open spots

## Leader Requirements

Trip leaders must:

- Maintain First Aid training
- Complete an annual physical

Details of leader health conditions that could affect leadership duties are
also stored in the database.
